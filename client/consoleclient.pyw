import socket
import threading

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(message.decode())
            else:
                break
        except:
            break

# Main client setup
def start_client():
    host = '127.0.0.1'  # Server address
    port = 12345         # Port to connect to

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Start a thread to listen for incoming messages
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    # Send messages to the server
    while True:
        message = input("You: ")
        if message:
            client_socket.send(message.encode())

if __name__ == "__main__":
    start_client()
