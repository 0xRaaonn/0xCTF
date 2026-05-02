# 🧩 What's the Wi-Fi Password? (50 pts)

> 🍵 “Computers seem to love this format…”

---

## 📌 Challenge Description

You arrive at a matcha café in Kyoto and ask for the Wi-Fi password. Instead of a normal password, the board shows:

```
4C 49 43 7B 6D 61 74 63
68 61 5F 6C 61 74 74 65 7D
```

---

## 🧠 Initial Thoughts

- The text is made of:
  - Hexadecimal characters (0–9, A–F)
- Hint mentions:
  - “Each pair represents one letter”

👉 This strongly indicates **Hex → ASCII encoding**

---

## 🔍 Analysis & Approach

### What is Hexadecimal?
- Base-16 number system
- Each **2 hex characters = 1 byte**
- Each byte maps to an ASCII character

Example:
- `41` → A  
- `6D` → m  

---

## 🛠️ Solution

### Method 1: CyberChef
1. Open CyberChef  
2. Paste the hex string  
3. Apply: `From Hex`

---

### Method 2: Python

```python
bytes.fromhex("4C 49 43 7B 6D 61 74 63 68 61 5F 6C 61 74 74 65 7D").decode()
```

---

## 🧾 Decoded Output

```
LIC{matcha_latte}
```

---

## 🚩 Flag

<details>
<summary>🧠 Click to reveal the flag</summary>

```
LIC{matcha_latte}
```

</details>

---

## 📚 Key Takeaways

- Hex encoding is extremely common in CTFs  
- Always group hex in **pairs (bytes)**  
- Easy to decode once recognized  

---

## ⚡ Pro Tips

When you see:
- Pairs of characters (e.g., `4C 49 43`)
- Only 0–9 and A–F  

👉 Try:
1. Hex → ASCII  
2. Base64  
3. Binary  

---

## 🏁 Conclusion

This challenge reinforces:

> **Recognizing encoding formats quickly is key**

Once identified as hex, decoding becomes trivial.

---

⭐ *Another classic beginner-friendly encoding challenge!*