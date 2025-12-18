import random

def bit_flip(data):
    if not data:
        return data, "Bit Flip"
    binary_list = [list(format(ord(c), '08b')) for c in data]
    char_idx = random.randint(0, len(binary_list) - 1)
    bit_idx = random.randint(0, 7)
    binary_list[char_idx][bit_idx] = '0' if binary_list[char_idx][bit_idx] == '1' else '1'
    return ''.join(chr(int(''.join(b), 2)) for b in binary_list), "Bit Flip"

def char_substitute(data):
    if not data:
        return data, "Character Substitution"
    idx = random.randint(0, len(data) - 1)
    return data[:idx] + chr(random.randint(65, 90)) + data[idx+1:], "Character Substitution"

def char_delete(data):
    if len(data) < 2:
        return data, "Character Deletion"
    idx = random.randint(0, len(data) - 1)
    return data[:idx] + data[idx+1:], "Character Deletion"

def char_insert(data):
    idx = random.randint(0, len(data))
    return data[:idx] + chr(random.randint(97, 122)) + data[idx:], "Character Insertion"

def char_swap(data):
    if len(data) < 2:
        return data, "Character Swapping"
    idx = random.randint(0, len(data) - 2)
    return data[:idx] + data[idx+1] + data[idx] + data[idx+2:], "Character Swapping"

def multiple_bit_flip(data):
    result = data
    for _ in range(random.randint(2, 5)):
        result, _ = bit_flip(result)
    return result, "Multiple Bit Flips"

def burst_error(data):
    if len(data) < 3:
        return data, "Burst Error"
    burst_len = random.randint(3, min(8, len(data)))
    start = random.randint(0, len(data) - burst_len)
    corrupted = list(data)
    for i in range(start, start + burst_len):
        corrupted[i] = chr(random.randint(65, 90))
    return ''.join(corrupted), "Burst Error"

def corrupt_data(data):
    methods = [bit_flip, char_substitute, char_delete, char_insert, char_swap, multiple_bit_flip, burst_error]
    method = random.choice(methods)
    return method(data)

def process_packet(packet):
    parts = packet.split('|')
    if len(parts) != 3:
        print("Invalid packet!")
        return None
    
    data, method, control_info = parts
    
    print("=" * 50)
    print("Server - Received Packet")
    print("=" * 50)
    print("Original Data        :", data)
    print("Method               :", method)
    print("Control Info         :", control_info)
    
    should_corrupt = random.random() < 0.75
    
    if should_corrupt:
        corrupted_data, corruption_method = corrupt_data(data)
        print("Corrupted Data       :", corrupted_data)
        print("Corruption Method    :", corruption_method)
        print("Status               : Error injected")
    else:
        corrupted_data = data
        print("Status               : Data forwarded without corruption")
    
    print("Packet forwarded to Client 2")
    print("=" * 50)
    
    return f"{corrupted_data}|{method}|{control_info}"

if __name__ == "__main__":
    test_packet = "HELLO|CRC16|BB5D"
    process_packet(test_packet)