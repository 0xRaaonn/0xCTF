# Crypto: Caesar and Friends — CTF Write-Up

## Challenge Information

- **Category:** Cryptography
- **Challenge:** Caesar and Friends
- **Difficulty:** 1/5
- **Points:** 5
- **Objective:** Decrypt an intercepted transmission encoded using a classical substitution cipher and retrieve the hidden flag.

## Challenge Description

The challenge states that an intercepted transmission has been encoded using a **classical cipher**. The challenge instance provides an encrypted message and explains that every letter has been shifted by the same fixed amount.

This strongly indicates a **Caesar cipher**, where each letter in the plaintext is shifted by a fixed number of positions in the alphabet.

The objective also notes that there are only **25 possible shifts**, so brute-forcing every possible Caesar shift is practical.

## Analysis

From the challenge description, we know:

1. The encryption is a classical substitution cipher.
2. Every character is shifted by the same fixed amount.
3. Only 25 meaningful shifts need to be tested.
4. The decrypted message should contain a token in the format `flag{...}`.

Because the keyspace is extremely small, there is no need to determine the key manually before attempting decryption. We can simply test every possible Caesar shift and identify the output that produces readable English.

## Solution

### Step 1 — Obtain the Ciphertext

After launching the challenge instance, an intercepted transmission is displayed. The ciphertext can also be downloaded using the **Download transmission.txt** button.

The encrypted message initially appears as unreadable shifted text.

### Step 2 — Identify the Cipher

The challenge explicitly describes a substitution where every letter is shifted by the same fixed amount.

This is the defining behavior of a Caesar cipher:

```text
Plaintext:   ABCDEFGHIJKLMNOPQRSTUVWXYZ
Ciphertext:  DEFGHIJKLMNOPQRSTUVWXYZABC
```

The exact mapping depends on the shift value.

### Step 3 — Brute-Force the Caesar Shift

The ciphertext was pasted into a Caesar cipher decoder and all possible shifts were tested.

A readable result appeared using:

```text
Shift / Key: 3
```

The decrypted transmission begins with:

```text
CLASSIFIED COMMUNICATION -
PROJECT NIGHTFALL

Priority: HIGH
Date: 2025-03-14
From: Director V.
To: Field Unit Seven
```

The remaining plaintext explains that the rendezvous at sector nine has been relocated and contains the access token required by the challenge.

### Step 4 — Extract the Flag

Inside the decrypted plaintext, the access token is revealed as:

```text
Access token:
flag{caesar_shift_cracked}
```

The token was submitted to the challenge platform and accepted as correct.

## Flag

```text
flag{caesar_shift_cracked}
```

## Alternative: Solve with Python

Instead of using an online Caesar decoder, all 25 shifts can be tested with a short Python script:

```python
ciphertext = "PASTE_CIPHERTEXT_HERE"

for shift in range(1, 26):
    result = ""

    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
        else:
            result += char

    print(f"Shift {shift}:")
    print(result)
    print("-" * 50)
```

We then inspect the results for readable English or search directly for the expected `flag{` pattern.

## Why the Attack Works

A Caesar cipher has an extremely small keyspace. For the English alphabet there are only 25 non-trivial shifts.

Therefore, an attacker can simply attempt:

```text
Shift 1
Shift 2
Shift 3
...
Shift 25
```

and identify the plaintext without knowing the original key.

In this challenge, **shift 3** produces the readable transmission and exposes the flag.

## Conclusion

This challenge demonstrates the weakness of classical Caesar-shift encryption. Although the ciphertext initially appears unreadable, the cipher provides effectively no meaningful security because its entire keyspace can be brute-forced almost instantly.

**Key takeaway:** Caesar cipher should never be used to protect sensitive information because testing all possible keys is trivial.

## Final Answer

```text
flag{caesar_shift_cracked}
```
