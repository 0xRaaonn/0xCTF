#!/usr/bin/env python3
# solve_qkd_ransom_v4.py
import sys, csv, re, hashlib, hmac, binascii, itertools
from pathlib import Path
from Crypto.Cipher import AES, ChaCha20
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Util import Counter
from Crypto.Protocol.KDF import HKDF, PBKDF2, scrypt

# ---------- QKD parsing ----------
def load_qkd(path):
    rows=[]
    with open(path, newline='') as f:
        r=csv.DictReader(f)
        for row in r:
            rows.append({
                'aB': row['AliceBasis'].strip(),
                'a':  1 if row['AliceBit'].strip()=='1' else 0,
                'bB': row['BobBasis'].strip(),
                'b':  1 if row['BobResult'].strip()=='1' else 0,
            })
    return rows

def sift(rows, mode):
    bits=[]
    for r in rows:
        aB,a,bB,b=r['aB'],r['a'],r['bB'],r['b']
        if mode=='match_alice' and aB==bB: bits.append(a)
        elif mode=='match_equal' and aB==bB and a==b: bits.append(a)
        elif mode=='match_bob' and aB==bB: bits.append(b)
        elif mode=='xor' and aB==bB: bits.append(a^b)
        elif mode=='Z_alice' and aB==bB=='Z': bits.append(a)
        elif mode=='Z_bob' and aB==bB=='Z': bits.append(b)
    return bits

def pack_bits(bits, order='msb'):
    out=bytearray(); acc=0; cnt=0
    if order=='msb':
        for bit in bits:
            acc=(acc<<1)|(bit&1); cnt+=1
            if cnt==8: out.append(acc); acc=0; cnt=0
        if cnt: out.append((acc<<(8-cnt))&0xFF)
    else:
        for bit in bits:
            acc |= ((bit&1)<<cnt); cnt+=1
            if cnt==8: out.append(acc); acc=0; cnt=0
        if cnt: out.append(acc)
    return bytes(out)

def slice_bits(bits, mode):
    # return a list of 0/1 of length exactly 256 or 128 depending on mode
    need = 256 if '256' in mode else 128
    if len(bits) < need: return None
    if mode.startswith('first'): return bits[:need]
    if mode.startswith('last'):  return bits[-need:]
    return None

# ---------- Key variants ----------
def key_variants(raw, nonce):
    ks=[]
    sha=hashlib.sha256(raw).digest()
    ks.append(('raw32', (raw+b'\x00'*32)[:32]))
    ks.append(('sha256', sha))
    ks.append(('sha1_16', hashlib.sha1(raw).digest()[:16]))
    ks.append(('md5_16', hashlib.md5(raw).digest()))
    # HKDF with salt=nonce
    ks.append(('hkdf_sha256', HKDF(master=raw, key_len=32, salt=nonce, hashmod=hashlib.sha256)))
    # PBKDF2 with salt=nonce (moderate iters)
    ks.append(('pbkdf2_10k', PBKDF2(password=raw, salt=nonce, dkLen=32, count=10000, hmac_hash_module=hashlib.sha256)))
    # scrypt with salt=nonce
    ks.append(('scrypt', scrypt(password=raw, salt=nonce, key_len=32, N=1<<14, r=8, p=1)))
    return ks

# ---------- Heuristics ----------
def find_flags(b):
    s=b.decode('utf-8','ignore')
    return re.findall(r'CBCTF\{[^}\n]{4,200}\}', s)

def textiness(b):
    sample=b[:4096]
    printable=sum(32<=c<=126 or c in (9,10,13) for c in sample)
    return printable/max(1,len(sample))

def magic(b):
    if b.startswith(b'%PDF-'): return 'PDF'
    if b.startswith(b'PK\x03\x04'): return 'ZIP'
    if b.startswith(b'\x89PNG\r\n\x1a\n'): return 'PNG'
    if b.startswith(b'CBCTF{'): return 'FLAG-START'
    return None

# ---------- CTR layouts ----------
def ctr_variants(key, nonce12):
    outs=[]
    n=nonce12
    # pycryptodome default: prefix=nonce, counter_len=4 (BE)
    try:
        c=AES.new(key, AES.MODE_CTR, nonce=n); outs.append(('ctr.prefix12+ctr32_BE.pyc', c))
    except: pass
    # prefix12 + ctr32 LE/BE start at 0 and 1
    for endian,name in ((True,'LE'),(False,'BE')):
        for iv0 in (0,1):
            try:
                ctr=Counter.new(32, prefix=n, initial_value=iv0, little_endian=endian)
                outs.append((f'ctr.prefix12+ctr32_{name}.iv{iv0}', AES.new(key, AES.MODE_CTR, counter=ctr)))
            except: pass
    # prefix8 + ctr64
    p8=n[:8]
    for endian,name in ((True,'LE'),(False,'BE')):
        for iv0 in (0,1):
            try:
                ctr=Counter.new(64, prefix=p8, initial_value=iv0, little_endian=endian)
                outs.append((f'ctr.prefix8+ctr64_{name}.iv{iv0}', AES.new(key, AES.MODE_CTR, counter=ctr)))
            except: pass
    # (counter || nonce) 4+12 (BE/LE), iv0=0/1
    for endian,name in ((True,'LE'),(False,'BE')):
        for iv0 in (0,1):
            try:
                ctr=Counter.new(32, prefix=b'', initial_value=iv0, little_endian=endian, suffix=n)
                outs.append((f'ctr.ctr32_{name}+suffix12.iv{iv0}', AES.new(key, AES.MODE_CTR, counter=ctr)))
            except: pass
    # full 16-byte IV by appending 4 bytes (0 or 1) then interpret as 128-bit counter (BE/LE)
    for pad in (b'\x00\x00\x00\x00', b'\x00\x00\x00\x01', b'\x01\x00\x00\x00'):
        iv16=n+pad
        for endian,name in ((False,'BE'),(True,'LE')):
            try:
                init=int.from_bytes(iv16, 'little' if endian else 'big')
                ctr=Counter.new(128, initial_value=init, little_endian=endian)
                outs.append((f'ctr.full128_{name}.iv={iv16.hex()}', AES.new(key, AES.MODE_CTR, counter=ctr)))
            except: pass
    return outs

# ---------- AEAD tries ----------
def try_aes_gcm(ct, key, nonce, aad_list):
    outs=[]
    for taglen in (16,12,32):
        if len(ct) <= taglen: continue
        ctext, tag = ct[:-taglen], ct[-taglen:]
        for aad in aad_list:
            try:
                c=AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=taglen)
                if aad: c.update(aad)
                pt=c.decrypt_and_verify(ctext, tag)
                outs.append((f'gcm.tag{taglen}.aad={aad!r}', pt))
            except Exception:
                pass
    return outs

def try_chacha20(key, nonce, ct):
    try:
        c=ChaCha20.new(key=key, nonce=nonce)
        return [('chacha20', c.decrypt(ct))]
    except: return []

def try_chacha20_poly(key, nonce, ct, aad_list):
    outs=[]
    taglen=16
    if len(ct)<=taglen: return outs
    ctext, tag = ct[:-taglen], ct[-taglen:]
    for aad in aad_list:
        try:
            c=ChaCha20_Poly1305.new(key=key, nonce=nonce)
            if aad: c.update(aad)
            pt=c.decrypt_and_verify(ctext, tag)
            outs.append((f'chacha20poly.tag16.aad={aad!r}', pt))
        except: pass
    return outs

# ---------- main ----------
def main():
    if len(sys.argv)!=4:
        print(f"Usage: {sys.argv[0]} qkd.csv nonce.hex ransomed.enc"); sys.exit(1)
    rows=load_qkd(sys.argv[1])
    nonce=bytes.fromhex(Path(sys.argv[2]).read_text().strip())
    ct=Path(sys.argv[3]).read_bytes()
    outdir=Path('outputs_v4'); outdir.mkdir(exist_ok=True)

    csv_header=b'AliceBasis,AliceBit,BobBasis,BobResult\n'
    aad_candidates=[b'', nonce, b'QKD', csv_header]

    sift_modes=['match_alice','match_equal','match_bob','xor','Z_alice','Z_bob']
    orders=['msb','lsb']
    bit_slices=['full', 'first256', 'last256', 'first128', 'last128']

    hits=[]
    for sm in sift_modes:
        base_bits=sift(rows, sm)
        if len(base_bits)<64: continue
        for bs in bit_slices:
            if bs=='full':
                use_bits=base_bits
            else:
                use_bits=slice_bits(base_bits, bs)
                if use_bits is None: continue
            for order in orders:
                raw=pack_bits(use_bits, order)
                for kname, key in key_variants(raw, nonce):
                    # AES-CTR
                    for tag, cipher in ctr_variants(key, nonce):
                        try:
                            pt=cipher.decrypt(ct)
                        except Exception:
                            continue
                        score=0
                        flags=find_flags(pt)
                        mg=magic(pt)
                        t=textiness(pt)
                        if flags: score=3
                        elif mg:  score=2
                        elif t>0.85: score=1
                        if score:
                            fname=outdir/f"ctr_{sm}-{bs}-{order}-{kname}-{tag}.bin"
                            fname.write_bytes(pt)
                            print(f"[+] CTR HIT {fname.name} | score={score} | flags={flags[:2]}")
                            hits.append(fname)

                    # AES-GCM
                    for tag, pt in try_aes_gcm(ct, key, nonce, aad_candidates):
                        flags=find_flags(pt); mg=magic(pt); t=textiness(pt)
                        score=3 if flags else 2 if mg else (1 if t>0.85 else 0)
                        if score:
                            fname=outdir/f"gcm_{sm}-{bs}-{order}-{kname}-{tag}.bin"
                            fname.write_bytes(pt)
                            print(f"[+] GCM HIT {fname.name} | score={score} | flags={flags[:2]}")
                            hits.append(fname)

                    # ChaCha20 (no tag)
                    for tag, pt in try_chacha20(key, nonce, ct):
                        flags=find_flags(pt); mg=magic(pt); t=textiness(pt)
                        score=3 if flags else 2 if mg else (1 if t>0.85 else 0)
                        if score:
                            fname=outdir/f"{tag}_{sm}-{bs}-{order}-{kname}.bin"
                            fname.write_bytes(pt)
                            print(f"[+] {tag} HIT {fname.name} | score={score} | flags={flags[:2]}")
                            hits.append(fname)

                    # ChaCha20-Poly1305
                    for tag, pt in try_chacha20_poly(key, nonce, ct, aad_candidates):
                        flags=find_flags(pt); mg=magic(pt); t=textiness(pt)
                        score=3 if flags else 2 if mg else (1 if t>0.85 else 0)
                        if score:
                            fname=outdir/f"{tag}_{sm}-{bs}-{order}-{kname}.bin"
                            fname.write_bytes(pt)
                            print(f"[+] CP HIT {fname.name} | score={score} | flags={flags[:2]}")
                            hits.append(fname)

    if not hits:
        print("[-] Still nothing conclusive. Two more pivots:\n"
              "    (1) try AES-SIV (RFC5297) or AES-GCM-SIV (less common in PyCryptodome)\n"
              "    (2) try using NONCE as salt to HKDF but with info=b'CBCTF' or b'QKD'.")
    else:
        print(f"[+] Saved {len(hits)} promising candidates to outputs_v4/. Check for CBCTF{...} first.")
        print("    Example: grep -aEo 'CBCTF\\{[^}]+' outputs_v4/* | head")
if __name__=='__main__':
    main()
