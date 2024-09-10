import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 10000)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
total_size , Caddress = sock.recvfrom(4096)

print('Total size of file {} will be received from {}'.format(total_size, Caddress))
# Receive the data in small chunks and write it to a file
received_data = b''
next_seq = 0
while True:
    data, address = sock.recvfrom(5210)
    if received_data == total_size:
        break
    else:
        seq, chunk = data
        seq = int(seq)
        if seq == next_seq:
            received_data += chunk
            next_seq += 1
            ack = str(next_seq).encode('utf-8')
            sock.sendto(ack, address)
            print('Sent ACK {}'.format(next_seq))
        else:
            ack = str(next_seq).encode('utf-8')
            sock.sendto(ack, address)
            print('Sent ACK {}'.format(next_seq))

# Clean up the socket
sock.close()

with open('DataReceived.txt', 'wb') as f:
    f.write(received_data)