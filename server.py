
#import sockets and libraries
import socket
import threading
import os
import uuid

#list_of_clients = []
list_of_clients = {}


#Add more information inside this loop to give message receipts and broadcast clients connected to server 
def accept_clients(c, addr):
    while True:
        
        data = c.recv(1024).decode('utf-8')
        if not data:
            message = '\n'+ addr + ' has disconnected.'
            print(message)
            broadcast(bytes(message,'utf-8'), c)
            if c in list_of_clients:
                del list_of_clients[c]
            break

        print("Received Message: ", data, " from", addr)
        receipt = 'ACK'
        c.send(bytes(receipt, 'utf-8'))
        message = '\nReceived message \'' + data + '\' from '+ addr
        broadcast(bytes(message,'utf-8'), c)
    c.close()

#used to broadcast message to all clients
def broadcast(message, connection): 
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
        #still need to add unique ID:
        unique_id = str(uuid.uuid4())
        #list_of_clients.append(c)
        list_of_clients[c] = unique_id
        for key,value in list(list_of_clients.items()):
            message = f"\nOther client connected is {value}"
            broadcast(bytes(message,'utf-8'), key)
        #for client in list_of_clients:
        #    for c in list_of_clients:
        #        if client != c:
        #            client.send(bytes(str(c),'utf-8'))
        print("Connected with", unique_id)
        #call accept_client function to properly handle the data
        client_handler = threading.Thread(target=accept_clients, args=(c, unique_id))
        client_handler.start()

if __name__ == "__main__":
    server()