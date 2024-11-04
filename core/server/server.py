import os
import signal
import socket
import threading

from dotenv import load_dotenv

load_dotenv()


class ChatServer:
    def __init__(self) -> None:
        self.clients: list[socket.socket] = []
        self.nicknames: list[str] = []

        self.server_socket = self._get_socket()

    def _get_socket(self) -> socket.socket:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host, port = os.getenv('CHAT_HOST'), int(os.getenv('CHAT_PORT', 5555))
        server_socket.bind((host, port))
        server_socket.listen()
        return server_socket

    def broadcast(self, data: bytes) -> None:
        for client in self.clients:
            client.send(data)

    def handle_client(self, client_socket: socket.socket) -> None:
        while True:
            try:
                data = client_socket.recv(1024)
                self.broadcast(data)
            except:  # Removing clients on their exit
                index = self.clients.index(client_socket)
                nickname = self.nicknames[index]

                self.clients.remove(client_socket)
                client_socket.close()

                self.broadcast(f'User {nickname} quit!'.encode('utf-8'))
                self.nicknames.remove(nickname)
                break

    def _add_new_user_nickname(self, client_socket: socket.socket) -> str:
        client_socket.send('NICKNAME'.encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')
        self.nicknames.append(nickname)
        self.clients.append(client_socket)
        print(f'New User joined with nickname: {nickname}')
        return nickname

    def _thread_handle_client(self, client_socket: socket.socket):
        thread = threading.Thread(target=self.handle_client, args=(client_socket,))
        thread.start()

    def start(self):
        print('Chat Server started...')
        while True:
            client_socket, address = self.server_socket.accept()
            print(f'New Client Connected - {address}')

            nickname = self._add_new_user_nickname(client_socket)

            self.broadcast(f'New User: {nickname} - joined!'.encode('utf-8'))
            client_socket.send('Connected to server successfully!'.encode('utf-8'))

            self._thread_handle_client(client_socket)


def run_server():
    chat_server = ChatServer()
    chat_server.start()
