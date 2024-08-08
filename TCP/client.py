import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    while True:
        message = client_socket.recv(4096).decode()
        if not message:
            break
        print(message, end='')  # Print question and options

        # Read answer from user
        answer = input()
        client_socket.sendall(answer.encode())

    client_socket.close()

if __name__ == "__main__":
    start_client()
