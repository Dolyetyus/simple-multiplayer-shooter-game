import socket
import threading
import time
from gamefiles.player import Player    # Adds the player class to the client.py
from ast import literal_eval            #for changing string to list nicely
from enemyClass import Enemy

class ClientClass():
    def __init__(self, window):
        self.hostPort = ("127.0.0.1", 1113)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tEvent = threading.Event()
        self.sock.settimeout(0.1)
        self.players = {}
        self.serverData = ""
        self.playerData = []
        self.enemiesData = []
        self.enemiesList = []
        self.enemiesObjectList = []
        self.window = window
        self.powerUpType = 0
        self.powerUpX = 0
        self.powerUpY = 0
        self.powerUpToDelete = []

        self.generator = "110101001"

    def connect(self):
        try:
            msg = "SYN"
            msg = self.prepForBinary(msg)
            print(msg)
            self.sock.sendto(msg.encode("utf-8"), self.hostPort)
            data, address = self.sock.recvfrom(4096)
            data = data.decode()
            data = self.prepForAscii(data)
            if data == "SYN-OK":
                print("calling threads\n")
                threading.Thread(target=self.receiveData, daemon=True).start()
                #threading.Thread(target=movement, daemon=True).start()
                return True
            elif data == "FAIL":
                print("server full")  
        except:
            print("cumming")
            return False

    def disconnect(self):
        self.tEvent.set()
        time.sleep(0.1)
        while True:
            try:
                msg = self.prepForBinary("FIN")
                self.sock.sendto(msg.encode("utf-8"), self.hostPort)
                data, address = self.sock.recvfrom(4096)
                data = data.decode()
                data = self.prepForAscii(data)
                while data != "FIN-OK":
                    data, address = self.sock.recvfrom(4096)
                    data = data.decode()
                return
            except:
                print("came")

    def setPlayerData(self, data):
        self.playerData = data
        self.sendData(data)
    
    def sendData(self, msg):
        if msg != str(msg):
            msg = str(msg)
        #print(msg)
        msg = self.prepForBinary(msg)
        #test = self.prepForBinary(msg)
        #self.prepForAscii(test)
        #if "PCK" in msg:
            #print("send",msg)
        self.sock.sendto(msg.encode("utf-8"), self.hostPort)
    
    def receiveData(self): 
        while self.tEvent.is_set() == False:
            try:
                data, address = self.sock.recvfrom(4096)
                data = data.decode()
                print("got", data)
                data = self.prepForAscii(data)
                self.handleData(data)
            except socket.timeout:
                continue

    def handleData(self, data):
        #data = self.prepForAscii(data)
        #print(data)
        self.serverData = data
        if data == "STR":
            self.sendData("STR-OK")
        elif data == "WAIT":
            print("waiting")
        elif data == "STP":
            self.sendData("STP-OK")
        elif data[:4] == "MOVE":
            self.handle_server_message(data)	#If the message flag is MOVE, then the player stats should change
        elif "FIN-OK" in data:
            print(data)
            address = data[7:]
            print(address)
            for enemy in self.enemiesObjectList:
                if str(enemy.getId()) == address:
                    print("deleting")
                    enemy.deleteEnemy()
        elif "APU" in data:
            data = data.split()
            self.powerUpType = int(data[1])
            self.powerUpX = int(data[2])
            self.powerUpY = int(data[3])
        elif "NO" in data:
            data = data.split()
            print(data[1], data[2], data[3])
            self.powerUpToDelete = [data[1], data[2], data[3]]
        else:
            self.updateEnemiesData()

    def getPowerUpData(self):
        return [self.powerUpType, self.powerUpX, self.powerUpY]
    
    def pickedPowerUp(self, num, x, y):
        msg = "PCK " + str(num) + " " + str(x) + " " + str(y) + " \n"
        #print(msg)
        self.sendData(msg)

    def deletePowerUp(self):
        return self.powerUpToDelete

    def getServerData(self):
        return self.serverData
    
    def getEnemiesData(self):
        return self.enemiesData
    
    def getNewEnemies(self):
        return self.newEnemy
    
    def getBulletData(self):
        toReturn = []
        for enemy in self.enemiesObjectList:
            #if len(enemy.getBulletData()) > 0:
            #print(enemy.getBulletData())
            toReturn.append([enemy, enemy.getBulletData()])
        return toReturn
    
    def deleteBullet(self, object, bullet):
        #print(object, bullet)
        for enemy in self.enemiesObjectList:
            if object == enemy:
                enemy.deleteBullet(bullet[0])
    
    def updateEnemiesData(self):
        #print("update",self.serverData)
        data = literal_eval(self.serverData)
        if data[0] not in self.enemiesList:
            self.enemiesList.append(data[0])
            enemy = Enemy(data[0], self.window)
            self.enemiesObjectList.append(enemy)
        self.enemiesData = data           #has to be changed
        for enemy in self.enemiesObjectList:
            if enemy.getId() == data[0]:
                #print(data)
                enemy.setData(data[1], data[2], data[3], data[4], data[5], data[6], False)

    def handle_server_message(self, message):
        player_id, x, y, direction, shoot, powerup = message.split()    #This part is written assuming that: MESSAGE = flag + player_id + x_coordinate + y_coordinate + direction + shoot + powerup

        # Check if the player already exists in the dictionary
        if player_id in self.players:
            player = self.players[player_id]  # Get the existing player object
        else:
            # Create a new player object if it doesn't exist
            player = Player((int(x), int(y)), direction)          #For player creating part, the direction should be "I" by default and the x and y coordinates should be determined by the server.
            self.players[player_id] = player

        player.update_position((int(x), int(y)))
        player.set_direction(direction)
        player.set_shoot(shoot == "True")			#This is a comparison, if the received shoot value is True, then it shoots. If it's false, then it does not. 1==1 ot 0==1 but simpler.
        player.set_powerup(int(powerup))			#This value is already explained in the player.py but in short: 0 = None, 1 = Extra Heart, 2 = Faster Player, 3 = Increased bullet damage

########################################################

    def prepForBinary(self, strSend):             #since msg is in a format SEND <user> <msg> and only <msg> can be altered this fucntion makes it so that the string to send it SEND <user> 010101011101110...
        #print("make into binary", strSend)
        asciiString = strSend.split()
        asciiString = " ".join(asciiString)
        binaryString = self.translateToBinary(asciiString)
        remainder = self.crc(binaryString, self.generator)
        binaryString = binaryString + remainder
        strSend = strSend.split()
        strSend = " ".join(strSend) + " " + binaryString
        #print(binaryString)
        return binaryString

    def prepForAscii(self, msg):              #since we get DELIVERY <user> 1010110011001... this function translates binary string into ascii so that we can work on in later on + print it
        msgToChange = msg
        binaryString = msgToChange.split()
        binaryString = " ".join(binaryString)
        msgToChange = msgToChange.split()
        remainder = self.crc(binaryString, self.generator)
        for i in remainder:             #error  checking -> if  remainder is made out  of only 0's -> no errors
            if i != "0":
                #print("error")
                return 
        #print("no error")
        asciiString =  self.translateToAscii(binaryString, self.generator)
        msgToChange = asciiString
        #print("in ascii", asciiString)
        return msgToChange

    def translateToBinary(self, asciiString):     #transaltes ascii string  to binary string 
        asciiString = ''.join(format(ord(i), '08b') for i in asciiString)
        return asciiString

    def translateToAscii(self, binaryString, generator):
        binaryString = binaryString[:len(binaryString) - len(generator) + 1]    #deleting codeword from the string so we can print the actual msg
        i = 0
        while i in range(0, len(binaryString)):
            if i % 9 == 0:
                binaryString = binaryString[:i] + " " + binaryString[i:]
            i = i + 1
        binaryString = binaryString[1:]
        return "".join([chr(int(binary, 2)) for binary in binaryString.split(" ")]) #translates into ascii

    def xor(self, binaryRep, generator):  #xoring -> binary division
        toPrint = ""
        for i in range(0, len(generator)):
            if binaryRep[i] == generator[i]:
                toPrint = toPrint + "0"
            else:
                toPrint = toPrint + "1"
        return toPrint

    def crc(self, binaryRep, generator):      #preping for xoring -> crc algorithm
        zeroString = ""
        for i in range(0, len(generator)):
            zeroString = zeroString + "0"
        binaryRep = binaryRep + zeroString[1:]

        result = ""
        i = 0
        while len(binaryRep) >= len(generator):
            if binaryRep[i] == "0":
                result = self.xor(binaryRep[i:], zeroString)
            else:
                result = self.xor(binaryRep[i:], generator)
            binaryRep = result + binaryRep[i+len(generator):]
            binaryRep = binaryRep[1:]
        return binaryRep
