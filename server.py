import socket
import threading

# Server settings
HOST = '127.0.0.1'  # Localhost
PORT = 5555  # Port to bind to

# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = {}
aliases = {}


# Broadcast message to all clients
def broadcast(message, sender=None):
    for client in clients.keys():
        client.send(f"{sender if sender else 'Server'}: {message}".encode())


# Handle individual client
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.startswith('/rename'):
                new_alias = message.split(maxsplit=1)[1]
                broadcast(f"{aliases[client_socket]} has changed their name to {new_alias}", "Server")
                aliases[client_socket] = new_alias
            else:
                broadcast(message, aliases[client_socket])
        except:
            client_socket.close()
            broadcast(f"{aliases[client_socket]} has left the chat.", "Server")
            clients.pop(client_socket)
            aliases.pop(client_socket)
            break


# Accept incoming connections
def accept_connections():
    while True:
        client_socket, client_address = server_socket.accept()
        client_socket.send("Welcome! Type /rename <name> to set your alias.".encode())
        clients[client_socket] = client_address
        aliases[client_socket] = f"User{len(clients)}"
        broadcast(f"{aliases[client_socket]} has joined the chat.", "Server")
        threading.Thread(target=handle_client, args=(client_socket,)).start()


print("Server is running...")
accept_connections()
