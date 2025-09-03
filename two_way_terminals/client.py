import socket
import threading
import time

import msvcrt
import ctypes

HEADER = 64
FORMAT = 'utf-8'
PORT1 = 5052
THISHOST = socket.gethostbyname(socket.gethostname()) #this device ip
ADDR1 = (THISHOST, PORT1)

# AF_INET is for IPv4 address family.
# SOCK_STREAM is for TCP connection.
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# assigns socket location with local ip address and selected port
clientsocket.connect(ADDR1)

client_message = str("")
print(f"Client: {client_message}")

console_handle = ctypes.windll.kernel32.GetStdHandle(-10)
ctypes.windll.kernel32.SetConsoleMode(console_handle, 0)

def send(message):

    print(f"\n\rClient: ", end="")

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

            clear_message = " " * len("Client: " + client_message)
            print(f"\r{str(clear_message)}", end="")
            print(f"\r{receive_message}", end ="")
            print(f"\rClient: {client_message}", end ="")
            #print(f"\r{receive_message}\nEnter message: ", end="")


def start():
    global client_message
    # handle sending separate from receiving since if they are run as same thread the receive script will
    # hold up the send script.

    # outside of loop since receive thread doesn't need to handle multiple instances but just one.
    thread_rx = threading.Thread(target=receive, args=())
    thread_rx.start()

    while True:
        new_char = msvcrt.getch()

        # new line
        if (new_char == b'\r'):
            print(f"\rClient: {client_message}", end="")
            thread_tx = threading.Thread(target=send, args=(client_message + "\n",))
            thread_tx.start()
            client_message = str("")
        # backspaces remove characters
        elif (new_char == b'\x08'):
            if (client_message != ""):
                client_message = client_message[:-1]
                print(f"\rClient: {client_message}" + " ", end="")
            else:
                print(f"\rClient: {client_message}", end="")
        # hopefully alphanumeric
        else:
            client_message = client_message + new_char.decode()

        print(f"\rClient: {client_message}", end="")

# main
print(f" --- ({THISHOST}) CLIENT BEGAN --- \n")

start()