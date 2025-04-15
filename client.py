
#import socket and other libraries
import socket
import threading
import time


def receive(c):
    while True:
        
        try:
            message = c.recv(1024).decode('utf-8')
            if message == 'ACK':
                print('\nReceipt ACK: Message Received by Server.')
            else:
                print(message)
        except OSError:
            break
        except Exception as e:
            break


#use a conditional in the loop to exit.

def client():
    #create a client socket to send and receive messages.
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 8000
    #assign client the proper ip address and port number
    c.connect((host, port))
    
    client_handler = threading.Thread(target=receive, args=(c,))
    client_handler.daemon = True
    client_handler.start()
    #need a loop to receive messages and process the data better
    #to continue client and server interaction until exit
    while True:
        data = input('Enter your message: ')
        if data == '.exit':
            print('Exiting')
            c.close()
            break
        else:
        #give the client the ability to send a message to the server
            c.sendall(bytes(data,'utf-8'))

            
if __name__ == "__main__":
    client()