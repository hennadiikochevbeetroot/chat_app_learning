import socket


def response_to_clients(data: bytes) -> bytes:
    message = data.decode('utf-8')
    print(f'Received message from User: {message}')
    response = f'User : {message}'
    return response.encode('utf-8')


def handle_client(client_socket: socket.socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        response = response_to_clients(data)
        client_socket.sendall(response)

    client_socket.close()
