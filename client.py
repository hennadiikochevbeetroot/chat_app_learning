import socket
import threading

# Client settings
HOST = '127.0.0.1'  # Server IP address
PORT = 5555  # Server port

# Create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            print("An error occurred! Exiting...")
            client_socket.close()
            break


# Function to send messages to the server
def send_messages():
    while True:
        message = input("")
        client_socket.send(message.encode())


# Start receiving and sending threads
threading.Thread(target=receive_messages).start()
threading.Thread(target=send_messages).start()
