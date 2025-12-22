import random
import socket
import threading

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

def handle_client(packet, client2_socket):
    """Client1'den gelen paketi işler ve Client2'ye iletir"""
    try:
        parts = packet.split("|")
        if len(parts) == 3:
            data, method, control = parts
            should_corrupt = random.random() < 0.75

            if should_corrupt:
                corrupted, corruption_method = corrupt_data(data)
                new_packet = f"{corrupted}|{method}|{control}|{corruption_method}"
                print(f"[SERVER] Veri bozuldu: {corruption_method}")
            else:
                new_packet = f"{data}|{method}|{control}|BOZULMADI"
                print(f"[SERVER] Veri bozulmadı")

            client2_socket.settimeout(10.0)
            try:
                client2_conn, addr2 = client2_socket.accept()
                print(f"[SERVER] Client 2 bağlandı: {addr2}")
                client2_conn.send(new_packet.encode())
                client2_conn.close()
                print(f"[SERVER] Client 2'ye paket gönderildi")
            except socket.timeout:
                print("[SERVER] HATA: Client 2 bağlanmadı (timeout)")
            except Exception as e:
                print(f"[SERVER] HATA: Client 2 bağlantı hatası: {e}")
        else:
            print(f"[SERVER] HATA: Geçersiz paket formatı: {packet}")
    except Exception as e:
        print(f"[SERVER] HATA: Paket işleme hatası: {e}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 5000))
    server.listen(5)
    print("[SERVER] 5000 portunda başlatıldı (Client1 için)")

    client2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client2_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client2_socket.bind(('localhost', 5001))
    client2_socket.listen(5)
    print("[SERVER] 5001 portu dinleniyor (Client2 için)")
    print("[SERVER] Hazır! İstekleri bekliyorum...\n")

    while True:
        try:
            client1_conn, addr = server.accept()
            print(f"[SERVER] Client 1 bağlandı: {addr}")

            packet = client1_conn.recv(4096).decode()
            client1_conn.close()

            if packet:
                print(f"[SERVER] Paket alındı: {packet[:50]}...")
                thread = threading.Thread(
                    target=handle_client,
                    args=(packet, client2_socket),
                    daemon=True
                )
                thread.start()
            else:
                print("[SERVER] UYARI: Boş paket alındı")

        except KeyboardInterrupt:
            print("\n[SERVER] Kapatılıyor...")
            break
        except Exception as e:
            print(f"[SERVER] HATA: {e}")

if __name__ == "__main__":
    start_server()