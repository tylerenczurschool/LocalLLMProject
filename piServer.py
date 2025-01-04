import socket
from TTS import say
from inputs import snap_photo
from gpiozero import Button


def start_server(port=12345):

    # Starts the Server
    host = socket.gethostname()
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server started on {host}:{port}")

    # Listens for client
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    # Buttons
    pictureSwitch = Button(23, pull_up=True)
    voiceSwitch = Button (24, pull_up=True)
    button = Button(25, pull_up=True)

    # Checking for Button Press
    while True:
        button.wait_for_active()
        if (pictureSwitch.is_active()):
            image_send(snap_photo(), client_socket)
        if (voiceSwitch.is_active()):
            try:
                client_socket.send("true")
                response = client_socket.recv(1024).decode('utf-8')
                print(f"Received: {response}")
                say(response)
            except ConnectionResetError:
                print ("Connection reset by client")
                break

    # Closes Server
    client_socket.close()
    server_socket.close()

def image_send(image_path, client_socket):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        image_size = len(image_data)
        client_socket.sendall(image_size.to_bytes(4, 'big'))
        client_socket.sendall(image_data)

if __name__ == "__main__":
    start_server()
