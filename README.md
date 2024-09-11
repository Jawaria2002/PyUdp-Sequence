# PyUdp-Sequence


File Transfer Protocol Using UDP
Project Overview
This project demonstrates a simple file transfer protocol using UDP (User Datagram Protocol). It includes both client and server scripts for sending and receiving files, and showcases basic functionality for file transfer reliability and handling.

Project Name
UDP File Transfer Protocol

File Descriptions
ClientSaw2.py: This script is a client application that sends a file over UDP. It uses sequence numbers and acknowledgments to ensure data integrity.

ClientSawGui.py: This is a GUI version of the client application. It allows users to select a file through a graphical interface and send it over UDP.

serverGBN4.py: This script acts as a server that receives files sent over UDP using a basic Go-Back-N protocol for handling packet loss and acknowledgments.

serverSaw2.py: Another server script that handles the reception of files over UDP. It manages packet sequence and acknowledgments for reliable file transfer.

Run the Scripts

To start the server:
python serverSaw2.py


To send the file to client:
python ClientSaw2.py
