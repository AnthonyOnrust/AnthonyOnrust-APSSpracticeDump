import socket
import threading

HEADER = 64
FORMAT = 'utf-8'
PORT = 5052 #higher value should make current use of this port unlikely
SERVER = socket.gethostbyname(socket.gethostname()) #this device ip
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "ENDING SESSION"

# AF_INET is for IPv4 address family.
# SOCK_STREAM is for TCP connection.
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# assigns socket location with any local ip address
serversocket.bind(ADDR)

# for each thread instance this code runs, thus clients do not hold up eachother
def handle_client(connection, address):
    print(f"{address} connection began")

    connected = True
    while connected:

        # as we need to know defined no. of bytes for message we use header to provide
        # that info first.
        message_len = connection.recv(HEADER).decode(FORMAT)

        # ensure header is legit before taking paylaod
        if message_len:
            message_len = int(message_len)

            # using now known payload length from header take in message content
            message = connection.recv(message_len).decode(FORMAT)

            # waiting for client to command ending socket on server side
            if message == DISCONNECT_MESSAGE:
                connected = False
            print(f"{address} says: {message}")

    # kills socket
    connection.close()
    print(f"{address} closed connection")

def start():
    serversocket.listen() #ready for connection
    while True:

        # wait for connection to provide us socket object and its address
        print("listening...")
        connection, address = serversocket.accept() 

        print("CONNECTION FOUND")

        # thread object made to run handle_client 
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()

# main
print(f" --- {SERVER} server began --- ")
start()