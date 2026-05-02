# 🧩 The Shrine's Secret (50 pts)

> ⛩️ “The ancient scribes liked to shift things around…”

---

## 📌 Challenge Description

While exploring a quiet Shinto shrine in Kyoto, you notice something carved into the back of the torii gate. It looks like letters, but they don't make any sense.

The shrine keeper hints that the text has been **shifted**.

```
YVP{fue1ar_tngr_haybpxrq}
```

---

## 🧠 Initial Thoughts

- The text looks like a flag format but **obfuscated**
- Hint mentions:
  - “shift things around”
  - “rotate by 13 places”

👉 This strongly indicates **ROT13 cipher**

---

## 🔍 Analysis & Approach

### What is ROT13?
- A substitution cipher
- Each letter is shifted **13 positions**
- Applying ROT13 **twice returns original text**

Example:
- A ↔ N  
- B ↔ O  
- C ↔ P  

---

## 🛠️ Solution

### Method 1: CyberChef
1. Open CyberChef
2. Paste the encoded string
3. Apply: `ROT13`

---

### Method 2: Python

```python
import codecs

encoded = "YVP{fue1ar_tngr_haybpxrq}"
decoded = codecs.decode(encoded, 'rot_13')

print(decoded)
```

---

## 🧾 Decoded Output

```
LIC{shr1ne_gate_unlocked}
```

---

## 🚩 Flag

<details>
<summary>🧠 Click to reveal the flag</summary>

```
LIC{shr1ne_gate_unlocked}
```

</details>

---

## 📚 Key Takeaways

- ROT13 is a **classic beginner CTF cipher**
- Look for hints like:
  - “shift”
  - “rotate”
  - “13”
- Always test simple ciphers before overcomplicating

---

## ⚡ Pro Tips

When dealing with weird readable-but-not-readable text:

1. ROT13  
2. Caesar Cipher (shift variations)  
3. Substitution ciphers  
4. Frequency analysis (for harder ones)

---

## 🏁 Conclusion

This challenge highlights a key CTF habit:

> **Start simple before going complex**

ROT13 is often used as a quick obfuscation layer — easy to miss if you overthink.

---

⭐ *Another solid beginner-friendly crypto challenge!*