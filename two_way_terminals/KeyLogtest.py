from pynput import keyboard

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


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

while True:
    pass