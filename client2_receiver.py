def calculate_parity(data, even=True):
    result = []
    for char in data:
        ones = bin(ord(char)).count('1')
        if even:
            parity = '0' if ones % 2 == 0 else '1'
        else:
            parity = '1' if ones % 2 == 0 else '0'
        result.append(parity)
    return ''.join(result)

def calculate_2d_parity(data):
    binary_data = ''.join(format(ord(c), '08b') for c in data)
    rows = []
    for i in range(0, len(binary_data), 8):
        row = binary_data[i:i+8].ljust(8, '0')
        rows.append(row)
    
    row_parities = [str(row.count('1') % 2) for row in rows]
    col_parities = []
    for col in range(8):
        col_sum = sum(int(row[col]) for row in rows if col < len(row))
        col_parities.append(str(col_sum % 2))
    
    return ''.join(row_parities) + ''.join(col_parities)

def calculate_crc16(data):
    polynomial = 0x1021
    crc = 0xFFFF
    for char in data:
        crc ^= (ord(char) << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc = crc << 1
            crc &= 0xFFFF
    return format(crc, '04X')

def calculate_hamming(data):
    result = []
    for char in data:
        bits = format(ord(char), '08b')
        for i in range(0, 8, 4):
            d = [int(b) for b in bits[i:i+4].ljust(4, '0')]
            p1 = d[0] ^ d[1] ^ d[2]
            p2 = d[0] ^ d[1] ^ d[3]
            p3 = d[1] ^ d[2] ^ d[3]
            result.append(f"{p1}{p2}{d[0]}{p3}{d[1]}{d[2]}{d[3]}")
    return ''.join(result)

def calculate_checksum(data):
    total = 0
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            word = (ord(data[i]) << 8) + ord(data[i + 1])
        else:
            word = ord(data[i]) << 8
        total += word
        while total >> 16:
            total = (total & 0xFFFF) + (total >> 16)
    return format(~total & 0xFFFF, '04X')

def get_control_info(data, method):
    if method == "PARITY_EVEN":
        return calculate_parity(data, True)
    elif method == "PARITY_ODD":
        return calculate_parity(data, False)
    elif method == "2D_PARITY":
        return calculate_2d_parity(data)
    elif method == "CRC16":
        return calculate_crc16(data)
    elif method == "HAMMING":
        return calculate_hamming(data)
    elif method == "CHECKSUM":
        return calculate_checksum(data)

def receive_from_server():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 5001))
    packet = s.recv(4096).decode()
    s.close()
    return packet