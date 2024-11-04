import os
import socket
import threading

from dotenv import load_dotenv

from .handle_client import handle_client

load_dotenv()


def get_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host, port = os.getenv('CHAT_HOST'), int(os.getenv('CHAT_PORT', 12345))
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f'Chat Server listening on {host}:{port}...')
    return server_socket


def server_loop(server_socket: socket.socket):
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
        except OSError:
            break

def run_server():
    server_socket = get_server_socket()

    server_thread = threading.Thread(target=server_loop, args=(server_socket, ))
    server_thread.start()

    running = True
    while running:
        command = input('Enter `exit` to stop server: ')
        if command.strip().lower() == 'exit':
            running = False

    print('Stopping server...')
    server_socket.close()
    server_thread.join()
    print('Server shutdown complete!')
