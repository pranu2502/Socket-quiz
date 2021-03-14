import socket
import sys
import select
import time

server = "127.0.0.1"
port = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((server,port))     #Client makes a connection with the server
except:
    print("Please start the server first") # A message is given if the server is not on
    exit()
if(client):
    msg = client.recv(2048)        #Recieving  a message from the server
    print(msg.decode())

    while True:

        # maintains a list of possible input streams
        sockets_list = [sys.stdin, client]                   #The message can be from the socket or the user

        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

        for socks in read_sockets:     #Print themessage if the message is from the socket
            if (socks == client):
                message = socks.recv(2048)
                print(message.decode())
                if("GAME OVER" in message.decode()):  #If the message is 'GAME OVER' close the client
                    sys.exit()
                    client.close()
            else:                                       #If the message is from the user send it to the client
                message = sys.stdin.readline()
                client.send(message.encode())
                sys.stdout.flush()
    server.close()
    sys.exit()

    
    



