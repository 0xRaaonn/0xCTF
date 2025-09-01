#!/usr/bin/env python3

cipher = [69, 68, 69, 87, 73, 124, 98, 115, 121, 96, 103, 102, 117, 121, 97, 120, 107, 107, 96, 116, 108, 96, 110, 113, 118, 106, 117, 117, 105, 126]

# CBCTF{ should be: 67, 66, 67, 84, 70, 123
expected_start = [67, 66, 67, 84, 70, 123]

print("Cipher values:", cipher[:6])
print("Expected:    ", expected_start)
print("Differences: ", [c - e for c, e in zip(cipher[:6], expected_start)])

# Calculate the actual shifts needed
shifts_needed = [c - e for c, e in zip(cipher[:6], expected_start)]
print("Shifts needed:", shifts_needed)

# Apply these shifts to see if pattern emerges
print("\nTrying calculated shifts:")
decoded = []
for i, (val, shift) in enumerate(zip(cipher, shifts_needed + [shifts_needed[-1]] * (len(cipher) - 6))):
    decoded_char = val - shift
    decoded.append(chr(decoded_char))

result = ''.join(decoded)
print("Result:", result)

# The pattern might be: 2, 2, 2, 3, 3, 1, then uniform
# Let's try this based on the description
print("\nTrying pattern interpretation:")
print("'The first one is simple' - maybe shift 2")  
print("'Then its shifted further' - maybe increases")
print("'But after that its uniform' - constant shift")

# Try: 2, 2, 2, 3, 3, 1, then uniform shift
for uniform in range(1, 10):
    pattern = [2, 2, 2, 3, 3, 1] + [uniform] * (len(cipher) - 6)
    decoded = []
    valid = True
    
    for val, shift in zip(cipher, pattern):
        decoded_char = val - shift
        if 32 <= decoded_char <= 126:
            decoded.append(chr(decoded_char))
        else:
            valid = False
            break
    
    if valid:
        result = ''.join(decoded)
        if 'CBCTF' in result:
            print(f"Pattern {pattern[:6]}+{uniform}: {result}")