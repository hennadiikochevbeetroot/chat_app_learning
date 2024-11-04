import os
import socket
import threading

from dotenv import load_dotenv

from .handle_client import handle_client

load_dotenv()


def get_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = os.getenv('CHAT_HOST'), os.getenv('CHAT_PORT')
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f'Chat Server listening on {host}:{port}...')
    return server_socket


def run_server():
    server_socket = get_server_socket()
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
