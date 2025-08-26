import socket
import threading
from pynput import keyboard

HEADER = 64
FORMAT = 'utf-8'
PORT1 = 5052 #higher value should make current use of this port unlikely
THISHOST = socket.gethostbyname(socket.gethostname()) #this device ip
ADDR1 = (THISHOST, PORT1)

server_message = ""

# AF_INET is for IPv4 address family.
# SOCK_STREAM is for TCP connection.
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# assigns socket location with any local ip address
serversocket.bind(ADDR1)

server_message = str("Type here:")

def on_press(key):
    global server_message
    if (str(key).replace("'", "") == "Key.enter"):
        server_message = str(server_message) + "\n"
        print(server_message, end="\r")
        server_message = "Type here:"
        print(server_message, end="\r")

    elif (str(key).replace("'", "") == "Key.space"):
        server_message = str(server_message) + " "
        print(server_message, end="\r")

    elif (str(key).replace("'", "")).isalnum():
        server_message = str(server_message) + str(key).replace("'", "")
        print(server_message, end="\r")
    pass

def on_release():
    pass

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
        print("listening... Only type in alphanumeric:")

        connection, address = serversocket.accept() 

        break

    # thread object made to run to receive
    thread_rx = threading.Thread(target=receive, args=(connection, address))
    thread_rx.start()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while True:

        thread_tx = threading.Thread(target=send, args=(server_message,))
        thread_tx.start()


# main
print(f" --- ({THISHOST}) SERVER BEGAN --- \n")
start()