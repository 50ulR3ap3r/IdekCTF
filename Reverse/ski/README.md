Name: SKI
files : program.txt ; interpreter.py ; interpreter.cpp
Flag format: idek{...}


This was a fascinating challenge that combined esoteric programming languages with classic reverse engineering techniques. Instead of a typical binary, we were given a program written in SKI combinator calculus, a system famous for its power and extreme obfuscation.

This write-up details the more direct method: solving it the "intended way" through static analysis.

1. Initial Reconnaissance
The challenge provided three files:

interpreter.py: A slow but readable Python implementation of a SKI interpreter.

interpreter.cpp: A fast, optimized C++ version of the interpreter.

program.txt: A massive, single-line SKI expression that constitutes the core logic.

Analyzing the readable interpreter.py revealed the program's core mechanics:

Input Processing: The program prompts for a flag, which it converts into a 560-bit sequence (implying a 70-character ASCII flag).

SKI Booleans: Each bit of the input is translated into a specific SKI expression that functions as a boolean value:

A 1 bit becomes the combinator K (True).

A 0 bit becomes the application (K I) (False).

Program Logic: The enormous expression in program.txt is a function that sequentially consumes each of the 560 flag-derived boolean variables (_F0, _F1, ..., _F559).

Win Condition: The flag is correct if, and only if, the entire expression evaluates to the single combinator K (True) after all reductions. Any other result signifies failure.

The challenge description explicitly warns that running the interpreters is too resource-intensive. This was a clear signal that brute-force or direct execution was a dead end. We needed a shortcut.

2. The "Aha!" Moment: From Dynamic to Static Analysis
An initial thought was a side-channel attack. We could feed the program bits one by one and observe some property of the resulting expression, like its complexity or evaluation time. A wrong bit would likely cause the expression to collapse into a simple "False" state, while the correct bit would yield another complex expression, ready for the next input.

However, a closer look at program.txt suggested a far more elegant solution. If the program checks each bit sequentially, it must contain a repeating structural pattern—a piece of code for "check bit i". It stood to reason that the code to check for a 0 would be textually different from the code to check for a 1.

If we could find a unique textual "fingerprint" for one of these checks, we could solve the puzzle without ever running the interpreter.

3. The Intended Way: Static Pattern Matching
By examining the text of program.txt around the flag variables (_F0, _F1, _F2, etc.), a clear and repeating pattern emerged. One specific sequence of combinators consistently appeared immediately before some of the flag variables.

This fingerprint is: (((S ((S I) (K (K I)))) (K K)) 

This sequence is the SKI implementation of a function that effectively checks if its argument is (K I) (False).

This led to our core hypothesis: If this pattern appears immediately before a flag variable _Fi, the program expects the i-th bit of the flag to be 0. If any other pattern appears, the program must be expecting a 1.

This simple, powerful insight allows us to bypass the complex SKI evaluation entirely. We can simply "read" the correct bits from the source file itself.

4. The Solver Script
The following Python script implements this static analysis strategy. It uses a regular expression to robustly find each flag variable in the correct order and then checks the text immediately preceding it for our "zero-bit" fingerprint.

check solve.py

5. Conclusion
This challenge was a masterful example of how a problem that appears computationally impossible can be solved with a simple, elegant observation. By stepping back from the complex mechanics of SKI evaluation and instead analyzing the static structure of the code, we found the intended shortcut.

Final Flag: idek{d1d_y0u_0pt1m1z3_4nd_s1d3ch4nn3l3d_0r_s0lv3d_1n_7h3_1nt3nd3d_w4y}