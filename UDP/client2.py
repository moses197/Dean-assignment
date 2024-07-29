import socket

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12348)

    while True:
        client_socket.sendto(b'GET_QUESTION', server_address)
        question_message, _ = client_socket.recvfrom(1024)
        print(question_message.decode())

        # if "Your answer (A/B/C/D):" in question_message.decode():
        if "A: " in question_message.decode():
            answer = input("Enter your answer (A/B/C/D): ").strip().upper()
            client_socket.sendto(answer.encode(), server_address)

        response_message, _ = client_socket.recvfrom(1024)
        print(response_message.decode())

        if "Congratulations!" in response_message.decode() or "Disconnecting." in response_message.decode():
            # client_socket.close()
            break

    client_socket.close()

if __name__ == "__main__":
    connect_to_server()
