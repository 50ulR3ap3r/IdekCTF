This document details the solution to the "Constructor" binary challenge. The binary validates a password using a simple, custom encryption scheme. The solution lies in reversing this algorithm and applying it to an encrypted data block found within the binary itself.

Step 1: Initial Reconnaissance
The first step is to understand the nature of the binary.

File Analysis
The file and checksec commands provide a baseline understanding of the executable.

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

Statically Linked & Stripped: All necessary code is in the file, but function names are removed, requiring manual analysis to understand the program flow.

No PIE: The binary loads at a fixed address (0x400000), which makes referencing memory locations straightforward during analysis.

Searching for Strings
A quick search for keywords often reveals the program's intent.

$ strings chall | grep -iE 'correct|wrong'
Correct!
Wrong!

The presence of these strings confirms a simple validation mechanism. Our goal is to find the data it's comparing against.

Step 2: Static Analysis with Ghidra
Opening the binary in a decompiler like Ghidra allows us to inspect its internal logic. By searching for references to the "Correct!" string, we immediately find the validation function, which Ghidra labels FUN_00401050.

The core logic of this function is a loop that decrypts and compares data:

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

Step 3: Vulnerability and Strategy
The vulnerability is the simplicity of the encryption scheme. The program reads 42 bytes (0x2a) from address 0x403040, decrypts them, and compares the result to the user's input. The algorithm is a series of XOR operations, which are easily reversible.

Our strategy is therefore:

Extract the encrypted data block from the binary at address 0x403040.

Re-implement the decryption logic in a script.

Run the script on the extracted data to reveal the flag.

Step 4: Extraction and Decryption
Dumping the Encrypted Data
We use xxd to dump the 42 bytes of encrypted data directly from the file, starting at offset 0x3040.

$ xxd -s 0x3040 -l 42 -g 1 chall
00003040: 33 21 00 6d 5f ab 86 b4 d4 2d 36 3a 4e 90 8c e3
00003050: cc 2e 09 6c 49 b8 8f f7 cc 22 4e 4d 5e b8 80 cb
00003060: d3 da 20 29 70 02 b7 d1 b7 c4

Decryption Script
This process is automated using a Python script that precisely reverses the operations seen in Ghidra. See script.py for the complete implementation.

Step 5: Retrieving the Flag
Running the decryption script on the extracted byte array reveals the flag.

Flag: idek{he4rd_0f_constructors?_now_you_d1d!!}
