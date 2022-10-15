import hashlib
import socket
import threading


# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59999))

def welcome():
    print("Welcome User to The Messaging Server!")
    print("would you like to signup or login")

    choice = str(input("Enter Here:"))
    if choice == "login":
        login()
        #starting listening and writing thread
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()
        
        write_thread = threading.Thread(target=write)
        write_thread.start()
    elif choice == "signup":
        register()
    else:
        #If wrong input restarts function again
        print("You must enter signup or login")
        welcome()

def login():
    global Username
    Username = input("Please enter your username")
    Password = input("Please enter your password")
    db = open('database.txt' , 'r')

    #Conitnues if if username and password greater than 1
    if len(Username or Password)>1:
        #seperating usernames and password
        #put username and password into seperate lists
        Username_list = []
        Password_list = []
        for i in db:
            a,b = i.split(" P:")
            b = b.strip()
            Username_list.append(a)
            Password_list.append(b)
        #creates dictionary to link username to corresponding password
        login_details = dict(zip(Username_list, Password_list))

        try:
            if Username in login_details:
                #takes password from database.txt
                hashed = login_details[Username].strip('b')
                hashed = hashed.replace("'", "")

                #hashes the inputted password and works out the digest
                inputted = hashlib.sha512(str(Password).encode('utf-8')).hexdigest()

            #Comparing inputted password digest to associated Password of Username digest
                if str(inputted) == str(hashed):
                    print("Login successful, welcome", Username)
                else:
                    print("Incorrect Password")
                    welcome()
            else:
                print("Incorrect Username")
                welcome()
        except:
            print("Login Error")
            welcome()
    else:
        print("Please enter a username or password")
        login()


def register():
    Username = input("Please enter your username") 
    Password = input("Please enter your password")
    Confirm_password = input("Please confirm your password")
    #For reading Usernames in database
    db = open('database.txt' , 'r')

    #seperating usernames and password
    #put username and password into seperate lists
    Username_list = []
    Password_list = []
    for i in db:
        a,b = i.split(" P:")
        b = b.strip()
        Username_list.append(a)
        Password_list.append(b)
    #creates dictionary to link username to corresponding password
    login_details = dict(zip(Username_list, Password_list))

    if Password != Confirm_password:
        print("Password don't match")
        register()
    elif Username in Username_list:
        print("Username already exists")
        register()
    elif Password == Confirm_password:
        #Hashes the password works out the digest and saves in database text file
        hash_Password = hashlib.sha512(str(Password).encode('utf-8')).hexdigest()
        try:
            #Appends username and p: digest of the password
            db = open('database.txt','a')
            db.write(Username + " P:" +str(hash_Password)+"\n")
            db.close()
            print("Success please login now")
            welcome()
        except:
            print("Registeration Error")
            print("Reloading")
            register()
    else:
        print("register error")
        register()

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('ascii')
            #server asks for username and recieves from client
            if message == 'USERNAME':
                client.send(Username.encode('ascii'))
            else:
                print(message)
        except:
        # Close Connection When Error
            print("An error occured!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(Username, input(''))
        #if message starts with ! it is a command
        if message[len(Username)+2:].startswith('!'):
            #only admin can access command
            if Username == 'admin':
                if message[len(Username)+2:].startswith('!kick'):
                    #to get to the username we are trying to use a command on
                    #goes past ur username,space,colon and command
                    client.send(f'KICK {message[len(Username)+2+6:]}'.encode('ascii'))
                elif message[len(Username)+2:].startswith('!welcome'):
                    client.send(f'WELCOME {message[len(Username)+2+9:]}'.encode('ascii'))
            else:
                print("Admin Activity Only")
        else:
            client.send(message.encode('ascii'))

welcome()