Our agents intercepted an encrypted file from a suspicious communication channel.

Intelligence suggests the file uses XOR encryption with a repeating key. The key is believed to be 4 bytes long.

We also know the document contains a flag in the standard format: DECCTF{...}

Can you recover the original message?

Hint: If you know part of the plaintext, you can recover part of the key...

Flag Format: DECCTF{...}
View Hint

XOR is reversible: if C = P XOR K, then P = C XOR K and K = P XOR C. You know the flag starts with 'DECCTF{' - what does that XOR to?
View Hint

XOR is reversible: if C = P XOR K, then P = C XOR K and K = P XOR C. You know the flag starts with 'DECCTF{' - what does that XOR to?
View Hint

XOR is reversible: if C = P XOR K, then P = C XOR K and K = P XOR C. You know the flag starts with 'DECCTF{' - what does that XOR to?
View Hint

Take the first 4 bytes of the ciphertext and XOR them with 'DECC' (first 4 bytes of known plaintext). This gives you the 4-byte key!
View Hint

Take the first 4 bytes of the ciphertext and XOR them with 'DECC' (first 4 bytes of known plaintext). This gives you the 4-byte key!
View Hint

Take the first 4 bytes of the ciphertext and XOR them with 'DECC' (first 4 bytes of known plaintext). This gives you the 4-byte key!
View Hint

The key is 4 ASCII characters. Once you find it, XOR the entire ciphertext with the repeating key to decrypt the full message.
View Hint

The key is 4 ASCII characters. Once you find it, XOR the entire ciphertext with the repeating key to decrypt the full message.
View Hint

The key is 4 ASCII characters. Once you find it, XOR the entire ciphertext with the repeating key to decrypt the full message.
