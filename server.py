
#import sockets and libraries
import socket
import threading
import os


list_of_clients = []



#Add more information inside this loop to give message receipts and broadcast clients connected to server 
def accept_clients(c, addr):
    while True:
        
        data = c.recv(1024).decode('utf-8')
        print("Received Message: ", data, " from", addr)
        #Still need to add 'exit' conditional for client to exit server.
        
        receipt = 'Received message ' + data + ' from '+ str(addr[1])
        broadcast(bytes(receipt,'utf-8'), c)
    c.close()

#used to broadcast message to all clients
def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 
 
                # if the link is broken, we remove the client 
                remove(clients) 

#this is the main server function that connects to clients
def server():
    #create a socket on the server side to recieve message
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 12345
    s.bind((host, port))
    s.listen(5)
    print(f"Server listening on {host}:{port}")
    #Accept the connection and print in terminal which address server is connected with until client disconnects
    while True:
        c, addr = s.accept()
        #still need to add unique ID:


        list_of_clients.append(c)
        print("Connected with", addr)
        #call accept_client function to properly handle the data
        client_handler = threading.Thread(target=accept_clients, args=(c, addr))
        client_handler.start()

if __name__ == "__main__":
    server()