Name: Constructor
files : ./chall
Flag format: idek{...}

This challenge, named "Constructor," is an excellent exercise in reverse engineering a Linux binary. The solution lies in understanding a simple encryption function and extracting data directly from the binary.

1. Initial Reconnaissance
After extracting the archive, the first step is to analyze the provided chall file.

Binary Properties
The file and checksec commands give us crucial information:

$ file chall
chall: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, stripped

$ checksec chall
[*] '/path/to/attachments/chall'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)

Analysis:

ELF 64-bit, statically linked: All necessary libraries are included in the binary itself. This is often simpler for analysis as there are no external dependencies to manage.

stripped: Function names and debugging symbols have been removed, which will make the analysis a bit more difficult.

No PIE: The executable is not Position-Independent. It will always be loaded at the same base address (0x400000), which simplifies tracking memory addresses.

No canary: No protection against stack overflows, although this is not relevant for this challenge.

Searching for Strings
A quick search for the strings "Correct" or "Wrong" is often a good starting point.

$ strings chall | grep -iE 'correct|wrong'
Correct!
Wrong!

The presence of these strings confirms that there is a comparison between user input and an expected value. Our goal is to find this expected value.

2. Reverse Engineering with Ghidra
We open the binary in Ghidra. By searching for the string "Correct!", we land directly in the function that validates the flag. Ghidra names it FUN_00401050.

Here is the decompiled pseudo-code of the verification logic:

// Pseudo-code for function FUN_00401050
undefined8 FUN_00401050(void)
{
  // ... (initialization) ...

  // Main decryption and comparison loop
  uVar3 = 0;
  do {
    bVar1 = (&DAT_00403040)[uVar3] ^ bVar6;
    bVar6 = bVar6 + 0x1f;
    local_48[uVar3] = bVar1 ^ (byte)(uVar3 >> 1) ^ 0x5a;
    uVar3 = uVar3 + 1;
  } while (uVar3 != 0x2a);

  // ... (comparison with user input) ...
}

3. Analysis of the Decryption Algorithm
The core of the challenge lies in the do-while loop. This loop reads 42 bytes (0x2a in hexadecimal) from address 0x403040, decrypts them, and stores them in a local variable (local_48) before comparing them to the user's input.

The decryption algorithm for each byte c at index i is as follows:

The encrypted byte is XORed with an incrementing key (bVar6).

The result is XORed with the index i shifted one bit to the right (i >> 1).

The final result is XORed with the constant 0x5a.

To find the flag, we just need to reverse this logic.

4. Data Extraction and Decryption
Dumping the Encrypted Data
We extract the 42 encrypted bytes from address 0x403040 (offset 0x3040 in the file).

$ xxd -s 0x3040 -l 42 -g 1 chall
00003040: 33 21 00 6d 5f ab 86 b4 d4 2d 36 3a 4e 90 8c e3
00003050: cc 2e 09 6c 49 b8 8f f7 cc 22 4e 4d 5e b8 80 cb
00003060: d3 da 20 29 70 02 b7 d1 b7 c4

Decryption Script
The following Python script implements the reversed decryption algorithm to reveal the flag. check script.py

5. Conclusion
This challenge was a simple but effective introduction to reverse engineering "stripped" binaries. By combining static analysis with strings and dynamic analysis with Ghidra, we were able to identify, understand, and reverse a simple encryption algorithm to recover the flag.

Final Flag: idek{he4rd_0f_constructors?_now_you_d1d!!}