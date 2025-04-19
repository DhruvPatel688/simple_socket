
#import socket and other libraries
import socket
import threading
import time
import sys

#This function handles the client receiving messages from other clients via the server
def receive(c):
    #Run the message acceptance until connection broken
    while True:
        
        try:
            message = c.recv(1024).decode('utf-8')
            # Bonus Feature Check to see if message has been received by server.
            if message == 'ACK':
                print('\nReceipt ACK: Message Received by Server.')
            else:
                # Use sys to help with formatting. Like print() but without white space.
                sys.stdout.write(message + '\nEnter Message: ')
        except OSError:
            break
        except Exception as e:
            break



#Main client function allows client to connect to server via a socket
def client():
    #create a client socket to send and receive messages.
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 8000
    #assign client the proper ip address and port number
    c.connect((host, port))
    
    #Use threading for asynchronous message handling
    client_handler = threading.Thread(target=receive, args=(c,))
    client_handler.daemon = True
    client_handler.start()
    #need a loop to receive messages and process the data better
    #to continue client and server interaction until exit
    while True:
        
        data = str(input())
        #Use this conditional so client can exit loop.
        if data == '.exit':
            print('Exiting')
            c.close()
            break
        else:
        #give the client the ability to send a message to the server
            c.sendall(bytes(data,'utf-8'))

#Running the program.           
if __name__ == "__main__":
    client()