#!/usr/bin/env python3
import sys, re, csv, hashlib, os, binascii
from pathlib import Path

# Optional: PyCryptodome
try:
    from Crypto.Cipher import AES, ChaCha20
    HAVE_PYCRYPTO = True
except Exception:
    HAVE_PYCRYPTO = False

# ---- Helpers ---------------------------------------------------------------

def bits_to_bytes(bitstr: str) -> bytes:
    # left-to-right, pack by 8 (pad last group with zeros at the end if needed)
    if len(bitstr) % 8 != 0:
        bitstr = bitstr + '0' * (8 - (len(bitstr) % 8))
    return bytes(int(bitstr[i:i+8], 2) for i in range(0, len(bitstr), 8))

def looks_like_flag(data: bytes) -> bool:
    text = None
    try:
        text = data.decode('utf-8', 'ignore')
    except Exception:
        return False
    patterns = [
        r'[A-Z0-9_]{2,}\{[^}]{4,}\}',  # CTF{...}, FLAG{...}, HTB{...}, etc.
        r'flag\s*[:=]\s*.+',           # generic
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)

def dump(fname: Path, data: bytes):
    fname.write_bytes(data)
    print(f"[+] Wrote {fname} ({len(data)} bytes)")

# ---- Step 1: Load and sift QKD --------------------------------------------

def sift_qkd_bits(qkd_path: Path) -> str:
    keep_bits = []
    with qkd_path.open(newline='') as f:
        reader = csv.DictReader(f)
        # Expect columns: AliceBasis,AliceBit,BobBasis,BobResult
        for row in reader:
            aB = row['AliceBasis'].strip()
            aBit = row['AliceBit'].strip()
            bB = row['BobBasis'].strip()
            bRes = row['BobResult'].strip()
            # Keep when same basis
            if aB == bB:
                # sanity: in ideal BB84, bits should match; if not, we still trust AliceBit
                keep_bits.append('1' if aBit == '1' else '0')
    bitstr = ''.join(keep_bits)
    print(f"[+] Sifted {len(keep_bits)} bits from QKD (matching bases).")
    return bitstr

# ---- Step 2: Key derivation ------------------------------------------------

def derive_key(bitstr: str) -> bytes:
    raw = bits_to_bytes(bitstr)
    key = hashlib.sha256(raw).digest()  # 32 bytes, robust for AES-256/ChaCha20
    print(f"[+] Derived key = SHA256(sifted_bytes) = {binascii.hexlify(key).decode()}")
    return key

# ---- Step 3/4: Try decryptions --------------------------------------------

def try_aes_ctr(ct, key, nonce):
    if not HAVE_PYCRYPTO:
        return None, "PyCryptodome not available"
    if len(nonce) not in (12, 16):  # AES-CTR IV sizes vary; many libs accept 16
        # still try with provided
        pass
    try:
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        pt = cipher.decrypt(ct)
        return pt, None
    except Exception as e:
        return None, str(e)

def try_aes_cbc(ct, key, iv):
    if not HAVE_PYCRYPTO:
        return None, "PyCryptodome not available"
    if len(iv) != 16:
        return None, "CBC requires 16-byte IV"
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        pt = cipher.decrypt(ct)
        # best-effort PKCS#7 unpad
        if len(pt) > 0:
            pad = pt[-1]
            if pad > 0 and pad <= 16 and pt.endswith(bytes([pad])*pad):
                pt = pt[:-pad]
        return pt, None
    except Exception as e:
        return None, str(e)

def try_chacha20(ct, key, nonce):
    if not HAVE_PYCRYPTO:
        return None, "PyCryptodome not available"
    if len(nonce) not in (8, 12):  # PyCryptodome expects 8 or 12
        return None, "ChaCha20 wants 8/12-byte nonce"
    try:
        cipher = ChaCha20.new(key=key, nonce=nonce)
        pt = cipher.decrypt(ct)
        return pt, None
    except Exception as e:
        return None, str(e)

def try_toy_stream(ct, key, nonce):
    # Fallback toy keystream: XOR with SHA256(key || nonce || counter)
    pt = bytearray()
    counter = 0
    off = 0
    while off < len(ct):
        ks = hashlib.sha256(key + nonce + counter.to_bytes(8,'big')).digest()
        chunk = ct[off:off+len(ks)]
        pt.extend(bytes(a ^ b for a, b in zip(chunk, ks)))
        off += len(ks)
        counter += 1
    return bytes(pt), None

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} qkd.csv nonce.hex ransomed.enc")
        sys.exit(1)
    qkd_path = Path(sys.argv[1])
    nonce_path = Path(sys.argv[2])
    enc_path = Path(sys.argv[3])

    bitstr = sift_qkd_bits(qkd_path)
    if len(bitstr) == 0:
        print("[-] No sifted bits. Check CSV columns/format.")
        sys.exit(2)
    key = derive_key(bitstr)

    nonce_hex = nonce_path.read_text().strip().replace(" ", "").replace("\n","")
    try:
        nonce = bytes.fromhex(nonce_hex)
    except Exception as e:
        print(f"[-] Could not parse nonce.hex as hex: {e}")
        sys.exit(3)
    print(f"[+] Nonce/IV ({len(nonce)} bytes): {binascii.hexlify(nonce).decode()}")

    ct = enc_path.read_bytes()
    print(f"[+] Ciphertext size: {len(ct)} bytes")

    attempts = []
    attempts.append(("aes-ctr", try_aes_ctr))
    attempts.append(("aes-cbc", try_aes_cbc))
    attempts.append(("chacha20", try_chacha20))
    attempts.append(("toy-sha256-stream", try_toy_stream))

    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)

    any_hit = False
    for name, fn in attempts:
        print(f"\n[*] Trying {name}...")
        pt, err = (fn(ct, key, nonce) if name != "aes-cbc" else fn(ct, key, nonce))
        if err:
            print(f"    error: {err}")
            continue
        out_file = out_dir / f"decrypted_{name}.bin"
        dump(out_file, pt)
        if looks_like_flag(pt):
            print(f"[!!!] {name}: looks like a FLAG is inside this output.")
            any_hit = True

    if not any_hit:
        print("\n[?] No obvious flag detected yet.")
        print("    Open the outputs/ files (try strings/xxd) — one of them may be the real plaintext format.")
        print("    If none look right, we can extend to AES-GCM (need tag parsing) or tweak key derivation (e.g., use AliceBit==BobResult filter, or different bit packing).")

if __name__ == "__main__":
    main()
