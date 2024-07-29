# import socket

# def start_client():
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect(('127.0.0.1', 12348))
    
#     while True:
#         question = client.recv(4096).decode()
#         if "Game over" in question or "Congratulations" in question:
#             print(question)
#             break
        
#         print(question)
#         answer = input("Your answer (A, B, C, D): ").strip().upper()
#         client.sendall(answer.encode())
    
#     client.close()

# if __name__ == "__main__":
#     start_client()

import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    while True:
        try:
            message = client_socket.recv(4096).decode()
            if not message:
                break
            print(message, end='')  # Print question and options

            # Read answer from user
            answer = input()
            client_socket.sendall(answer.encode())
            
        except ConnectionResetError:
            print("Connection closed by the server.")
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
