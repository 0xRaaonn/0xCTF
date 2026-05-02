# 🧩 Sumimasen, Is This Your Phone? (100 pts)

> 📱 “Sometimes deleted doesn’t mean gone…”

---

## 📌 Challenge Description

You find a lost smartphone on a train. The phone is unlocked, and you decide to investigate to identify the owner and return it.

Artifacts found:
- Deleted files (recycle bin)
- Browser history

Goal:
> Reconstruct the identity + location + secret code to form the flag

Format:
```
LIC{firstname_lastname_location_code}
```

---

## 🧠 Initial Thoughts

This is a **digital forensics + OSINT-style challenge**:
- Recover deleted data
- Correlate with browsing activity
- Extract meaningful identifiers

---

## 🔍 Analysis & Approach

---

### 🧩 Step 1: Identify Owner Name

From recovered deleted files:

- Passport metadata:
  > Owner name **"Yuki Tanaka"** :contentReference[oaicite:0]{index=0}  

- Browser history confirmation:
  - Instagram profile: `yuki.tanaka.1215` :contentReference[oaicite:1]{index=1}  

👉 Final name:
```
yuki_tanaka
```

---

### 🧩 Step 2: Identify Location

From multiple artifacts:

- Travel diary:
  > “visited the hot springs near Hakone…” :contentReference[oaicite:2]{index=2}  

- Browser history:
  - Hakone Onsen website  
  - Google Maps → Hakone Shrine :contentReference[oaicite:3]{index=3}  

👉 Repeated location:
```
hakone
```

---

### 🧩 Step 3: Extract Secret Code

From deleted files:

- Recovered hint:
  ```
  3ph45e_h0t_5pring_v1s1t_c0d3
  ```
  :contentReference[oaicite:4]{index=4}  

👉 Only the **core secret code** is required (first segment):

```
3ph45e
```

---

## 🧾 Final Reconstruction

- Name → `yuki_tanaka`  
- Location → `hakone`  
- Code → `3ph45e`  

---

## 🚩 Flag

<details>
<summary>🧠 Click to reveal the flag</summary>

```
LIC{yuki_tanaka_hakone_3ph45e}
```

</details>

---

## 📚 Key Takeaways

- Deleted files still expose sensitive data  
- Not all extracted data is needed — **filter relevant parts**  
- Correlation across:
  - Filesystem artifacts  
  - Browser history  

---

## ⚡ Pro Tips

1. Don’t blindly copy full strings — interpret them  
2. Identify patterns (codes vs descriptions)  
3. Focus on what fits the **flag format hint**  

---

## 🏁 Conclusion

This challenge reinforces:

> **Good analysis isn’t just finding data — it’s knowing what matters**

---

⭐ *A strong forensics + correlation challenge!*