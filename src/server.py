import socket
import asyncore
import random
import pickle


BUFFERSIZE = 4098

outgoing = []
class Alien:
  def __init__(self, ownerid):
    self.x = 50
    self.y = 50
    self.health = 3
    self.ownerid = ownerid

minionmap = {}


def spaceUpdate(message):
  arr = pickle.loads(message)
  print(str(arr))
  playerid = arr[1]
  x = arr[2]
  y = arr[3]

  if playerid == 0: return

  minionmap[playerid].x = x
  minionmap[playerid].y = y




  remove = []

  for i in outgoing:
    update = ['player locations']

    for key, value in minionmap.items():
      update.append([value.ownerid, value.x, value.y])
    
    try:
      i.send(pickle.dumps(update))
    except Exception:
      remove.append(i)
      continue
    
    print ('sent update data')

    for r in remove:
      outgoing.remove(r)

class MainServer(asyncore.dispatcher):
  def __init__(self, port):
    asyncore.dispatcher.__init__(self)
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.bind(('', port))
    self.listen(10)
  def handle_accept(self):
    conn, addr = self.accept()
    print ('Connection address:' + addr[0] + " " + str(addr[1]))
    outgoing.append(conn)
    playerid = random.randint(1000, 1000000)
    alien = Alien(playerid)
    minionmap[playerid] = alien
    conn.send(pickle.dumps(['id update', playerid]))
    SecondaryServer(conn)

class SecondaryServer(asyncore.dispatcher_with_send):
  def handle_read(self):
    recievedData = self.recv(BUFFERSIZE)
    if recievedData:
      spaceUpdate(recievedData)
    else: self.close()

MainServer(4330)
asyncore.loop()
