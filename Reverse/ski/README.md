**Category**: Reverse Engineering / Esoteric Languages  
**Flag format**: `idek{...}`  
**Files provided**:
- `program.txt`
- `interpreter.py`
- `interpreter.cpp`

---

## 🧠 Description

This fascinating challenge merges **esoteric programming** with classic reverse engineering.  
Instead of a binary, we are given a massive SKI combinator expression — a form of **combinatory logic** known for its simplicity and obfuscation.

---

## 📦 1. Initial Reconnaissance

The challenge provides three files:
```
- `**interpreter.py**`: A slow but readable Python implementation of a SKI interpreter.
- `**interpreter.cpp**`: A faster, optimized version in C++.
- `**program.txt**`: A huge, single-line SKI expression containing the verification logic.
```
---

## 🔍 2. Understanding the Interpreter

By analyzing `interpreter.py`, we learned how the system processes the input:

### 🧮 Flag Conversion

- The program prompts the user for a flag.
- It encodes the flag into **560 bits**, meaning the flag must be **70 ASCII characters** long.
- Each **bit** is turned into a SKI boolean:
  ```
  - `1` → `K`  (equivalent to **True**)
  - `0` → `(K I)` (equivalent to **False**)
  ```

### 🧠 Logic of the Program

- The main expression in `program.txt` consumes these 560 variables:
  ```
  - `_F0`, `_F1`, ..., `_F559`
  ```
- The expression is reduced step-by-step using SKI rules.
- If the final result is `K` (i.e., **True**), the input is considered valid.

---

## 🚫 3. Why Not Run It?

The challenge specifically warns that running either interpreter is **too slow** due to the size of the program. Brute-force or full evaluation is not viable.

This hinted that the solution lies elsewhere — not in execution, but in **static analysis**.

---

## ✨ 4. The "Aha!" Moment

The key insight:

> If each bit is checked one by one, the source must contain **repeating code patterns** that correspond to either a `0` or `1` check.

By identifying these patterns, we can **read the solution directly from the source** without executing anything.

---

## 🧬 5. Pattern Discovery

### 🔎 Observations

Upon searching `program.txt` near each `_Fi`, we noticed a **recurring structure**:

```
(((S ((S I) (K (K I)))) (K K))
````

This SKI pattern corresponds to a boolean test for **False** → `(K I)`.

### 💡 Hypothesis

* If this pattern appears **before** a variable `_Fi`, then bit `i` of the flag is expected to be `0`.
* Otherwise (if different), it's expecting a `1`.
  
---

## 🏁 6. Final Flag

```
idek{d1d_y0u_0pt1m1z3_4nd_s1d3ch4nn3l3d_0r_s0lv3d_1n_7h3_1nt3nd3d_w4y}
```

---

## ✅ 8. Conclusion

This challenge was a brilliant example of:

* **Esoteric logic** (SKI calculus)
* **Static reverse engineering**
* **Pattern recognition**
* Avoiding brute force in favor of smart observation

Rather than evaluating 560 combinator applications, we used **textual fingerprints** to extract the answer efficiently and as intended by the challenge author.

---
