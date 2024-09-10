import socket
import struct
import time

def receive_file_SAW(server_socket):
    total_packets = 0
    received_packets = 0
    lost_packets = 0

    data, address = server_socket.recvfrom(2048)
    seq_num, data_len = struct.unpack("!II", data[:8])
    data = data[8:]
    expected_seq = seq_num
    filename = "DataReceived.txt"  # Hard-coded file name to save
    with open(filename, 'wb') as file:
        while data_len == 1024:
            total_packets += 1
            if seq_num == expected_seq:
                file.write(data)
                expected_seq += 1024
                ack = struct.pack("!I", seq_num)
                server_socket.sendto(ack, address)
                print(f"ACK for packet {seq_num} sent.")
                received_packets += 1
                data, address = server_socket.recvfrom(2048)
                seq_num, data_len = struct.unpack("!II", data[:8])
                data = data[8:]
            else:
                ack = struct.pack("!I", expected_seq - 1024)
                server_socket.sendto(ack, address)
                print(f"Duplicate packet {seq_num} received. ACK for packet {expected_seq - 1024} sent.")
                lost_packets += 1
                data, address = server_socket.recvfrom(2048)
                seq_num, data_len = struct.unpack("!II", data[:8])
                data = data[8:]
        file.write(data)
        ack = struct.pack("!I", seq_num)
        server_socket.sendto(ack, address)
        print(f"ACK for packet {seq_num} sent.")
        received_packets += 1
        print(f"File '{filename}' received from {address}.")
    print(f"Total packets received: {received_packets}")
    print(f"Total packets lost: {lost_packets}")

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 4445))  # Bind server to localhost and port 4445
    print("\n Server started at localhost & port 4445")
    print("_____Waiting for client to connect..._____")
    start = time.time()
    receive_file_SAW(server_socket)
    end = time.time()
    print(f"File received in {end - start} seconds.")
    server_socket.close()
