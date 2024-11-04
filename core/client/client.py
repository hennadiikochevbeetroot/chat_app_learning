import os
import socket
import threading


class ChatClient:
    def __init__(self, nickname: str):
        self.nickname = nickname
        self.client_socket = self._get_socket()

    def _get_socket(self) -> socket.socket:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host, port = os.getenv('CHAT_HOST'), int(os.getenv('CHAT_PORT', 5555))
        client_socket.connect((host, port))
        return client_socket

    def send_message(self):
        while True:
            message = input('>> ')
            formatted_message = f'{self.nickname}: {message}'
            self.client_socket.send(formatted_message.encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message == 'NICKNAME':
                    self.client_socket.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:  # WHen server stops / connection is broken
                print('Error occured!')
                self.client_socket.close()
                break

    def start(self):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
        send_thread = threading.Thread(target=self.send_message)
        send_thread.start()


def run_client():
    nickname = input("Enter your nickname: ")
    chat_client = ChatClient(nickname)
    chat_client.start()
