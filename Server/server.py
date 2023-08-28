import os
import socket
import threading

myIP = socket.gethostbyname(socket.gethostname())
myPort = 9007
ADDRESS = (myIP, myPort)
buffer = 1024
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)
server.listen()
print("Server running.")

conn, address = server.accept()
while True:
    messageFromClient = conn.recv(buffer).decode(FORMAT)

    # to list all the files present in the directory
    if messageFromClient == "listallfiles":
        names = os.listdir()
        files = ' '.join(names)
        conn.send(files.encode(FORMAT))

    # to exit the application
    elif messageFromClient == "exit":
        conn.send("exit application".encode(FORMAT))
        server.close()
        break

    # to download the files
    else:
        inputValue = messageFromClient.split()
        inputValue_name = inputValue[1]
        # for all files
        if inputValue_name == "all":
            UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            UDPPort = 1035
            UDPAddress = (myIP, UDPPort)
            names = os.listdir()
            names.remove('server.py')
            names.remove('.idea')
            files = ' '.join(names)
            conn.send(files.encode(FORMAT))
            for file_name in names:
                file = open(file_name, "r")
                data = file.read(buffer)
                UDPSocket.sendto(str.encode(data), UDPAddress)
                file.close()
                import time
                time.sleep(0.05)
            UDPSocket.close()

    # for file.txt
        else:
            file = open(inputValue_name, "r")
            data = file.read(buffer)
            udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpPort = 1035
            udpAddress = (myIP, udpPort)
            udpSocket.sendto(str.encode(data), udpAddress)
            file.close()
            udpSocket.close()
