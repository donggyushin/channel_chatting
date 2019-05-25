import socket
import json
import threading


def client():
    host = 'localhost'
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    while True:

        username = input('Input username: ')
        channel = int(
            input('Which channel do you want to join in? (from 0 to 9999) '))

        data = {
            "username": username,
            "channel": channel
        }

        data = json.dumps(data)
        client_socket.send(data.encode())
        response = client_socket.recv(1024).decode()
        if response == 'already existing username':
            print(response)
            continue
        break

    threading.Thread(target=receive_message, args=(client_socket,)).start()
    print('Enjoy channel chatting! If you want to quit, just input "quit()"')
    message = ''
    while message.lower().strip() != 'quit()':
        message = input()

        data = {
            "message": message,
            "channel": channel,
            "username": username
        }
        data = json.dumps(data)
        client_socket.send(data.encode())
        if message == 'quit()':
            break
    client_socket.close()


def receive_message(client_socket):
    while True:
        received_message = client_socket.recv(1024).decode()
        received_message = json.loads(received_message)
        username = received_message['username']
        message = received_message['message']
        print(username, ': ', message)


if __name__ == '__main__':
    client()
