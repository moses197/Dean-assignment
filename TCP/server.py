# import socket
# import json
# import random

# # Load the questions from the JSON file
# with open('questions.json', 'r') as file:
#     questions = json.load(file)

# def get_random_question():
#     return random.choice(questions)

# def handle_client(client_socket):
#     trials = 3
#     correct_answers = 0
#     question_count = 0

#     while question_count < 10 and correct_answers < 10:
#         question = get_random_question()
#         question_count += 1
        
#         question_text = question['question']
#         options = question['options']
#         answer = question['answer']

#         # Send question to client
#         client_socket.sendall(f"{question_text}\nA: {options['A']}\nB: {options['B']}\nC: {options['C']}\nD: {options['D']}\n".encode())

#         while trials > 0:
#             response = client_socket.recv(1024).decode().strip().upper()
#             if response == answer:
#                 correct_answers += 1
#                 client_socket.sendall("Correct! Moving to the next question...\n".encode())
#                 break
#             else:
#                 trials -= 1
#                 if trials > 0:
#                     client_socket.sendall(f"Wrong answer. You have {trials} trials left.\n".encode())
#                 else:
#                     client_socket.sendall("You've exhausted your trials. Game over.\n".encode())
#                     client_socket.close()
#                     return

#     if correct_answers >= 10:
#         client_socket.sendall("Congratulations! 🎉 You answered 10 questions correctly!\n".encode())
    
#     client_socket.close()

# def start_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(('0.0.0.0', 9999))
#     server.listen(5)
#     print("Server started and waiting for connections...")
    
#     while True:
#         client_socket, addr = server.accept()
#         print(f"Accepted connection from {addr}")
#         handle_client(client_socket)

# if __name__ == "__main__":
#     start_server()



import socket
import threading
import json
import random

# Load questions from JSON file
with open('questions.json') as f:
    questions = json.load(f)

# Shuffle questions
random.shuffle(questions)

class ClientHandler(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.current_question_index = 0
        self.attempts = 0
        self.correct_answers = 0

    def run(self):
        global questions
        while self.current_question_index <= len(questions):
            if self.correct_answers >= len(questions):
                self.client_socket.sendall("Congratulations! You have answered 10 questions correctly! 🎉".encode())
                break

            question = questions[self.current_question_index]
            question_text = question['question']
            options = question['options']

            # Send question and options
            question_message = f"{question_text}\n" \
                               f"A: {options['A']}\n" \
                               f"B: {options['B']}\n" \
                               f"C: {options['C']}\n" \
                               f"D: {options['D']}\n" \
                               "Your answer (A/B/C/D): "
            self.client_socket.sendall(question_message.encode())

            try:
                # Receive client's answer
                answer = self.client_socket.recv(1024).decode().strip().upper()
                
                # Display answer picked by the client on the server side
                print(f"Client picked answer: {answer}")
                
                if answer == question['answer']:
                    self.client_socket.sendall(b'Correct! Moving to the next question.\n')
                    self.correct_answers += 1
                    self.current_question_index += 1
                    self.attempts = 0  # Reset attempts
                else:
                    self.attempts += 1
                    print(f"Wrong answer. Attempt {self.attempts} of 3.")
                    if self.attempts >= 3:
                        self.client_socket.sendall(b'You have exceeded the maximum number of attempts. Disconnecting.\n')
                        # break
                        self.client_socket.close()
                    else:
                        self.client_socket.sendall(b'Incorrect. Try again.\n')

                # Display number of questions answered and wrong attempts
                print(f"Questions answered correctly: {self.correct_answers}")
                print(f"Wrong attempts: {self.attempts}")
                print(f"{self.current_question_index} is the CQI")

            except ConnectionResetError:
                break

        if self.correct_answers >= 7:
            self.client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server started and listening on port 12345.")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        handler = ClientHandler(client_socket)
        handler.start()

if __name__ == "__main__":
    start_server()
