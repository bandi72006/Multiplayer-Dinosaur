import socket
from _thread import *

server = "192.168.1.70"
port = 5555 #typically an open port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #type of connection we are making

#binding socket to server and port
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2) #opens up port to "listen". Parameter = number of connections
print("Waiting for connection, server has started")

def arrToString(arr):
    return str(arr[0]) + "," + str(arr[1])

def stringToArr(str):
    string = str.split(",")
    return string[0], string[1]

pos = [450, 450]
playerDinoChoices = [0, 0]

def threaded_client(conn, player): #conn = connection
    global currentPlayer
    conn.send(str.encode(str(pos[player])))
    reply = ""
    while True:
        try:
            data = stringToArr(conn.recv(2048).decode())
            pos[player] = data[0]
            playerDinoChoices[player] = data[1]

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = str(pos[0]) + "," + str(playerDinoChoices[0])

                else:
                    reply = str(pos[1]) + "," + str(playerDinoChoices[1])

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(str(reply)))

        except:
            break

    print("Lost connection")
    conn.close()
    currentPlayer -= 1

currentPlayer = 0

while True: #continuosly looks for connections
    conn, addr = s.accept() #accepts any incoming connections
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer)) #allows for multiple connections happening at once
    currentPlayer += 1