import socket
# import time

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12347)

    init_msg = input("Message to Server: ")
    client_socket.sendto(init_msg.encode(), server_address)

    recv_msg, _ = client_socket.recvfrom(1024)
    print(f"Message from server: {recv_msg.decode()}")
    print("I want to play a game")
    print()

    try:
        while True:
            client_socket.sendto(b'GET_QUESTION', server_address)
            question_message, _ = client_socket.recvfrom(1024)
            question_message = question_message.decode()

            
            if "Congratulations!" in question_message:
                print(f"Yoo....{question_message}")
                break


            print(question_message)

            if "Disconnection." in question_message:
                print("Try again later")
                break

            if "A: " in question_message:
                answer = input("Enter your answer (A/B/C/D): ").strip().upper()
                client_socket.sendto(answer.encode(), server_address)

               

            response_message, _ = client_socket.recvfrom(1024)
            response_message = response_message.decode()

            if "Congratulations!" in response_message:

                print(f"Yoo....{response_message}")

                break

        print("Closing connection")
        client_socket.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        client_socket.close()

if __name__ == "__main__":
    connect_to_server()
