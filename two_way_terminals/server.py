import socket
import threading
import time

import msvcrt
import ctypes


HEADER = 64
FORMAT = 'utf-8'
PORT1 = 5052 #higher value should make current use of this port unlikely
THISHOST = socket.gethostbyname(socket.gethostname()) #this device ip
ADDR1 = (THISHOST, PORT1)



# AF_INET is for IPv4 address family.
# SOCK_STREAM is for TCP connection.
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# assigns socket location with any local ip address
serversocket.bind(ADDR1)

server_message = str("Server: ")
print(server_message)

connection_list = []

console_handle = ctypes.windll.kernel32.GetStdHandle(-10)
ctypes.windll.kernel32.SetConsoleMode(console_handle, 0)

#server_message = msvcrt.getch().decode()



def send(connection, message):

    # user input is put into utf-8
    message = message.encode(FORMAT)
    #print(f"utf-8 message: {message}.")

    # take payload length to use as header for initial receive by server so it can prepare for full payload
    message_length = len(message)
    #print(f"message length int: {message_length}.")

    # put payload into utf-8
    length_to_send = str(message_length).encode(FORMAT)
    #print(f"message length str: {length_to_send}.")

    # blank spaces added to end of data such that header is of defined size.
    length_to_send += b' ' * (HEADER - len(length_to_send))
    #print(f"message length ready: {length_to_send}.")

    connection.send(length_to_send)
    connection.send(message)



# for each thread instance this code runs, thus clients do not hold up eachother
def receive(connection, client_count):

    while True:

        # as we need to know defined no. of bytes for message we use header to provide
        # that info first.
        message_len = connection.recv(HEADER).decode(FORMAT)

        # ensure header is legit before taking paylaod
        if message_len:
            message_len = int(message_len)

            # using now known payload length from header take in message content
            receive_message = connection.recv(message_len).decode(FORMAT)

            clear_message = " " * len(server_message)
            print(f"\r{str(clear_message)}", end="")
            print(f"\rClient{client_count}: {receive_message}", end="")
            print(f"\r{server_message}", end ="")

            # this session is open forever

def handle_client(connection, address, client_count):
    global server_message
    global connection_list
    # thread object made to run to receive
    thread_rx = threading.Thread(target=receive, args=(connection, client_count))
    thread_rx.start()

    while True:
        new_char = msvcrt.getch()

        # new line
        if (new_char == b'\r'):
            print(f"\r{server_message}", end="")
            for connection_element in connection_list:

                thread_tx = threading.Thread(target=send, args=(connection_element, server_message + "\n"))
                thread_tx.start()
            print(f"\r{server_message}\n", end="")
            server_message = str("Server: ")
        # backspaces remove characters
        elif (new_char == b'\x08'):
            if (server_message != "Server: "):
                server_message = server_message[:-1]
                print(f"\r{server_message}" + " ", end="")
            else:
                print(f"\r{server_message}", end="")
        # hopefully alphanumeric
        else:
            server_message = server_message + new_char.decode()

        print(f"\r{server_message}", end="")


def start():
    serversocket.listen() #ready for connection
    print("listening...")
    client_count = 0

    while True:

        # wait for connection to provide us socket object and its address
        connection, address = serversocket.accept() 
        client_count += 1
        connection_list.append(connection)

        clear_message = " " * len(server_message)
        print(f"\r{str(clear_message)}", end="")
        print(f"\r@({address}) connected, going by alias: client{client_count}")
        thread_rx = threading.Thread(target=handle_client, args=(connection, address, client_count))
        thread_rx.start()


# main
print(f" --- ({THISHOST}) SERVER BEGAN --- \n")
start()