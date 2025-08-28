# Hashcrack – picoCTF Write-up

**Author:** Nana Ama Atombo-Sackey  
**Category:** Crypto / Misc  
**Challenge:** Hashcrack  

---

## Challenge Description
A company stored a secret message on a server which got breached due to the admin using weakly hashed passwords. Can you gain access to the secret stored within the server?

Access: `nc verbal-sleep.picoctf.net 65347`

---

## Solution Steps

1. **Connect to the service:**
   ```bash
   nc verbal-sleep.picoctf.net 65347
   ```

2. **Identify the hash provided:**
   - The service presented several hashes in sequence, each needing to be cracked to progress.
   - The hash algorithms were recognizable by their length:
     - **MD5:** 32 hex chars
     - **SHA1:** 40 hex chars
     - **SHA256:** 64 hex chars

3. **Crack the hashes:**
   - For MD5:
     ```
     482c811da5d5b4bc6d497ffa98491e38 → password123
     ```
   - For SHA1:
     ```
     b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3 → letmein
     ```
   - For SHA256:
     ```
     916e8c4f79b25028c9e467f1eb8eee6d6bbdff965f9928310ad30a8d88697745 → qwerty098
     ```

   Tools used:
   - `john` with `--format=raw-md5`, `raw-sha1`, `raw-sha256`

```
echo '916e8c4f79b25028c9e467f1eb8eee6d6bbdff965f9928310ad30a8d88697745' > hash.txt
john --format=raw-sha256 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
john --show --format=raw-sha256 hash.txt
```

   - `hashcat` with modes `-m 0`, `-m 100`, and `-m 1400`

```
echo '916e8c4f79b25028c9e467f1eb8eee6d6bbdff965f9928310ad30a8d88697745' > hash.txt
# SHA-256 = -m 1400 ; straight dictionary = -a 0
hashcat -m 1400 -a 0 hash.txt /usr/share/wordlists/rockyou.txt --force
# when it cracks, show the plaintext:
hashcat -m 1400 --show hash.txt
```

4. **Authenticate with cracked passwords:**
   Each cracked password was submitted to the service. On the final hash, providing `qwerty098` unlocked the secret.

5. **Flag Obtained:**
   ```
   picoCTF{UseStr0nG_h@shEs_&PaSswDs!_eb2f8459}
   ```

---

## Identified Vulnerability
- **Weak Hashing Algorithms:** MD5, SHA1, and unsalted SHA256 are all considered insecure for password storage. They are designed for speed and can be brute-forced rapidly with modern hardware.
- **Weak Passwords:** The chosen passwords (`password123`, `letmein`, `qwerty098`) are common and appear in public wordlists like *rockyou.txt*.

---

## Remediation
- Use strong, slow password hashing algorithms such as **bcrypt**, **scrypt**, **PBKDF2**, or **Argon2**.
- Always salt passwords before hashing to prevent precomputed attacks (rainbow tables).
- Enforce stronger password policies (length, complexity, disallowing common passwords).
- Implement rate-limiting and account lockout mechanisms to mitigate brute-force attempts.

