import base64

def decode_multiple_base64(encoded_string):
    """
    Repeatedly decode Base64 until we get a string that starts with 'AICTF'
    or until we can't decode anymore
    """
    current = encoded_string
    layer = 0
    
    print(f"Original: {current}")
    print("-" * 50)
    
    while True:
        try:
            # Attempt to decode Base64
            decoded_bytes = base64.b64decode(current)
            decoded_string = decoded_bytes.decode('utf-8')
            
            layer += 1
            print(f"Layer {layer}: {decoded_string}")
            
            # Check if we found the flag
            if decoded_string.startswith('AICTF'):
                print("-" * 50)
                print(f"🎉 FLAG FOUND: {decoded_string}")
                return decoded_string
            
            # Continue with the decoded result
            current = decoded_string
            
        except Exception as e:
            print(f"Could not decode further. Error: {e}")
            print(f"Final result after {layer} layers: {current}")
            break
    
    return current

# The original encoded message
original_message = "VmxaYVYyTXhTa2RYYTFwWVlXMVNWbFZzVm1GWlZsWnpWMnQwVjFKdFpETlVNVlpyVjFVeFIxZHNRbFpXUlVVeFZXeGFUMVpyTlZaaFJ6RldWa1JCTlE9PQ=="

# Decode the message
result = decode_multiple_base64(original_message)