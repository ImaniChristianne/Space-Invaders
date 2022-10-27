import socket
from _thread import *
import pickle
from alien import Alien

#creating our server

server = "192.168.11.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen((2))
print("Waiting for a connection, Server Started")

players = [Alien (0,0,50,50,(255,0,0)), Alien (0,0,50,50,(0,255,0))]
def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""

    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            players[player]= data

            if not data:
                print ("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received: ", data)
                print("Sending: ", reply)
            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("Lost connection")

    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)


    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
