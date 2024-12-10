import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

# Function to receive messages from the server
def receive_messages(client_socket, text_area):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                text_area.insert(tk.END, f"Friend: {message.decode()}\n")
                text_area.yview(tk.END)  # Auto scroll to the bottom
            else:
                break
        except:
            break

# Function to send messages to the server
def send_message(client_socket, message_entry, text_area, username):
    message = message_entry.get()
    if message:
        formatted_message = f"{username}: {message}"
        client_socket.send(formatted_message.encode())
        text_area.insert(tk.END, f"You: {message}\n")
        text_area.yview(tk.END)  # Auto scroll to the bottom
    message_entry.delete(0, tk.END)  # Clear the input field

# Function to ask for server details and username
def get_server_details():
    # Open an initial window to enter server details and username
    root = tk.Tk()
    root.title("Enter Server Details")

    # Server address label and input field
    tk.Label(root, text="Server Address (e.g., 127.0.0.1):").pack(padx=10, pady=5)
    server_entry = tk.Entry(root, width=40)
    server_entry.pack(padx=10, pady=5)

    # Port number label and input field
    tk.Label(root, text="Port (default 12345):").pack(padx=10, pady=5)
    port_entry = tk.Entry(root, width=40)
    port_entry.pack(padx=10, pady=5)
    port_entry.insert(0, "12345")  # Default port

    # Username label and input field
    tk.Label(root, text="Enter Your Username:").pack(padx=10, pady=5)
    username_entry = tk.Entry(root, width=40)
    username_entry.pack(padx=10, pady=5)

    # Function to handle when the "Connect" button is clicked
    def on_connect():
        server_address = server_entry.get()
        port = int(port_entry.get())
        username = username_entry.get()
        if server_address and username:
            root.destroy()  # Close the entry window
            start_client(server_address, port, username)

    # Connect button
    connect_button = tk.Button(root, text="Connect", command=on_connect)
    connect_button.pack(padx=10, pady=10)

    # Start the initial window
    root.mainloop()

# Main client setup
def start_client(server_address, port, username):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, port))

    # Set up the tkinter UI for the main chat window
    root = tk.Tk()
    root.title("Chat Client")

    # Create the scrollable text area for displaying chat messages
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
    text_area.pack(padx=10, pady=10)
    text_area.config(state=tk.DISABLED)  # Make it non-editable

    # Create the input field for entering messages
    message_entry = tk.Entry(root, width=40)
    message_entry.pack(padx=10, pady=10, side=tk.LEFT)

    # Create the send button
    send_button = tk.Button(root, text="Send", width=10, command=lambda: send_message(client_socket, message_entry, text_area, username))
    send_button.pack(padx=10, pady=10, side=tk.LEFT)

    # Start a thread to receive messages
    threading.Thread(target=receive_messages, args=(client_socket, text_area), daemon=True).start()

    # Run the tkinter UI loop
    root.mainloop()

if __name__ == "__main__":
    get_server_details()
