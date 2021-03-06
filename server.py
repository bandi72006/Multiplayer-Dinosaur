import socket
from _thread import *

server = "192.168.1.70"
port = 5555 #typically an open port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #type of connection we are making

#binding socket to server and poort
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2) #opens up port to "listen". Parameter = number of connections
print("Waiting for connection, server has started")
    
def threaded_client(conn): #conn = connection
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:  #tries to receives some data
            data = conn.recv(2048) #bits of data we are trying to receive
            reply = data.decode("utf-8")
            
            if not data: #if no data received
                 print("Disconnected")
                 break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)

            conn.sendall(str.encode(reply))

        except:
            break

    print("Lost connection")
    conn.close()

while True: #continuosly looks for connections
    conn, addr = s.accept() #accepts any incoming connections
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,)) #allows for multiple connections happening at once
