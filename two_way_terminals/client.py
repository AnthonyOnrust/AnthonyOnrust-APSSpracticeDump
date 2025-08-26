import socket
import threading
import time

HEADER = 64
FORMAT = 'utf-8'
PORT1 = 5052
THISHOST = socket.gethostbyname(socket.gethostname()) #this device ip
ADDR1 = (THISHOST, PORT1)

MESSAGE = "\nHello \nThis is client speaking \nOver \n"

# AF_INET is for IPv4 address family.
# SOCK_STREAM is for TCP connection.
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# assigns socket location with local ip address and selected port
clientsocket.connect(ADDR1)

def send(message):

    # user input is put into utf-8
    message = message.encode(FORMAT)

    # take payload length to use as header for initial receive by server so it can prepare for full payload
    message_length = len(message)

    # put payload length into utf-8
    length_to_send = str(message_length).encode(FORMAT)

    # blank spaces added to end of data such that header is of defined size (of both server/client).
    length_to_send += b' ' * (HEADER - len(length_to_send))

    clientsocket.send(length_to_send)
    clientsocket.send(message)

def receive():

    while True:

        # as we need to know defined no. of bytes for message we use header to provide
        # that info first.
        message_len = clientsocket.recv(HEADER).decode(FORMAT)

        # ensure header is legit before taking paylaod
        if message_len:
            message_len = int(message_len)
            #print(f"length received int: {message_len}.")

            # using now known payload length from header take in message content
            receive_message = clientsocket.recv(message_len).decode(FORMAT)
            #print(f"payload received: {receive_message}.")

            print(f"\r{receive_message}", end ="")
            #print(f"\r{receive_message}\nEnter message: ", end="")


def start():
    # handle sending separate from receiving since if they are run as same thread the receive script will
    # hold up the send script.

    # outside of loop since receive thread doesn't need to handle multiple instances but just one.
    thread_rx = threading.Thread(target=receive, args=())
    thread_rx.start()

    while True:
        msg = input("Enter message: ")

        thread_tx = threading.Thread(target=send, args=("Received: " + msg,))
        thread_tx.start()


# main
print(f" --- ({THISHOST}) CLIENT BEGAN --- \n")

start()