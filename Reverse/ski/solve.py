"""
# Author: 50ulR3ap3r
# Statut : solved
# Date: 2025-08-03
"""
import re

PROGRAM_FILE = 'program.txt'
FLAG_BIT_COUNT = 560

ZERO_BIT_FINGERPRINT = '(((S ((S I) (K (K I)))) (K K)) '


def extract_flag_bits_from_source(program_text):
    print("Beginning static analysis with regular expressions...")
    flag_variable_matches = re.finditer(r'_F\d+', program_text)
    
    extracted_bits = []
    
    for match in flag_variable_matches:
        pattern_start_index = match.start() - len(ZERO_BIT_FINGERPRINT)
        
        preceding_text = program_text[pattern_start_index : match.start()]
        
        if preceding_text == ZERO_BIT_FINGERPRINT:
            extracted_bits.append(0)
        else:
            extracted_bits.append(1)
            
    if len(extracted_bits) != FLAG_BIT_COUNT:
        print(f"Warning: Found {len(extracted_bits)} bits, but expected {FLAG_BIT_COUNT}.")
        
    print(f"Analysis complete. Found {len(extracted_bits)} bits.")
    return extracted_bits


def bits_to_ascii(bits):
    byte_strings = [
        "".join(map(str, bits[i:i+8]))
        for i in range(0, len(bits), 8)
    ]
    
    return "".join([chr(int(byte, 2)) for byte in byte_strings])


def main():
    try:
        with open(PROGRAM_FILE, 'r') as f:
            program_content = f.read()
    except FileNotFoundError:
        print(f"[ERROR] Could not find the file: {PROGRAM_FILE}")
        return

    correct_bits = extract_flag_bits_from_source(program_content)
    flag = bits_to_ascii(correct_bits)
    
    print("\n--- Correct Flag Recovered ---")
    print(flag)
    print("------------------------------")


if __name__ == '__main__':
    main()

# flag: idek{d1d_y0u_0pt1m1z3_4nd_s1d3ch4nn3l3d_0r_s0lv3d_1n_7h3_1nt3nd3d_w4y}