#!/usr/bin/env python3
# solve_qkd_ransom_v3.py
import sys, csv, re, binascii, hashlib
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util import Counter

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
        if mode=='match_alice':
            if aB==bB: bits.append(a)
        elif mode=='match_equal':
            if aB==bB and a==b: bits.append(a)
        elif mode=='match_bob':
            if aB==bB: bits.append(b)
        elif mode=='xor':
            if aB==bB: bits.append(a^b)
        elif mode=='Z_alice':
            if aB==bB=='Z': bits.append(a)
        elif mode=='Z_bob':
            if aB==bB=='Z': bits.append(b)
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

def key_variants(raw):
    sha=hashlib.sha256(raw).digest()
    ks=[]
    ks.append(('raw32', (raw+b'\x00'*32)[:32]))
    ks.append(('sha256', sha))
    ks.append(('sha256_16', sha[:16]))
    # author could have used ASCII "0/1" string directly
    ascii01 = ''.join('1' if ((b>>i)&1) else '0' for b in raw for i in range(7,-1,-1)).encode()
    ks.append(('sha256_ascii01', hashlib.sha256(ascii01).digest()))
    return ks

def try_aes_ctr_layouts(ct, key, nonce12: bytes):
    """Brute common CTR layouts. Yield (tag, pt) on success."""
    outs=[]
    n=nonce12
    # 1) PyCryptodome nonce=prefix, counter_len=4 (big-endian) [default-ish]
    try:
        c = AES.new(key, AES.MODE_CTR, nonce=n)  # counter_len inferred = 4
        outs.append(('ctr.prefix12+ctr32_BE.pycryptodome', c.decrypt(ct)))
    except: pass

    # 2) prefix12 + counter32 LE
    for iv0 in (0,1):
        try:
            ctr = Counter.new(32, prefix=n, initial_value=iv0, little_endian=True)
            c = AES.new(key, AES.MODE_CTR, counter=ctr)
            outs.append((f'ctr.prefix12+ctr32_LE.iv{iv0}', c.decrypt(ct)))
        except: pass

    # 3) prefix8 + counter64 (BE/LE), using first 8 bytes of nonce as prefix
    p8=n[:8]
    for endian,name in ((False,'BE'),(True,'LE')):
        for iv0 in (0,1):
            try:
                ctr = Counter.new(64, prefix=p8, initial_value=iv0, little_endian=endian)
                c = AES.new(key, AES.MODE_CTR, counter=ctr)
                outs.append((f'ctr.prefix8+ctr64_{name}.iv{iv0}', c.decrypt(ct)))
            except: pass

    # 4) Full 16-byte IV by padding nonce with 4 zero/one bytes, big vs little initial counter
    for pad in (b'\x00\x00\x00\x00', b'\x00\x00\x00\x01', b'\x01\x00\x00\x00'):
        iv16 = n + pad
        for endian,name in ((False,'BE'),(True,'LE')):
            try:
                init = int.from_bytes(iv16, 'little' if endian else 'big')
                ctr = Counter.new(128, initial_value=init, little_endian=endian)
                c = AES.new(key, AES.MODE_CTR, counter=ctr)
                outs.append((f'ctr.full128_{name}.iv={iv16.hex()}', c.decrypt(ct)))
            except: pass

    return outs

def looks_reasonable(b: bytes):
    # quick heuristics: high ASCII ratio or obvious magic/flag
    s = b[:65536].decode('utf-8','ignore')
    txt_ratio = sum(32<=c<=126 or c in (9,10,13) for c in b[:4096]) / max(1,len(b[:4096]))
    if 'CBCTF{' in s: return 3
    if s.startswith('CBCTF{'): return 3
    if b.startswith(b'%PDF-') or b.startswith(b'PK\x03\x04') or b.startswith(b'\x89PNG\r\n\x1a\n'): return 2
    if txt_ratio > 0.80: return 1
    return 0

def main():
    if len(sys.argv)!=4:
        print(f"Usage: {sys.argv[0]} qkd.csv nonce.hex ransomed.enc"); sys.exit(1)
    rows = load_qkd(sys.argv[1])
    nonce = bytes.fromhex(Path(sys.argv[2]).read_text().strip())
    ct = Path(sys.argv[3]).read_bytes()
    outdir = Path('outputs_v3'); outdir.mkdir(exist_ok=True)

    sift_modes = ['match_alice','match_equal','match_bob','xor','Z_alice','Z_bob']
    orders = ['msb','lsb']
    hits=[]; tried=0

    for sm in sift_modes:
        bits = sift(rows, sm)
        if len(bits) < 64: 
            continue
        for order in orders:
            raw = pack_bits(bits, order)
            for kname, key in key_variants(raw):
                # try AES-CTR constructions
                for tag, pt in try_aes_ctr_layouts(ct, key, nonce):
                    tried += 1
                    score = looks_reasonable(pt)
                    if score:
                        fname = outdir / f"dec_{sm}-{order}-{kname}-{tag}.bin"
                        fname.write_bytes(pt)
                        flags = re.findall(r'CBCTF\{[^}\n]{4,200}\}', pt.decode('utf-8','ignore'))
                        print(f"[+] CTR candidate: {fname.name}  | score={score} | flags={len(flags)}")
                        if flags:
                            for f in flags:
                                print("    FLAG:", f)
                        hits.append((fname.name, score, len(flags)))

    if not hits:
        print("[-] No joy yet. Next steps: try AES-GCM with explicit tag split positions (last 16/32), or ChaCha20-Poly1305 (tag16) with same key set.")
    else:
        print(f"\n[+] Saved {len(hits)} promising CTR plaintexts in outputs_v3/. Check ones with score=3 first.")
        print("    Example grep: strings outputs_v3/*.bin | grep -Eo 'CBCTF\\{[^}]+' -m1")

if __name__=='__main__':
    from pathlib import Path
    main()
