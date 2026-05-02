# 🧩 Boarding Pass Check (50 pts)

> ✈️ “Check everything carefully before you board.”

---

## 📌 Challenge Description

You're at the airport, about to board your flight to Tokyo Narita. The gate agent reminds you to carefully check your boarding pass.

Something seems… off.

---

## 🖼️ Provided Artifact

A boarding pass image containing flight and passenger details.

---

## 🧠 Initial Thoughts

- This is likely a **steganography / visual inspection challenge**
- No encoding given explicitly
- Hints suggest:
  - Check **every detail**
  - Focus on **small text / reference numbers**

👉 This means the flag is likely **hidden in plain sight**

---

## 🔍 Analysis & Approach

Carefully reviewing the boarding pass:

### Key Fields Observed:
- Passenger Name: DAYANG / SITI  
- Route: BWN → NRT  
- Flight: SA 1042  
- Seat: 22A  
- Gate: B7  

All of these look normal.

---

### 🚨 Suspicious Field

**Booking Reference:**
```
LIC{h4ppy_b0arding}
```

👉 This is NOT a normal booking reference format

- Real booking references are usually:
  - 6–8 characters
  - Alphanumeric (e.g., AB12CD)
- This clearly follows **CTF flag format**

---

## 🧾 Finding

The flag is directly embedded in the boarding pass under:
> **Booking Reference**

---

## 🚩 Flag

<details>
<summary>🧠 Click to reveal the flag</summary>

```
LIC{h4ppy_b0arding}
```

</details>

---

## 📚 Key Takeaways

- Not all challenges require decoding — sometimes it's **pure observation**
- Always inspect:
  - Metadata
  - Labels
  - Reference fields
  - “Normal-looking” values

---

## ⚡ Pro Tips

For similar challenges:

1. Zoom into images carefully  
2. Check all labels and small text  
3. Look for anything that breaks “real-world logic”  
4. Flags are often hidden in:
   - Booking refs
   - IDs
   - Filenames
   - Barcodes (advanced)

---

## 🏁 Conclusion

This challenge reinforces an important CTF skill:

> **Attention to detail beats overcomplication**

No decoding needed — just sharp observation.

---

⭐ *A classic “hidden in plain sight” challenge — easy to miss if you rush!*