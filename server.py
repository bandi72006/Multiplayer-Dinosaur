#To do:
#Add game speed in online version

from Player import Player
import socket
from _thread import *
from cactus import *

server = "192.168.70.159"
port = 5555 #typically an open port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #type of connection we are making

#binding socket to server and port
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2) #opens up port to "listen". Parameter = number of connections
print("Waiting for connection, server has started")


def stringToArr(str):
    return str.split(",")

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
                #Sends cactus data to everyone

                cactusPositions = []
                for cactus in cacti:
                    cactus.move(cacti, 1)
                    cactusPositions.append(cactus.x)

                if player == 0:
                    sendingPosition = 1
                else:
                    sendingPosition = 0

                reply = str(pos[sendingPosition]) + "," + str(playerDinoChoices[sendingPosition]) + "," + str(cactusPositions[0]) + "," + str(cactusPositions[1]) + "," + str(cactusPositions[2])


                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(str(reply)))

        except:
            break

    print("Lost connection")
    conn.close()
    currentPlayer -= 1

currentPlayer = 0

cacti = [Cactus(-1000, i) for i in range(3)] #-1000 so it automatically gets moved to the beginning

while True: #continuosly looks for connections
    conn, addr = s.accept() #accepts any incoming connections
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer)) #allows for multiple connections happening at once
    currentPlayer += 1