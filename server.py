#To do:
#Add game speed in online version
#CREATE A GAME END (finish state), if playerData[player][0] != '-150': causes error?

import socket
from _thread import *
from cactus import *
import time

gameState = "pregame"

server = "192.168.70.159"
port = 5555 #typically an open port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #type of connection we are making

#binding socket to server and port
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(10) #opens up port to "listen". Parameter = number of connections
print("Waiting for connection, server has started")


def stringToArr(str):
    return str.split(",")

#data format: y position, dino choice
playerData = []

def threaded_client(conn, player): #conn = connection
    global currentPlayer
    global gameState
    global startTime
    global cacti
    frameTime = time.time()
    gameSpeed = 1
    conn.send(str.encode(str(playerData[player][0])))
    reply = ""

    while True:
        try:
            data = stringToArr(conn.recv(2048).decode())
            playerData[player][0] = data[0]
            playerData[player][1] = data[1]

            if not data:
                print("Disconnected")
                break
            else:  

                if "countdown" in gameState:
                    gameState = "countdown" + str(int(time.time()-startTime))
                    if(int(time.time()-startTime)) == 3:
                        gameState = "game"

                #Sends cactus data to everyone

                #checks if game should end

                totalDead = 0
                for i in range(len(playerData)):
                    if int(playerData[i][0]) < -100:
                        totalDead += 1

                if gameState == "game":
                    if currentPlayer - totalDead == 1:
                        gameState = "countdown0"
                        startTime = time.time()
                        cacti = [Cactus(-1000, i) for i in range(3)] #-1000 so it automatically gets moved to the beginning

                    if gameSpeed <= 3:
                        gameSpeed += 0.001

                cactusPositions = []
                for cactus in cacti:
                    if gameState == "game":
                        if (time.time()-frameTime) > 1/30:
                            cactus.move(cacti, gameSpeed)
                            frameTime = time.time()

                    cactusPositions.append(int(cactus.x))

                reply = gameState + "," + str(currentPlayer) + "," + str(cactusPositions[0]) + "," + str(cactusPositions[1]) + "," + str(cactusPositions[2]) 

                for j in range(2):
                    for i in range(currentPlayer):
                        if i == player:
                            pass
                        else:
                            reply += "," + str(playerData[i][j])

                print("Received: ", data)
                print("Sending : ", reply)

            
            conn.sendall(str.encode(str(reply)))

        except Exception as e:
            print("An exception occured: ")
            print(e)
            break

    print("Lost connection")
    conn.close()
    currentPlayer -= 1

currentPlayer = 0

cacti = [Cactus(-1000, i) for i in range(3)] #-1000 so it automatically gets moved to the beginning

while True: #continuosly looks for connections
    conn, addr = s.accept() #accepts any incoming connections
    print("Connected to:", addr)
    playerData.append([450,0])

    if currentPlayer == 1: #1 less than the players needed to start 
        gameState = "countdown"
        startTime = time.time()

    start_new_thread(threaded_client, (conn, currentPlayer)) #allows for multiple connections happening at once
    currentPlayer += 1

    