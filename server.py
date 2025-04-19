
#import sockets and libraries
import socket
import threading
import os
import uuid


#Use a dictionary to keep track of different clients and their unique IDS
list_of_clients = {} #Bonus Feature allow more than 2 clients to connect


#This function allows the server to connect with clients
def accept_clients(c, addr):
    #Connect with clients until socket disconnected
    while True:
        
        data = c.recv(1024).decode('utf-8')
        # When exiting, we need error handle so that client disconnects
        if not data:
            message = '\n'+ addr + ' has disconnected.'
            print(message)
            broadcast(bytes(message,'utf-8'), c) #call function to help broadcast message to all clients
            #Update dictionary with one less client.
            if c in list_of_clients:
                del list_of_clients[c]
            break

        print("Received Message: ", data, " from", addr)
        #Bonus Feature: Send ACK message receipt.
        receipt = 'ACK'
        c.send(bytes(receipt, 'utf-8'))
        message = '\nReceived message \'' + data + '\' from '+ addr
        broadcast(bytes(message,'utf-8'), c) #call function to help broadcast message to all clients
    c.close()

#used to broadcast message to all clients
def broadcast(message, connection): 
    #iterate through dictionary of clients and send message.
    for clients, value in list(list_of_clients.items()): 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 
 
                # if the link is broken, we remove the client
              
                del list_of_clients[clients]

#this is the main server function that connects to clients
def server():
    #create a socket on the server side to recieve message
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = '127.0.0.1'
    port = 8000
    s.bind((host, port))
    s.listen(5)
    print(f"Server listening on {host}:{port}")
    #Accept the connection and print in terminal which address server is connected with until client disconnects
    
    while True:
        c, addr = s.accept()
        #Unique ID added using special library UUID
        unique_id = str(uuid.uuid4())
    
        list_of_clients[c] = unique_id
        #Broadcast to all clients the other clients they are connected to.
        for key,value in list(list_of_clients.items()):
            message = f"\nOther client connected is {value}"
            broadcast(bytes(message,'utf-8'), key)
     
        print("Connected with", unique_id)
        #call accept_client function to properly handle the data asynchronously 
        client_handler = threading.Thread(target=accept_clients, args=(c, unique_id))
        client_handler.start()

#run the program 
if __name__ == "__main__":
    server()