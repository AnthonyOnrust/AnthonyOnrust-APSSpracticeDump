import socket

HEADER = 64
FORMAT = 'utf-8'
PORT = 5052 #higher value should make current use of this port unlikely, use terminal to ensure port is not in use.
SERVER = socket.gethostbyname(socket.gethostname()) #this device ip
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "ENDING SESSION"

print("BEGIN CLIENT")

# AF_INET is for IPv4 address family.
# SOCK_STREAM is for TCP connection.
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# assigns socket location with any local ip address
clientsocket.connect(ADDR)
print("CLIENT SOCKET BOUND")

def message(message):

    # user input is put into utf-8
    message = message.encode(FORMAT)

    # take payload length to use as header for intial recieve by server so it can prepare for full payload
    message_length = len(message)

    # put payload into utf-8
    length_to_send = str(message_length).encode(FORMAT)

    # blank spaces added to end of data such that header is of defined size.
    length_to_send += b' ' * (HEADER - len(length_to_send))

    clientsocket.send(length_to_send)
    clientsocket.send(message)


# What is actually run
message("HI")
message(DISCONNECT_MESSAGE)