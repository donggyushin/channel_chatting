import socket
import threading
import json

clients = []


def server():

    host = ''
    port = 5000

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))

    server_socket.listen()
    while True:
        listening_for_client(server_socket)


def send_message(conn):
    while True:
        print("asldkjasldkjaslkdj")
        data = conn.recv(1024).decode()
        print(data)
        if not data:
            break
        data = json.loads(conn.recv(1024).decode())

        client_name = data["username"]
        channel = data["channel"]
        message = data['message']
        print('1')
        if message == 'quit()':
            print('2')
            for client in clients:
                if client['username'] == client_name:
                    clients.remove(client)
        else:
            print('3')
            for client in clients:
                if client['channel'] == channel:
                    if client['username'] != client_name:
                        data = json.dumps(data)
                        client['socket'].send(data.encode())

    conn.close()


def listening_for_client(server_socket):
    conn, _ = server_socket.accept()

    passOk = True

    while passOk:
        passOk = False
        data = conn.recv(1024)

        new_client = json.loads(data.decode())
        username = new_client["username"]
        channel = new_client["channel"]
        new_client = {
            "socket": conn,
            "username": username,
            "channel": channel
        }

        for client in clients:
            if client['username'] == username:
                conn.send('already existing username'.encode())
                passOk = True

    print('here??')
    clients.append(new_client)
    print('current clients: ', clients)
    t = threading.Thread(target=send_message, args=(conn, ))
    t.start()


if __name__ == '__main__':
    server()
