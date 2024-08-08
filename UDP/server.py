import socket
import json
import threading
import random
import time

# Load questions from JSON file
with open('question.json') as f:
    questions = json.load(f)

# Shuffle questions
random.shuffle(questions)

client_states = {}
clients = {}

def handle_client(message, addr, server_socket):
    client_data = clients[addr]

    if client_states[addr]['state'] == 'greeting':
        # Handle greeting state
        server_socket.sendto("Welcome to the quiz game!".encode(), addr)
        client_states[addr]['state'] = 'playing'

    elif client_states[addr]['state'] == 'playing':
        # Handle playing state
        if client_data['correct_answers'] == 7:
            server_socket.sendto("Congratulations! You have answered all the questions correctly! 🎉".encode(), addr)
            time.sleep(0.4)
            # win_num = 7
            # server_socket.sendto(win_num, addr)
            
            client_data['current_question_index'] = 0
            client_data['correct_answers'] = 0
            client_states[addr]['state'] = 'greeting'
            # server_socket.close()
            # continue

        question = questions[client_data['current_question_index']]
        question_text = question['question']
        options = question['options']

        if message == "GET_QUESTION":
            question_message = f"{question_text}\n" \
                               f"A: {options['A']}\n" \
                               f"B: {options['B']}\n" \
                               f"C: {options['C']}\n" \
                               f"D: {options['D']}\n"
            server_socket.sendto(question_message.encode(), addr)
        else:
            answer = message.upper()
            print(f"Client picked answer: {answer}")

            if answer == question['answer']:
                server_socket.sendto(b'Correct! Moving to the next question.\n', addr)
                client_data['correct_answers'] += 1
                client_data['current_question_index'] += 1
                client_data['attempts'] = 0  # Reset attempts
            else:
                client_data['attempts'] += 1
                # time.sleep(.6)
                print(f"Wrong answer. Attempt {client_data['attempts']} of 3.")
                if client_data['attempts'] == 3:
                    server_socket.sendto(b'You have exceeded the maximum number of attempts. Disconnecting.\n', addr)
                    # time.sleep(.6)
                    del clients[addr]
                    del client_states[addr]
                else:
                    server_socket.sendto(b'Incorrect. Try again.\n', addr)

            print(f"Questions answered correctly: {client_data['correct_answers']}")
            print(f"Wrong attempts: {client_data['attempts']}")
            print(f"{client_data['current_question_index']} is the current question index")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12347)
    server_socket.bind(server_address)
    print("Server started and listening on port 12347.")

    while True:
        message, client_address = server_socket.recvfrom(1024)
        message = message.decode().strip()

        if client_address not in clients:
            clients[client_address] = {'current_question_index': 0, 'attempts': 0, 'correct_answers': 0}
            client_states[client_address] = {'state': 'greeting', 'point': 0}
            client_thread = threading.Thread(target=handle_client, args=(message, client_address, server_socket))
            client_thread.start()
        else:
            client_thread = threading.Thread(target=handle_client, args=(message, client_address, server_socket))
            client_thread.start()

if __name__ == "__main__":
    thread = threading.Thread(target=start_server)
    thread.start()
