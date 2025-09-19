#!/usr/bin/env python3
# solve_qkd_ransom_v2.py
import sys, csv, re, os, binascii, hashlib
from pathlib import Path

# crypto
from Crypto.Cipher import AES, ChaCha20
from Crypto.Cipher import ChaCha20_Poly1305

def load_qkd(path):
    rows = []
    with open(path, newline='') as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append({
                'aB': row['AliceBasis'].strip(),
                'a':  1 if row['AliceBit'].strip()   == '1' else 0,
                'bB': row['BobBasis'].strip(),
                'b':  1 if row['BobResult'].strip() == '1' else 0,
            })
    return rows

def sift(rows, rule):
    bits = []
    for row in rows:
        if row['aB'] != row['bB']:
            continue
        a, b = row['a'], row['b']
        if rule == 'alice':
            bits.append(a)
        elif rule == 'equal_only':
            if a == b:
                bits.append(a)  # could also append b, same value
        elif rule == 'bob':
            bits.append(b)
        elif rule == 'xor':
            bits.append(a ^ b)
    return bits

def pack_bits(bits, order='msb'):
    # returns bytes from list of 0/1
    out = bytearray()
    acc = 0
    cnt = 0
    if order == 'msb':
        for bit in bits:
            acc = (acc << 1) | (bit & 1)
            cnt += 1
            if cnt == 8:
                out.append(acc)
                acc = 0
                cnt = 0
        if cnt:
            acc <<= (8 - cnt)
            out.append(acc)
    else:  # lsb-first in each byte
        for bit in bits:
            acc |= ((bit & 1) << cnt)
            cnt += 1
            if cnt == 8:
                out.append(acc)
                acc = 0
                cnt = 0
        if cnt:
            out.append(acc)
    return bytes(out)

def candidate_keys(raw):
    keys = []
    sha = hashlib.sha256(raw).digest()
    keys.append(('raw32_pad', (raw + b'\x00'*32)[:32]))   # naive 32-byte
    keys.append(('sha256', sha))                          # 32-byte
    keys.append(('sha256_16', sha[:16]))                  # AES-128
    return keys

def looks_text(b):
    sample = b[:4096]
    printable = sum(32 <= c <= 126 or c in (9,10,13) for c in sample)
    ratio = printable / max(1, len(sample))
    return ratio > 0.85

def find_flags(b):
    s = b.decode('utf-8', 'ignore')
    hits = []
    # prioritize CBCTF format
    for m in re.findall(r'CBCTF\{[^}\n]{4,200}\}', s):
        hits.append(m)
    # generic brace flags as backup
    for m in re.findall(r'[A-Za-z0-9_]{2,}\{[^}\n]{4,200}\}', s):
        if m not in hits:
            hits.append(m)
    return hits

def magic_guess(b):
    if b.startswith(b'%PDF-'): return 'PDF'
    if b.startswith(b'PK\x03\x04'): return 'ZIP'
    if b.startswith(b'\x89PNG\r\n\x1a\n'): return 'PNG'
    if b.startswith(b'\x7fELF'): return 'ELF'
    if b.startswith(b'CBCTF{'): return 'FLAG-START'
    return None

def try_aes_ctr(ct, key, nonce):
    try:
        c = AES.new(key, AES.MODE_CTR, nonce=nonce)
        return c.decrypt(ct)
    except Exception:
        return None

def try_aes_gcm(ct, key, nonce):
    # assume last 16 bytes = tag
    if len(ct) < 16: return None
    ctext, tag = ct[:-16], ct[-16:]
    try:
        c = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return c.decrypt_and_verify(ctext, tag)
    except Exception:
        return None

def try_chacha20(ct, key, nonce):
    try:
        c = ChaCha20.new(key=key, nonce=nonce)
        return c.decrypt(ct)
    except Exception:
        return None

def try_chacha20_poly(ct, key, nonce):
    if len(ct) < 16: return None
    ctext, tag = ct[:-16], ct[-16:]
    try:
        c = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        return c.decrypt_and_verify(ctext, tag)
    except Exception:
        return None

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} qkd.csv nonce.hex ransomed.enc")
        sys.exit(1)

    rows = load_qkd(sys.argv[1])
    nonce = bytes.fromhex(Path(sys.argv[2]).read_text().strip())
    ct = Path(sys.argv[3]).read_bytes()

    rules = ['alice','equal_only','bob','xor']
    orders = ['msb','lsb']
    modes = [
        ('aes-ctr', try_aes_ctr),
        ('aes-gcm', try_aes_gcm),
        ('chacha20', try_chacha20),
        ('chacha20-poly', try_chacha20_poly),
    ]

    outdir = Path('outputs_v2'); outdir.mkdir(exist_ok=True)
    tried = 0; hits = []

    for rule in rules:
        bits = sift(rows, rule)
        if len(bits) < 64:
            continue
        for order in orders:
            raw = pack_bits(bits, order)
            for kname, key in candidate_keys(raw):
                for mname, fn in modes:
                    # key size constraints per mode
                    if mname.startswith('aes') and len(key) not in (16,24,32): 
                        continue
                    if mname.startswith('chacha20') and len(key) != 32:
                        continue
                    if len(nonce) not in (12,16,8):  # pragmatic
                        pass

                    tried += 1
                    pt = fn(ct, key, nonce)
                    if pt is None: 
                        continue

                    fl = find_flags(pt)
                    mg = magic_guess(pt)
                    txty = looks_text(pt)
                    if fl or mg or txty:
                        tag = f"{rule}-{order}-{kname}-{mname}"
                        outp = outdir / f"dec_{tag}.bin"
                        outp.write_bytes(pt)
                        print(f"[+] Candidate HIT: {tag}  | flags: {len(fl)}  | magic: {mg}  | texty: {txty}")
                        if fl:
                            for f in fl:
                                print(f"    FLAG: {f}")
                        hits.append((tag, fl, mg, txty))

    if not hits:
        print("[-] No hits yet. We can extend with counter params for AES-CTR (prefix lengths) or try trimming tag sizes.")
    else:
        print(f"\n[+] Done. {len(hits)} promising candidates saved in outputs_v2/.")
        print("    If multiple, open the ones that report CBCTF hits or clear text. Example:")
        print("    strings outputs_v2/dec_<tag>.bin | grep -Eo 'CBCTF\\{[^}]+' -m1")

if __name__ == '__main__':
    from pathlib import Path
    main()
