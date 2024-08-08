import socket
import json
import threading
import random


# Load questions from JSON file
with open('question.json') as f:
    questions = json.load(f)

# Shuffle questions
random.shuffle(questions)

client_states = {}

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12347)
    server_socket.bind(server_address)
    print("Server started and listening on port 12348.")

    data, _ = server_socket.recvfrom(1024)
    print(f"Client message: {data} from client {_}")

    snd_2_client = str(input("Message to Client: "))
    server_socket.sendto(snd_2_client.encode(), _)

    clients = {}

    while True:
        message, client_address = server_socket.recvfrom(1024)
        message = message.decode().strip()

        if client_address not in clients:
            clients[client_address] = {'current_question_index': 0, 'attempts': 0, 'correct_answers': 0}

        client_data = clients[client_address]
        if client_data['correct_answers'] >= 7:
            server_socket.sendto("Congratulations! You have answered all the questions correctly! 🎉".encode(), client_address)
            # server_socket.close()
            client_data['current_question_index'] = 0

            continue

        question = questions[client_data['current_question_index']]
        question_text = question['question']
        options = question['options']

        if message == "GET_QUESTION":
            question_message = f"{question_text}\n" \
                               f"A: {options['A']}\n" \
                               f"B: {options['B']}\n" \
                               f"C: {options['C']}\n" \
                               f"D: {options['D']}\n" \
                            #    "Your answer (A/B/C/D): "
            server_socket.sendto(question_message.encode(), client_address)
        else:
            answer = message.upper()
            print(f"Client picked answer: {answer}")

            if answer == question['answer']:
                server_socket.sendto(b'Correct! Moving to the next question.\n', client_address)
                client_data['correct_answers'] += 1
                client_data['current_question_index'] += 1
                client_data['attempts'] = 0  # Reset attempts
            else:
                client_data['attempts'] += 1
                print(f"Wrong answer. Attempt {client_data['attempts']} of 3.")
                if client_data['attempts'] >= 3:
                    server_socket.sendto(b'You have exceeded the maximum number of attempts. Disconnecting.\n', client_address)
                    del clients[client_address]
                else:
                    server_socket.sendto(b'Incorrect. Try again.\n', client_address)

            print(f"Questions answered correctly: {client_data['correct_answers']}")
            print(f"Wrong attempts: {client_data['attempts']}")
            print(f"{client_data['current_question_index']} is the CQI")

if __name__ == "__main__":
    
    thread = threading.Thread(target=start_server)
    thread.start()
    # start_server()


