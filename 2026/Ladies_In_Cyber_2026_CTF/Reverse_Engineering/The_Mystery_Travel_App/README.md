# 🧩 The Mystery Travel App (200 pts)

> 📱 “The app works, but what is it doing in the background?”

---

## 📌 Challenge Description

A suspicious Japanese travel booking app was extracted and decompiled.

The source code contains multiple layers:
- Data definitions
- Obfuscated functions
- Execution flow

Goal:
> Reverse engineer the code and construct the flag manually.

Flag format:

```text
LIC{component_1_component_2_component_3_component_4_component_5}
```

---

## 🧠 Initial Thoughts

This is a **reverse engineering / malware analysis** challenge.

The hints mention that the flag components come from the `UserDataManager` class and are modified through the execution flow.

So the key is to trace:

```text
UserDataManager → collect_user_travel_data() → encode_travel_profile() → main_execution()
```

---

## 🔍 Analysis & Approach

### 🧩 Step 1: Identify Data Definitions

Inside `UserDataManager`, the following values are initialized:

```python
self.travel_destination = "kyoto"
self.visit_purpose = "shrine"
self.visit_type = "visit"
self.collected_data = True
self.exfil_status = "detected"
```

These become the first few flag components.

---

### 🧩 Step 2: Check App Configuration

Inside `TravelAppConfig`:

```python
DATA_COLLECTION = True
UPLOAD_LOCATION = "suspicious-server.xyz/upload"
```

Because `DATA_COLLECTION` is set to `True`, the behavior becomes:

```python
data_stealing
```

---

### 🧩 Step 3: Trace Flag Components

Inside `collect_user_travel_data()`:

```python
component_1 = stolen_destination
component_2 = stolen_purpose
component_3 = stolen_type
component_4 = "data_" + ("stealing" if TravelAppConfig.DATA_COLLECTION else "safe")
component_5 = "_" + ("detected" if manager.exfil_status == "detected" else "hidden")
```

So the components are:

| Component | Value |
|---|---|
| component_1 | `kyoto` |
| component_2 | `shrine` |
| component_3 | `visit` |
| component_4 | `data_stealing` |
| component_5 | `_detected` |

---

## 🧾 Final Reconstruction

Combining the components:

```text
kyoto + shrine + visit + data_stealing + detected
```

Final format:

```text
LIC{kyoto_shrine_visit_data_stealing_detected}
```

---

## 🚩 Flag

<details>
<summary>🧠 Click to reveal the flag</summary>

```text
LIC{kyoto_shrine_visit_data_stealing_detected}
```

</details>

---

## 📚 Key Takeaways

- Decompiled code should be read from top to bottom
- Focus on:
  - Class variables
  - Conditional logic
  - Return values
  - Main execution flow
- Obfuscation may distract from simple hardcoded values

---

## 🏁 Conclusion

This challenge reinforces:

> **Reverse engineering is about tracing data flow.**

The flag was constructed by following how the suspicious app collected, processed, and labelled user travel data.