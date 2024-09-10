import socket
import os
import struct
import time
import tkinter as tk
from tkinter import filedialog

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

def select_file():
    root.filename = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("all files", "*.*"), ("jpeg files", "*.jpg")))
    file_label.config(text=root.filename)

def send_file():
    start = time.time()
    send_file_SAW(root.filename, ('localhost', 4445))
    end = time.time()
    print("Time taken to send the file: ", end - start)

root = tk.Tk()
root.title("File Transfer GUI")

select_file_button = tk.Button(root, text="Select File", command=select_file)
send_file_button = tk.Button(root, text="Send File", command=send_file)
file_label = tk.Label(root, text="No file selected")

select_file_button.pack()
file_label.pack()
send_file_button.pack()

root.mainloop()
