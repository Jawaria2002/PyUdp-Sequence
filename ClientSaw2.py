import socket
import os
import struct
import time

def send_file_SAW(filename, server_address):
    print(f"Sending file '{filename}' to {server_address}...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)

    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        client_socket.close()
        return

    with open(filename, 'rb') as file:
        file_data = file.read()
        seq_num = 0
        expected_ack = 0
        sent_data = {}
        while seq_num < len(file_data):
            data = file_data[seq_num:seq_num + 1024]
            header = struct.pack("!II", seq_num, len(data))
            client_socket.sendto(header + data, server_address)
            sent_data[seq_num] = data
            print(f"Packet {seq_num} sent.")
            seq_num += 1024

        while expected_ack < seq_num:
            try:
                ack, _ = client_socket.recvfrom(1024)
                ack = struct.unpack("!I", ack)[0]
                print(f"Received ACK for packet {ack}.")
                if ack in sent_data:
                    del sent_data[ack]
                    expected_ack = ack + 1024
            except socket.timeout:
                for seq, data in sent_data.items():
                    header = struct.pack("!II", seq, len(data))
                    client_socket.sendto(header + data, server_address)
                    print(f"Packet {seq} resent.")
                time.sleep(1)

        print(f"File '{filename}' sent to {server_address}.")
    client_socket.close()

if __name__ == '__main__':
    server_address = ('localhost', 4445)  # Server address and port
    filename = "DataSent.txt"  # Hard-coded file name to send
    start = time.time()
    send_file_SAW(filename, server_address)
    end = time.time()
    print("Time taken to send the file: ", end - start)
