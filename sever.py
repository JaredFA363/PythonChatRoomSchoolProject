import socket
import threading

#Connection address & data
host = '127.0.0.1'
#non reserved port
port = 59999

#Server
#SOCK_STREAM indicates we are using TCP
#AF.INET indicates we are using a internet socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind our host and port
server.bind((host, port))
server.listen()

#Lists for clients and their Usernames
clients = []
client_Usernames = []

#sending messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

#Handle mesages from clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            #if kick command sent by admin will kick user
            if message.decode('ascii').startswith('KICK'):
                kick_username = message.decode('ascii')[5:]
                kick_user(kick_username)
            #if welcome command sent by admin will welcome user and send rules
            elif message.decode('ascii').startswith('WELCOME'):
                welcome_username = message.decode('ascii')[8:]
                welcome_user(welcome_username)
            else:
            #broadcasts message into chatroom
                broadcast(message)
        except:
            print("Handle Error")

#Listening Function
def recieve():
    while True:
        #Accepts Conncection
        client, address = server.accept() 

        # Request And Store Username so shows user before message
        client.send('USERNAME'.encode('ascii'))
        #1024 bits
        username = client.recv(1024).decode('ascii')
        client_Usernames.append(username)
        clients.append(client)
        print("{} has joined the server".format(username))

        #Broadcast Username & informs client they have connected
        broadcast("{} has entered the chat".format(username).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in client_Usernames:
        name_index = client_Usernames.index(name)
        #gets username to be kicked in list
        user_to_kick = clients[name_index]
        #removes username from list hence they are kicked
        clients.remove(user_to_kick)
        user_to_kick.send("You were kicked".encode('ascii'))
        user_to_kick.close()
        client_Usernames.remove(name)
        #broadcasts to rest of chatroom that user has been kicked
        broadcast(f'{name} was kicked'.encode('ascii'))

def welcome_user(name):
    if name in client_Usernames:
        #gets username and prints rules
        broadcast(f'Welcome, {name} this is the chatroom! \n Rules: \n no Profanity \n No annoying people \n Enjoy'.encode('ascii'))

recieve()