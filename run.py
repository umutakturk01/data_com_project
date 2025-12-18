from client1_sender import send_packet
from server_corruptor import process_packet
from client2_receiver import receive_packet

def main():
    packet = send_packet()

    if packet is None:
        return

    corrupted_packet = process_packet(packet)

    if corrupted_packet is None:
        return

    receive_packet(corrupted_packet)

if __name__ == "__main__":
    while True:
        main()
        print("\n")
        again = input("Send another message? (y/n): ")
        if again.lower() != 'y':
            break