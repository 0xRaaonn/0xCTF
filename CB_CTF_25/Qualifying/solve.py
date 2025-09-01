#!/usr/bin/env python3
from pwn import *
import string

HOST = "exploit.cyberbattle.info"
PORT = 9999

banner_fail = b"YOU SHALL NOT PASS"

def caesar(s, k):
    out = []
    for ch in s:
        if 'a' <= ch <= 'z':
            out.append(chr((ord(ch)-97 + k) % 26 + 97))
        elif 'A' <= ch <= 'Z':
            out.append(chr((ord(ch)-65 + k) % 26 + 65))
        else:
            out.append(ch)
    return ''.join(out)

def vigenere(pt, key):
    res = []
    ki = 0
    for ch in pt:
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            k = ord(key[ki % len(key)].lower()) - 97
            res.append(chr((ord(ch)-base + k) % 26 + base))
            ki += 1
        else:
            res.append(ch)
    return ''.join(res)

base_words = [
    "mellon", "Pedo mellon a minno".lower(),
    "moria","durin","khazaddum","khazad-dum",
    "nazgul","ulairi","friend"
]

decor = lambda s: [s, s+"9", "9"+s, s+"-9", s+"^9", s+"_nine", s+"nine", s+"IX", s+"9nine", s+"9x"]
keys  = ["nazgul","moria","durin","khazad","mellon"]

def gen_candidates():
    seen = set()
    # base + simple decorations
    for b in base_words:
        for d in decor(b):
            if d not in seen:
                seen.add(d); yield d
    # Caesar (ROT all, highlight ROT9 & ROT13)
    for b in base_words:
        for k in range(1,26):
            c = caesar(b, k)
            if k in (9,13) or b=="mellon":  # prioritize hinty ones
                for d in decor(c):
                    if d not in seen:
                        seen.add(d); yield d
    # Vigenère with LotR keys
    for b in base_words:
        for key in keys:
            v = vigenere(b, key)
            for d in decor(v):
                if d not in seen:
                    seen.add(d); yield d

def try_one(pw):
    io = remote(HOST, PORT, level='error')
    data = io.recvuntil(b"Enter the password", drop=False, timeout=3)
    io.sendline(pw.encode())
    out = io.recvrepeat(1.5)  # grab a bit more output
    io.close()
    if banner_fail not in out:
        print(f"[HIT?] {pw!r}\n{out.decode(errors='ignore')}\n{'-'*60}")
        return True
    return False

if __name__ == "__main__":
    for guess in gen_candidates():
        if try_one(guess):
            break
