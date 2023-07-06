import socket
import threading

HOST = 'localhost'
PORT = 5000

clients = []
usernames = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            usernames.remove(username)
            broadcast(f'{username} has left the chat'.encode('utf-8'))
            break

def accept_connections():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NAME'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')

        usernames.append(username)
        clients.append(client)

        print(f'Username of the client is {username}')
        broadcast(f'{username} has joined the chat'.encode('utf-8'))
        client.send('Connected to the server'.encode('utf-8'))

        client.send('Enter your message: '.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print('Server started')
accept_connections()
