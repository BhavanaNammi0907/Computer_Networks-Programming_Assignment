import socket

myIP = socket.gethostbyname(socket.gethostname())
myPort = 9007
address = (myIP, myPort)
buffer = 1024
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address)

while True:
    yourInput = input("Enter your command :")
    client.send(yourInput.encode(FORMAT))

    # to list all the files coming from the server directory
    if yourInput == "listallfiles":
        messageFromServer = client.recv(buffer).decode(FORMAT)
        allFileNames = messageFromServer
        allFileNames = allFileNames.split()
        print(allFileNames)

    # to exit the application
    elif yourInput == "exit":
        messageFromServer = client.recv(buffer).decode(FORMAT)
        print("Exiting")
        client.close()
        break

    # to download the files
    else:
        inputValue = yourInput.split()
        inputValue_name = inputValue[1]
        # for all files
        if inputValue_name == 'all':
            messageFromServer = client.recv(buffer).decode(FORMAT)
            fileNames = messageFromServer
            fileList = fileNames.split()
            UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            UDPPort = 1035
            UDPAddress = (myIP, UDPPort)
            UDPSocket.bind(UDPAddress)
            for file_name in fileList:
                file = open(file_name, "wb")
                fileAddressPair = UDPSocket.recvfrom(buffer)
                fileInbytes = fileAddressPair[0]
                file.write(fileInbytes)
                file.close()
            print("Downloaded " + messageFromServer)

        # for file.txt
        else:
            UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            UDPPort = 1035
            udpAddress = (myIP, UDPPort)
            UDPSocket.bind(udpAddress)
            file = open(inputValue_name, "wb")
            fileAddressPair = UDPSocket.recvfrom(buffer)
            fileInbytes = fileAddressPair[0]
            file.write(fileInbytes)
            print("Downloaded " + inputValue_name)
            file.close()
