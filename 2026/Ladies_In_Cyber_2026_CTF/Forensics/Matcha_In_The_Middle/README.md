# 🧩 Matcha in the Middle (100 pts)

> 🍵 “Maybe this wasn't just a receipt after all…”

---

## 📌 Challenge Description

After visiting a small café in Tokyo, you receive a digital receipt image via email. At first glance, it looks like a normal receipt written in Japanese.

But something feels off…

---

## 🧠 Initial Thoughts

The receipt contains a hint:

> **※注意：この画像には秘密があります**  
> **ヒント：メタ**

📌 Translation:
> *Note: This image contains a secret*  
> *Hint: Meta*

👉 This strongly suggests checking **metadata / hidden fields** within the image.

---

## 🔍 Analysis & Approach

### Step 1: Inspect Image Metadata

Used **Aperi'Solve** to analyze the image.

👉 Found hidden data in the **comment section** of the image.

---

### Step 2: Extract Hidden Data

The comment contained the following Base64 string:

```
U2F5b25hcmEhIEZsYWcgaXMgaGlkZGVuIGJlbG93OiBMSUN7bUB0Y2hhX2xAdHRlX21AbHdhcmV9
```

---

### Step 3: Decode Base64

Used **CyberChef** → `From Base64`

Decoded output:

```
Sayonara! Flag is hidden below: LIC{m@tcha_l@tte_m@lware}
```

---

## 🚩 Flag

<details>
<summary>🧠 Click to reveal the flag</summary>

```
LIC{m@tcha_l@tte_m@lware}
```

</details>

---

## 📚 Key Takeaways

- Image files can contain hidden data in:
  - Metadata  
  - Comment fields  
- Hidden data is often **encoded (Base64, Hex, etc.)**
- Always decode extracted content

---

## ⚡ Pro Tips

When solving similar challenges:

1. Check metadata first (`exiftool`, Aperi'Solve)  
2. Look for encoded strings  
3. Decode using:
   - CyberChef  
   - Base64 tools  
4. Only move to advanced stego if nothing found  

---

## 🏁 Conclusion

This challenge reinforces:

> **Hidden data doesn’t mean complex — sometimes it’s just metadata + encoding**

Simple techniques, applied correctly, lead to the solution.

---

⭐ *A great blend of metadata inspection and encoding analysis!*