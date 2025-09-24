# CBCTF – Journey Home in Tokyo (Crypto Challenge Writeup)

## Challenge Description

We were given a ciphertext and an image of the Tokyo subway map centered on **Hinode Station**:

```
}NNNIOFCSCE-OGITSPT{TBEF_T-SC
```

The problem statement hinted that the flag format is `CBCTF{...}`.

## Solution Steps

1. **Initial observation**
   The ciphertext clearly had braces (`{ }`) but placed incorrectly. That suggested it was already close to a flag format. The presence of dashes and underscores also matched typical CTF flag word separation.

2. **Analyzing the hint (map)**
   The Tokyo subway map centered on **Hinode (日の出)** station was given. "Hinode" literally means **sunrise**, but more importantly the map with **rail lines** hinted at a **Rail Fence Cipher**.

3. **Testing Rail Fence**
   The ciphertext length was 29 characters. Using an online tool ([https://www.boxentriq.com/code-breaking/rail-fence-cipher](https://www.boxentriq.com/code-breaking/rail-fence-cipher)) and selecting **3 rails** for decryption produced a promising output:

   ```
   }SECNEF-NO_GNITTIS-POTS{FTCBC
   ```

4. **Reversing the text**
   The decryption looked like English words but backwards. Reversing it yielded:

   ```
   CBCTF{STOP-SITTING_ON-FENCES}
   ```

   This matches the expected `CBCTF{}` format.

## Flag

```
CBCTF{STOP-SITTING_ON-FENCES}
```

## Identified Vulnerability / Trick

The trick was recognizing that the hint (subway **rails**) pointed to a **Rail Fence Cipher**. Once decoded, the output was simply reversed, giving the final flag.

## Remediation / Lesson

* Always pay attention to non-textual hints; they often point directly to the cipher used.

* Rail Fence ciphers are a common CTF classic; train maps or anything with "rails" often signal it.

* Online cipher tools like Boxentriq are very handy for quickly testing classical cipher hypotheses.

* If the decrypted text looks almost right but scrambled, try simple transformations (like reversing the string).
