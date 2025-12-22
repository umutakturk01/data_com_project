import random

def bit_flip(data):
    if not data:
        return data, "Bit Çevirme"
    binary_list = [list(format(ord(c), '08b')) for c in data]
    char_idx = random.randint(0, len(binary_list) - 1)
    bit_idx = random.randint(0, 7)
    binary_list[char_idx][bit_idx] = '0' if binary_list[char_idx][bit_idx] == '1' else '1'
    return ''.join(chr(int(''.join(b), 2)) for b in binary_list), "Bit Çevirme"

def char_substitute(data):
    if not data:
        return data, "Karakter Değiştirme"
    idx = random.randint(0, len(data) - 1)
    return data[:idx] + chr(random.randint(65, 90)) + data[idx+1:], "Karakter Değiştirme"

def char_delete(data):
    if len(data) < 2:
        return data, "Karakter Silme"
    idx = random.randint(0, len(data) - 1)
    return data[:idx] + data[idx+1:], "Karakter Silme"

def char_insert(data):
    idx = random.randint(0, len(data))
    return data[:idx] + chr(random.randint(97, 122)) + data[idx:], "Karakter Ekleme"

def char_swap(data):
    if len(data) < 2:
        return data, "Karakter Yer Değiştirme"
    idx = random.randint(0, len(data) - 2)
    return data[:idx] + data[idx+1] + data[idx] + data[idx+2:], "Karakter Yer Değiştirme"

def multiple_bit_flip(data):
    result = data
    for _ in range(random.randint(2, 5)):
        result, _ = bit_flip(result)
    return result, "Çoklu Bit Çevirme"

def burst_error(data):
    if len(data) < 3:
        return data, "Patlama Hatası"
    burst_len = random.randint(3, min(8, len(data)))
    start = random.randint(0, len(data) - burst_len)
    corrupted = list(data)
    for i in range(start, start + burst_len):
        corrupted[i] = chr(random.randint(65, 90))
    return ''.join(corrupted), "Patlama Hatası"

def corrupt_data(data):
    methods = [bit_flip, char_substitute, char_delete, char_insert, char_swap, multiple_bit_flip, burst_error]
    method = random.choice(methods)
    return method(data)