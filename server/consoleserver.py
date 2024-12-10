import socket
import threading

# List to keep track of connected clients
clients = []

# Broadcast message to all clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

# Handle client messages
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Received message: {message.decode()}")
                broadcast(message, client_socket)
            else:
                break
        except:
            break

    # Remove the client from the list and close the connection
    clients.remove(client_socket)
    client_socket.close()

# Main server setup
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = '172.16.0.41'  # Localhost
    port = 12345         # Port to bind to

    server.bind((host, port))
    server.listen(5)

    print(f"Server started on {host}:{port}")
    print("Waiting for clients to connect...")

    while True:
        client_socket, client_address = server.accept()
        print(f"Connection from {client_address} established.")
        clients.append(client_socket)

        # Start a new thread to handle the client
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
