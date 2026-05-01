# 🧩 Lost in Translation (50 pts)

> 🗼 A simple but classic encoding challenge — don’t overthink it.

---

## 📌 Challenge Description

You've been chatting with your Japanese pen pal, Sakura, about your upcoming trip to Tokyo. She just sent you the meeting point for tomorrow, but the message looks… strange.

It seems like it was copied from some kind of encoded system.

```
TElDe3czbGNvbWVfdG9famFwYW59
```

---

## 🧠 Initial Thoughts

- The string contains:
  - Uppercase + lowercase letters
  - Numbers
- Hint mentions **“64 characters”**

👉 This strongly suggests **Base64 encoding**

---

## 🔍 Analysis & Approach

Base64 is a common encoding scheme used to represent binary data in ASCII format.

### Why Base64?
- Uses a 64-character set
- Often seen in CTFs for quick obfuscation
- Matches the hint exactly

---

## 🛠️ Solution

### Method 1: CyberChef
1. Open CyberChef
2. Paste the encoded string
3. Apply: `From Base64`

---

### Method 2: Python

```python
import base64

encoded = "TElDe3czbGNvbWVfdG9famFwYW59"
decoded = base64.b64decode(encoded).decode()

print(decoded)
```

---

## 🧾 Decoded Output

```
LIC{w3lcome_to_japan}
```

---

## 🚩 Flag

<details>
<summary>🧠 Click to reveal the flag</summary>

```
LIC{w3lcome_to_japan}
```

</details>

---

## 📚 Key Takeaways

- Always pay attention to hints — they often directly point to the method  
- Base64 is one of the most common encodings in beginner CTFs  
- Tools like CyberChef can speed up your workflow significantly  

---

## ⚡ Pro Tips

When you see suspicious encoded text, try this order:

1. Base64  
2. Hex  
3. URL Encoding  
4. XOR / Custom Encoding  

---

## 🏁 Conclusion

This challenge reinforces a fundamental CTF skill:

> **Recognizing encoding patterns quickly**

Once identified, the solution becomes straightforward.

---

⭐ *Good warm-up challenge — perfect for beginners getting into CTFs!*