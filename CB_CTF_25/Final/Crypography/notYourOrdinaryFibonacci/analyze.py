from hashlib import sha256, md5
from os import urandom
import sys

sys.set_int_max_str_digits(0)

FLAG = b"CBCTF{xxxxxxxxxxxxxxx}"

def george(n):
    
    if n == 0:
        return 2
    if n == 1:
        return 1
    

    L = [[1, 1], [1, 0]]
    power_matrix(L, n - 1)
    return L[0][0] + L[0][1]  

def multiply_matrix(F, M):

    x = (F[0][0] * M[0][0] + F[0][1] * M[1][0])
    y = (F[0][0] * M[0][1] + F[0][1] * M[1][1])
    z = (F[1][0] * M[0][0] + F[1][1] * M[1][0])
    w = (F[1][0] * M[0][1] + F[1][1] * M[1][1])
    F[0][0] = x
    F[0][1] = y
    F[1][0] = z
    F[1][1] = w

def power_matrix(F, n):
  
    if n == 0 or n == 1:
        return
    M = [[1, 1], [1, 0]]
    power_matrix(F, n // 2)
    multiply_matrix(F, F)
    if n % 2 != 0:
        multiply_matrix(F, M)

def gen_composite_key(k):
  
    L_k = george(k)
    
 
    k2 = (k * 0x1337) % 0xDEAD
    L_k2 = george(k2)

    primary_hash = sha256(str(L_k).encode()).digest()
    secondary_hash = md5(str(L_k2).encode()).digest()

    padded_secondary = secondary_hash * 2  
    composite_key = bytes(a ^ b for a, b in zip(primary_hash, padded_secondary))
    
    return composite_key

def advanced_pad(m, block_size=16):
    
    padding_len = block_size - (len(m) % block_size)
   
    random_pad = urandom(padding_len - 1) if padding_len > 1 else b''
    length_byte = bytes([len(m) % 256])  
    return m + random_pad + length_byte



def encrypt(m, key):
  
    m = advanced_pad(m)
    c = bytearray()
    
    for i, byte in enumerate(m):
       
        key_idx = i % len(key)
        rotated_key_byte = ((key[key_idx] << (i % 8)) | (key[key_idx] >> (8 - (i % 8)))) & 0xFF
        c.append(byte ^ rotated_key_byte)
    
    return bytes(c)




k = 13337  
key = gen_composite_key(k)
ct = encrypt(FLAG, key)

with open("output.txt", "w") as f:
    f.write(ct.hex())


assert pt == FLAG

print(f"Challenge generated successfully!")
print(f"Primary parameter k: {k}")
print(f"Secondary parameter k2: {(k * 0x1337) % 0xDEAD}")
print(f"Ciphertext written to output.txt")
print(f"Hint: This isn't your ordinary Fibonacci...")