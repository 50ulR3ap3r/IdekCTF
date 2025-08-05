````markdown
# 🛠️ Constructor - Reverse Engineering Challenge
**Platform**: Linux (x86-64)  
**Flag format**: `idek{...}`  
**Challenge file**: `./chall`

---

## 🧩 Description

This challenge, named **"Constructor"**, is a great exercise in reverse engineering a statically linked and stripped Linux binary. The goal is to understand a simple decryption function and extract the flag hidden directly within the binary.

---

## 🔍 1. Initial Reconnaissance

After extracting the archive, we begin by inspecting the binary:

```bash
$ file chall
chall: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, stripped

$ checksec chall
[*] '/path/to/attachments/chall'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
````

### 🧠 Observations

* **Statically linked**: No external dependencies.
* **Stripped**: No symbols, harder analysis.
* **No PIE**: Predictable memory layout (base address = `0x400000`).
* **No stack canary**: Not relevant here.

---

## 🔎 2. Searching for Strings

```bash
$ strings chall | grep -iE 'correct|wrong'
Correct!
Wrong!
```

We find two important strings used for feedback. These are likely part of the input validation function.

---

## ⚙️ 3. Reverse Engineering with Ghidra

We open the binary in **Ghidra** and locate the function containing `"Correct!"`. Ghidra names it `FUN_00401050`.

### 📄 Decompiled Pseudo-code

```c
undefined8 FUN_00401050(void)
{
  // ... initialization ...

  // Decryption loop
  uVar3 = 0;
  do {
    bVar1 = (&DAT_00403040)[uVar3] ^ bVar6;
    bVar6 = bVar6 + 0x1f;
    local_48[uVar3] = bVar1 ^ (byte)(uVar3 >> 1) ^ 0x5a;
    uVar3 = uVar3 + 1;
  } while (uVar3 != 0x2a);

  // ... comparison with user input ...
}
```

---

## 🔐 4. Understanding the Decryption Algorithm

### 🔁 For each byte at index `i`:

1. Read encrypted byte from address `0x403040`.
2. XOR with incrementing value `bVar6`, starting from an unknown seed.
3. XOR the result with `(i >> 1)`.
4. XOR with constant `0x5a`.

The decrypted value is then compared against the user input.

---

## 📥 5. Dumping the Encrypted Data

We extract the 42 encrypted bytes directly from the binary:

```bash
$ xxd -s 0x3040 -l 42 -g 1 chall
00003040: 33 21 00 6d 5f ab 86 b4 d4 2d 36 3a 4e 90 8c e3
00003050: cc 2e 09 6c 49 b8 8f f7 cc 22 4e 4d 5e b8 80 cb
00003060: d3 da 20 29 70 02 b7 d1 b7 c4
```

---

## ✅ 6. Final Flag

```
idek{he4rd_0f_constructors?_now_you_d1d!!}
```

---

## 🧠 7. Conclusion

* We used `strings` for initial clues.
* Ghidra helped us find and understand the decryption logic.
* Manual data extraction and a Python script allowed us to recover the flag.

This challenge provided a clean introduction to analyzing **stripped, statically linked, non-PIE binaries** and understanding basic obfuscation techniques.

---
