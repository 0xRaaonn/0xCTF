#!/usr/bin/env python3
"""
XOR Binary Analysis and Key Recovery Tool
Advanced tool for analyzing XOR-encrypted binaries and recovering encryption keys
"""

import os
import sys
import string
from collections import Counter
from itertools import cycle
import argparse

class XORAnalyzer:
    def __init__(self, binary_data):
        self.data = binary_data
        self.printable_chars = set(string.printable.encode())
        
    def single_byte_xor_decrypt(self, data, key):
        """Decrypt data using single-byte XOR key"""
        return bytes([b ^ key for b in data])
    
    def multi_byte_xor_decrypt(self, data, key):
        """Decrypt data using multi-byte XOR key"""
        key_cycle = cycle(key)
        return bytes([b ^ next(key_cycle) for b in data])
    
    def calculate_score(self, decrypted_data):
        """Score decrypted data based on English text characteristics"""
        if not decrypted_data:
            return 0
            
        # Count printable characters
        printable_count = sum(1 for b in decrypted_data if b in self.printable_chars)
        printable_ratio = printable_count / len(decrypted_data)
        
        # English letter frequency analysis
        english_freq = {
            b'e': 12.7, b't': 9.1, b'a': 8.2, b'o': 7.5, b'i': 7.0, b'n': 6.7,
            b's': 6.3, b'h': 6.1, b'r': 6.0, b'd': 4.3, b'l': 4.0, b'c': 2.8,
            b'u': 2.8, b'm': 2.4, b'w': 2.4, b'f': 2.2, b'g': 2.0, b'y': 2.0,
            b'p': 1.9, b'b': 1.3, b'v': 1.0, b'k': 0.8, b'j': 0.15, b'x': 0.15,
            b'q': 0.10, b'z': 0.07
        }
        
        # Calculate frequency score
        text_lower = decrypted_data.lower()
        freq_score = 0
        for char_byte, expected_freq in english_freq.items():
            actual_count = text_lower.count(char_byte[0])
            actual_freq = (actual_count / len(decrypted_data)) * 100
            freq_score += abs(expected_freq - actual_freq)
        
        # Look for common English patterns
        common_patterns = [b'the', b'and', b'ing', b'ion', b'tio', b'ent', b'ers']
        pattern_score = sum(decrypted_data.lower().count(pattern) for pattern in common_patterns)
        
        # Combined score (lower is better for freq_score, higher is better for others)
        total_score = (printable_ratio * 100) + pattern_score - (freq_score / 10)
        return total_score
    
    def brute_force_single_byte(self):
        """Brute force single-byte XOR key"""
        best_score = -1
        best_key = None
        best_decryption = None
        results = []
        
        print("[+] Attempting single-byte XOR brute force...")
        
        for key in range(256):
            decrypted = self.single_byte_xor_decrypt(self.data, key)
            score = self.calculate_score(decrypted)
            
            results.append((key, score, decrypted))
            
            if score > best_score:
                best_score = score
                best_key = key
                best_decryption = decrypted
        
        # Sort results by score
        results.sort(key=lambda x: x[1], reverse=True)
        
        print(f"[+] Top 5 single-byte key candidates:")
        for i, (key, score, decrypted) in enumerate(results[:5]):
            preview = decrypted[:50].replace(b'\n', b'\\n').replace(b'\r', b'\\r')
            print(f"    {i+1}. Key: 0x{key:02x} ({chr(key) if 32 <= key <= 126 else '?'}) | Score: {score:.2f}")
            print(f"       Preview: {preview}")
            print()
        
        return best_key, best_decryption, results
    
    def find_repeating_key_length(self, max_length=20):
        """Find likely key length using Index of Coincidence"""
        print("[+] Analyzing for repeating key patterns...")
        
        ic_scores = []
        
        for key_length in range(1, max_length + 1):
            # Split data into groups based on key position
            groups = [[] for _ in range(key_length)]
            
            for i, byte in enumerate(self.data):
                groups[i % key_length].append(byte)
            
            # Calculate average Index of Coincidence
            total_ic = 0
            valid_groups = 0
            
            for group in groups:
                if len(group) > 1:
                    ic = self.calculate_index_of_coincidence(group)
                    total_ic += ic
                    valid_groups += 1
            
            avg_ic = total_ic / valid_groups if valid_groups > 0 else 0
            ic_scores.append((key_length, avg_ic))
        
        # Sort by IC score (higher is better for English text)
        ic_scores.sort(key=lambda x: x[1], reverse=True)
        
        print("[+] Top key length candidates (by Index of Coincidence):")
        for i, (length, ic) in enumerate(ic_scores[:5]):
            print(f"    {i+1}. Length: {length} | IC: {ic:.4f}")
        
        return ic_scores
    
    def calculate_index_of_coincidence(self, data):
        """Calculate Index of Coincidence for frequency analysis"""
        if len(data) <= 1:
            return 0
        
        freq = Counter(data)
        ic = sum(f * (f - 1) for f in freq.values()) / (len(data) * (len(data) - 1))
        return ic
    
    def brute_force_multi_byte(self, key_length):
        """Brute force multi-byte XOR key of given length"""
        print(f"[+] Attempting multi-byte XOR with key length {key_length}...")
        
        # Split data by key position
        groups = [[] for _ in range(key_length)]
        for i, byte in enumerate(self.data):
            groups[i % key_length].append(byte)
        
        # Find best single-byte key for each position
        key_bytes = []
        for i, group in enumerate(groups):
            if not group:
                key_bytes.append(0)
                continue
                
            best_score = -1
            best_key_byte = 0
            
            for key_byte in range(256):
                decrypted_group = [b ^ key_byte for b in group]
                score = self.calculate_score(bytes(decrypted_group))
                
                if score > best_score:
                    best_score = score
                    best_key_byte = key_byte
            
            key_bytes.append(best_key_byte)
            print(f"    Position {i}: 0x{best_key_byte:02x} ({chr(best_key_byte) if 32 <= best_key_byte <= 126 else '?'})")
        
        # Decrypt with found key
        key = bytes(key_bytes)
        decrypted = self.multi_byte_xor_decrypt(self.data, key)
        
        return key, decrypted
    
    def analyze_entropy(self):
        """Analyze data entropy to detect encryption"""
        freq = Counter(self.data)
        entropy = -sum((count/len(self.data)) * 
                      __import__('math').log2(count/len(self.data)) 
                      for count in freq.values())
        
        print(f"[+] Data entropy: {entropy:.4f}")
        print(f"    (0 = not random, 8 = perfectly random)")
        
        if entropy > 7.5:
            print("    High entropy detected - likely encrypted/compressed")
        elif entropy > 6.0:
            print("    Medium entropy - possibly encrypted")
        else:
            print("    Low entropy - likely plaintext or simple encoding")
        
        return entropy
    
    def search_for_patterns(self):
        """Search for common patterns that might indicate the key or flag format"""
        print("[+] Searching for patterns...")
        
        # Look for common flag formats
        flag_patterns = [b'flag{', b'FLAG{', b'ctf{', b'CTF{', b'{', b'}']
        
        for pattern in flag_patterns:
            # Try XORing the pattern with the beginning of data
            if len(self.data) >= len(pattern):
                potential_key = bytes([a ^ b for a, b in zip(self.data[:len(pattern)], pattern)])
                print(f"    If data starts with '{pattern.decode('utf-8', errors='ignore')}', key might be: {potential_key.hex()}")
                
                # Test this potential key
                if len(potential_key) > 0:
                    decrypted = self.multi_byte_xor_decrypt(self.data, potential_key)
                    preview = decrypted[:100].replace(b'\n', b'\\n').replace(b'\r', b'\\r')
                    print(f"      Result: {preview}")
                    print()

def main():
    parser = argparse.ArgumentParser(description='XOR Binary Analysis Tool')
    parser.add_argument('binary_file', help='Path to binary file to analyze')
    parser.add_argument('--max-key-length', type=int, default=20, 
                       help='Maximum key length to test for multi-byte XOR')
    parser.add_argument('--output', '-o', help='Output decrypted data to file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.binary_file):
        print(f"Error: File '{args.binary_file}' not found!")
        sys.exit(1)
    
    # Read binary data
    print(f"[+] Loading binary file: {args.binary_file}")
    with open(args.binary_file, 'rb') as f:
        binary_data = f.read()
    
    print(f"[+] File size: {len(binary_data)} bytes")
    
    # Initialize analyzer
    analyzer = XORAnalyzer(binary_data)
    
    # Analyze entropy
    entropy = analyzer.analyze_entropy()
    print()
    
    # Search for patterns
    analyzer.search_for_patterns()
    
    # Try single-byte XOR
    single_key, single_decrypted, single_results = analyzer.brute_force_single_byte()
    print()
    
    # Find potential key lengths
    key_lengths = analyzer.find_repeating_key_length(args.max_key_length)
    print()
    
    # Try multi-byte XOR with top key lengths
    multi_results = []
    for key_length, ic_score in key_lengths[:3]:  # Try top 3 lengths
        if key_length > 1:  # Skip length 1 as it's covered by single-byte
            try:
                multi_key, multi_decrypted = analyzer.brute_force_multi_byte(key_length)
                score = analyzer.calculate_score(multi_decrypted)
                multi_results.append((key_length, multi_key, multi_decrypted, score))
                
                print(f"[+] Multi-byte key (length {key_length}): {multi_key.hex()}")
                print(f"    Key as string: {multi_key}")
                print(f"    Score: {score:.2f}")
                preview = multi_decrypted[:100].replace(b'\n', b'\\n').replace(b'\r', b'\\r')
                print(f"    Preview: {preview}")
                print()
            except Exception as e:
                print(f"    Error with length {key_length}: {e}")
    
    # Determine best result
    print("[+] ANALYSIS SUMMARY:")
    print("=" * 50)
    
    all_results = []
    
    # Add single-byte result
    single_score = analyzer.calculate_score(single_decrypted)
    all_results.append(('single', single_key, single_decrypted, single_score))
    
    # Add multi-byte results
    for length, key, decrypted, score in multi_results:
        all_results.append(('multi', key, decrypted, score))
    
    # Sort by score
    all_results.sort(key=lambda x: x[3], reverse=True)
    
    if all_results:
        best_type, best_key, best_decrypted, best_score = all_results[0]
        
        print(f"Best result:")
        if best_type == 'single':
            print(f"  Type: Single-byte XOR")
            print(f"  Key: 0x{best_key:02x} ({chr(best_key) if 32 <= best_key <= 126 else '?'})")
        else:
            print(f"  Type: Multi-byte XOR")
            print(f"  Key: {best_key.hex()} ({best_key})")
        
        print(f"  Score: {best_score:.2f}")
        print(f"  Decrypted data preview:")
        preview = best_decrypted[:200].replace(b'\n', b'\\n').replace(b'\r', b'\\r')
        print(f"    {preview}")
        
        if args.output:
            with open(args.output, 'wb') as f:
                f.write(best_decrypted)
            print(f"\n[+] Decrypted data saved to: {args.output}")
        
        # Look for flag patterns in the best result
        flag_indicators = [b'flag{', b'FLAG{', b'ctf{', b'CTF{']
        for indicator in flag_indicators:
            if indicator in best_decrypted.lower():
                print(f"\n[!] POTENTIAL FLAG FOUND!")
                # Extract potential flag
                start = best_decrypted.lower().find(indicator.lower())
                end = best_decrypted.find(b'}', start)
                if end != -1:
                    potential_flag = best_decrypted[start:end+1]
                    print(f"[!] FLAG: {potential_flag}")
                break

if __name__ == "__main__":
    main()