# 3rd Time's The Charm — Crypto Challenge Writeup

## Challenge Description

**Title:** 3rd Time's The Charm

**Description:** The first one is simple. Then its shifted further. But after that its uniform.

### Given Data

```
69 68 69 87 73 124 98 115 121 96 103 102 117 121 97 120 107 107 96 116 108 96 110 113 118 106 117 117 105 126
```

---

## Solution Steps

### Step 1 – Convert numbers to ASCII

Map each decimal to its ASCII character:

```
69 = E, 68 = D, 69 = E, 87 = W, 73 = I, 124 = |,
98 = b, 115 = s, 121 = y, 96 = `, 103 = g, 102 = f,
117 = u, 121 = y, 97 = a, 120 = x, 107 = k, 107 = k,
96 = `, 116 = t, 108 = l, 96 = `, 110 = n, 113 = q,
118 = v, 106 = j, 117 = u, 117 = u, 105 = i, 126 = ~
```

Resulting string:

```
EDEWI|bsy`gfuyaxkk`tl`nqvjuui~
```

> (This matches the hint: **“the first one is simple.”**)

### Step 2 – Shift symbols by −1

Treat symbols as part of the shift and move them back by 1 in ASCII:

* `|` (124) → `{` (123)

* `` ` `` (96) → `_` (95)

* `~` (126) → `}` (125)

Updated string:

```
EDEWI{bsy_gfuyaxkk_tl_nqvjuui}
```

> (This reflects **“then it’s shifted further.”**)

### Step 3 – Group letters in 3s (ignore symbols while grouping)

Remove `{`, `}`, and `_` for grouping/ROT; keep their positions for reinsertion later.

```
Letters only: EDEWIbsygfuyaxkktlnqvjuui
Groups of 3:  EDE | WIb | syg | fuy | axk | ktl | nqv | juu | i
```

### Step 4 – Apply decreasing ROT shifts per group

Apply a Caesar rotation that **decreases by 1** per group, starting at ROT24 (≡ shift −2) and ending at ROT16 (≡ shift −10):

```
EDE → CBC
WIb → TFy
syg → ouc
fuy → apt
axk → ure
ktl → dme
nqv → fin
juu → all
i   → y
```

Concatenate letters:

```
CBCTFyoucapturedmefinally
```

> After the progressive shifts, the message becomes clear and “uniform” plaintext.

### Step 5 – Reinsert the symbols in their original spots

Bring `{`, `}`, and `_` back:

```
CBCTF{you_captured_me_finally}
```

---

## Flag

```
CBCTF{you_captured_me_finally}
```

---

## Identified Vulnerability

A custom, layered Caesar scheme (including symbol shifting and decreasing rotations) obscures plaintext. Such schemes provide **obfuscation**, not cryptographic security.

## Remediation

Use well-vetted cryptography (e.g., AES, libsodium) and avoid bespoke ciphers or ad‑hoc transformations. Keep hints separate from the secret; assume an attacker will discover the algorithm.
