
#import socket and other libraries
import socket
import threading





#use a conditional in the loop to exit.

def client():
    #create a client socket to send and receive messages.
    c = socket.socket()
    host = '127.0.0.1'
    port = 12345
    #assign client the proper ip address and port number
    c.connect((host, port))

    #need a loop to receive messages and process the data better
    #to continue client and server interaction until exit
    while True:
        data = input('Enter your message: ')

        #give the client the ability to send a message to the server
        c.sendall(bytes(data,'utf-8'))
        print(f"Server response: {c.recv(1024).decode('utf-8')}")


if __name__ == "__main__":
    client()