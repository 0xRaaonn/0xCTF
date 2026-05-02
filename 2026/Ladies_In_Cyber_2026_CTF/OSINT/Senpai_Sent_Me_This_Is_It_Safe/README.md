# 🧩 Senpai Sent Me This... Is It Safe? (100 pts)

> 📸 “Something feels off…”

---

## 📌 Challenge Description

You meet a friendly local (“Senpai”) in Tokyo who later sends you a message with a photo and social media handle.

You feel suspicious and decide to investigate further before interacting.

Goal:
> Identify who “Senpai” really is and uncover the hidden flag

---

## 🧠 Initial Thoughts

This looks like a **social engineering + OSINT + web investigation challenge**:

- Clues from chat/message
- Social media pivot
- Website analysis
- Hidden content discovery

---

## 🔍 Analysis & Approach

---

### 🧩 Step 1: Extract Username from Chat

From the message:

```
@tokyo_senpaixo
```

👉 This is the key pivot point (OSINT entry)

---

### 🧩 Step 2: Investigate Social Media

Visited the Instagram profile:

```
@tokyo_senpaixo
```

👉 Found a link in bio:

```
https://tokyo-senpaixo.github.io/lic-gallery/
```

(with tracking parameters like `utm_source=ig`, etc.)

---

### 🧩 Step 3: Analyze the Website

Opened the site and inspected it.

👉 Next step:
- **View Page Source**

---

### 🧩 Step 4: Hidden Clue in Source Code

Found a comment:

```html
<!-- 次はここ → /hidden.html -->
```

📌 Translation:
> “Next is here → /hidden.html”

---

### 🧩 Step 5: Discover Hidden Page

Navigated to:

```
https://tokyo-senpaixo.github.io/lic-gallery/hidden.html
```

---

### 🚨 Key Finding

The hidden page contains:

```html
<h1>LIC{senpai_is_not_so_safe}</h1>
```

---

## 🚩 Flag

<details>
<summary>🧠 Click to reveal the flag</summary>

```
LIC{senpai_is_not_so_safe}
```

</details>

---

## 📚 Key Takeaways

- Social media can be used as an **attack vector / entry point**
- Always pivot from:
  - Usernames
  - Profiles
  - Links in bio  
- Websites often hide clues in:
  - Source code  
  - Comments  
  - Hidden endpoints  

---

## ⚡ Pro Tips

When solving similar challenges:

1. Extract all identifiers (usernames, links)  
2. Pivot across platforms (IG → website)  
3. Always:
   - View page source  
   - Look for comments  
4. Try common hidden paths:
   - `/hidden`
   - `/admin`
   - `/backup`

---

## 🏁 Conclusion

This challenge reinforces:

> **Think like an attacker — follow the trail of digital breadcrumbs**

From a simple chat message →  
to social media →  
to hidden web content.

---

⭐ *Great OSINT + web exploitation style challenge!*