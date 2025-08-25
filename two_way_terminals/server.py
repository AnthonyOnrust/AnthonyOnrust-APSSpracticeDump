import socket
import threading
import time

HEADER = 1024
FORMAT = 'utf-8'
PORT1 = 5052 #higher value should make current use of this port unlikely
THISHOST = socket.gethostbyname(socket.gethostname()) #this device ip
ADDR1 = (THISHOST, PORT1)

SERVER_MESSAGE = "\nHello \nThis is server speaking \nOver \n"

# AF_INET is for IPv4 address family.
# SOCK_STREAM is for TCP connection.
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# assigns socket location with any local ip address
serversocket.bind(ADDR1)

def send(connection, message):

    # user input is put into utf-8
    message = message.encode(FORMAT)

    # take payload length to use as header for initial receive by server so it can prepare for full payload
    message_length = len(message)

    # put payload into utf-8
    length_to_send = str(message_length).encode(FORMAT)

    # blank spaces added to end of data such that header is of defined size.
    length_to_send += b' ' * (HEADER - len(length_to_send))

    connection.send(length_to_send)
    connection.send(message)



# for each thread instance this code runs, thus clients do not hold up eachother
def receive(connection, address):
    print(f"@ ({address}) CONNECTION FOUND! \n")

    while True:

        # as we need to know defined no. of bytes for message we use header to provide
        # that info first.
        message_len = connection.recv(HEADER).decode(FORMAT)

        # ensure header is legit before taking paylaod
        if message_len:
            message_len = int(message_len)

            # using now known payload length from header take in message content
            receive_message = connection.recv(message_len).decode(FORMAT)

            print(f"\r{receive_message}\nEnter message: ", end="")

            # this session is open forever

def start():
    serversocket.listen() #ready for connection
    while True:

        # wait for connection to provide us socket object and its address
        print("listening... Also you can type below:")

        connection, address = serversocket.accept() 

        break

    # thread object made to run to receive
    thread_rx = threading.Thread(target=receive, args=(connection, address))
    thread_rx.start()

    while True:
        msg = input("Enter message: ")

        thread_tx = threading.Thread(target=send, args=(connection,"Received: " + msg))
        thread_tx.start()




# main
print(f" --- ({THISHOST}) SERVER BEGAN --- \n")
start()