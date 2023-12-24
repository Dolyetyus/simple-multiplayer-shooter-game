############################CHANGES##############################
# added:
    # active_players - list that can keep track of alive players:
        #main  purpose  ->  not defined
    # players_send_back  -  list to send back stuff
    # playerStatus() - threaded function to print logged in users - so that main can actually start the game and whatnot
    # wait for at least 2 players  to  start a game in main() - sending a msg to a client "WAIT"
    # starting the game - send "STR" to  players
    # sending back "FAIL" if logged in players are at the maximum limit
    # STP - not enough  players
    # comments
    # I'm thinking of turning the data into a list to check the flags and other info
# deleted: nothing (i think)

import socket
import threading
import time
from ast import literal_eval            #for changing string to list nicely
import random

max_users = 69                                      # Capacity of the server
logged_in_users = []
players_send_back = []                                 # which players are alive and which are not - can be used to winning screen
hostPort = ("", 1113) 
powerUpList = []

def serverInit():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(hostPort)
    sock.settimeout
    return sock
    
def connectUser(sock, data, address):
    if len(logged_in_users) >= max_users:
        msg = prepForBinary("FAIL")
        sock.sendto(msg.encode("utf-8"), address)
    else:
        if address not in logged_in_users:
            logged_in_users.append(address)
            players_send_back.append(address)
        print("connected", address)
        msg = prepForBinary("SYN-OK")
        sock.sendto(msg.encode("utf-8"), address)

def disconnectUser(sock, data, address):
    if address in logged_in_users:
        logged_in_users.remove(address)
    msg = "FIN-OK"
    #sock.sendto(msg.encode("utf-8"), address)
    sendToClient(sock, msg, address)  
    print("disconnected", address)
    if address in players_send_back:
        players_send_back.remove(address)

def playerStatus():
    while True:
        print(logged_in_users)
        time.sleep(1)

def recvData(sock):
    global powerUpList
    while True:
        data, address = sock.recvfrom(4096)
        #print(data, address)
        data = data.decode("utf-8")
        data = prepForAscii(data)
	
        if data == "SYN":
            connectUser(sock, data, address)
        elif data == "FIN":
            disconnectUser(sock, data, address)
        elif data == "STR-OK":
            if address in players_send_back:
                players_send_back.remove(address)
        elif data == "STP-OK":
            print("stopped")
        elif "PCK" in data:
            data = data.split()
            print(data[0],data[1],data[2])
            powerUpList.remove([data[1], data[2], data[3]])
            msg = "NO " + data[1] + " " + data[2] + " "  + data[3]
            sendToClient(sock, msg, "server")
        else:        	
        	# Player id should also be added to the data here and then should be sent to every player - address can be used an id - otherways are kinda difficult/require bad solutions (or idk how to do it nicely)
        	# and players should process the coordinates etc. Flag handling can be done in the client as well for MOVE AND POWERUP flags etc.
            #print(data)
            #print("trying")
            #print(data)
            createPowerUp(sock, data, address)
            #sendToClient(sock, data, address)                           #Since recvData() is working with threading, sendToClient() will also work with threading and will only send message if a message is received.

def createPowerUp(sock, data, address):
    global logged_in_users
    global powerUpList

    type = random.randint(1,3)
    if len(logged_in_users) > 1:
        x = random.randint(0, 900)
        y = random.randint(0, 600)
        prob = random.randint(0, 2000)
        if prob == 500:
            if x > 370 and x < 620 and y > 345 and y < 375:
                x = random.randint(0, 900)
                y = random.randint(0, 600)
            elif x > 475 and x < 505 and y > 240 and y < 490:
                x = random.randint(0, 900)
                y = random.randint(0, 600)
            elif x > 100 and x < 350 and y > 100 and y < 130:
                x = random.randint(0, 900)
                y = random.randint(0, 600)
            elif x > 100 and x < 130 and y > 130 and y < 280:
                x = random.randint(0, 900)
                y = random.randint(0, 600)
            elif x > 650 and x < 800 and y > 100 and y < 130:
                x = random.randint(0, 900)
                y = random.randint(0, 600)
            elif x > 870 and x < 900 and y > 130 and y < 280:
                x = random.randint(0, 900)
                y = random.randint(0, 600)
            elif x > 650 and x < 800 and y > 600 and y < 630:
                x = random.randint(0, 900)
                y = random.randint(0, 600)
            elif x > 870 and x < 900 and y > 450 and y < 600:
                x = random.randint(0, 900)
                y = random.randint(0, 600)
            elif x > 100 and x < 350 and y > 600 and y < 630:
                x = random.randint(0, 900)
                y = random.randint(0, 600)
            elif x > 100 and x < 130 and y > 450 and y < 600:
                x = random.randint(0, 900)
                y = random.randint(0, 600)
            else: 
                #print("test")
                sendToClient(sock, "APU " + str(type) + " " + str(x) + " " + str(y), "server")
                powerUpList.append([str(type), str(x), str(y)])
    sendToClient(sock, data, address)                           #Since recvData() is working with threading, sendToClient() will also work with threading and will only send message if a message is received.
            
'''def sendMessage(sock, message, address):
    threads = []					#Here we will have the threads for each address
    for i in logged_in_users:
        thread = threading.Thread(target=sendToClient, args=(sock, message, address), daemon=True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()'''
        
def sendToClient(sock, message, address):                             #wtf is address variable? - i dont think we need it in this approach
    if "[" in message:
        message = literal_eval(message)
        message.insert(0, address)                             #I did a lot of research and this was the most useful and easiest way to do this. Multithreading literally is unnecessarily complicated and the latency with this is very low (but python is still slower than many other languages like C or Assembly)
        message = str(message)
    elif message == "FIN-OK":
        message = message + " " + str(address)  
    message = prepForBinary(message)
    for client_address in logged_in_users: 
        if client_address != address:
            #print(message)
            sock.sendto(message.encode("utf-8"), client_address)

#####################################
generator = "110101001"

def prepForBinary(strSend):             #since msg is in a format SEND <user> <msg> and only <msg> can be altered this fucntion makes it so that the string to send it SEND <user> 010101011101110...
    #print("in prep", strSend)
    asciiString = strSend.split()
    asciiString = " ".join(asciiString)
    binaryString = translateToBinary(asciiString)
    remainder = crc(binaryString, generator)
    binaryString = binaryString + remainder
    strSend = strSend.split()
    strSend = " ".join(strSend) + " " + binaryString
    #print(binaryString)
    return binaryString

def prepForAscii(msg):              #since we get DELIVERY <user> 1010110011001... this function translates binary string into ascii so that we can work on in later on + print it
    msgToChange = msg
    binaryString = msgToChange.split()
    binaryString = " ".join(binaryString)
    msgToChange = msgToChange.split()
    remainder = crc(binaryString, generator)
    for i in remainder:             #error  checking -> if  remainder is made out  of only 0's -> no errors
        if i != "0":
            #print("error")
            return 
    #print("no error")
    asciiString =  translateToAscii(binaryString, generator)
    msgToChange = asciiString
    #print("in ascii", asciiString)
    return msgToChange

def translateToBinary(asciiString):     #transaltes ascii string  to binary string 
    asciiString = ''.join(format(ord(i), '08b') for i in asciiString)
    return asciiString

def translateToAscii(binaryString, generator):
    binaryString = binaryString[:len(binaryString) - len(generator) + 1]    #deleting codeword from the string so we can print the actual msg
    i = 0
    while i in range(0, len(binaryString)):
        if i % 9 == 0:
            binaryString = binaryString[:i] + " " + binaryString[i:]
        i = i + 1
    binaryString = binaryString[1:]
    return "".join([chr(int(binary, 2)) for binary in binaryString.split(" ")]) #translates into ascii

def xor(binaryRep, generator):  #xoring -> binary division
    toPrint = ""
    for i in range(0, len(generator)):
        if binaryRep[i] == generator[i]:
            toPrint = toPrint + "0"
        else:
            toPrint = toPrint + "1"
    return toPrint

def crc(binaryRep, generator):      #preping for xoring -> crc algorithm
    zeroString = ""
    for i in range(0, len(generator)):
        zeroString = zeroString + "0"
    binaryRep = binaryRep + zeroString[1:]

    result = ""
    i = 0
    while len(binaryRep) >= len(generator):
        if binaryRep[i] == "0":
            result = xor(binaryRep[i:], zeroString)
        else:
            result = xor(binaryRep[i:], generator)
        binaryRep = result + binaryRep[i+len(generator):]
        binaryRep = binaryRep[1:]
    return binaryRep

def main():
    global sock
    global players_send_back

    while len(logged_in_users) < 2:
        msg = "WAIT"
        sendToClient(sock, msg, "")
        time.sleep(1)

    while len(players_send_back) != 0:            #keeps track of which players have sent the "STR-OK" back
        msg = "STR"
        sendToClient(sock, msg, "")

    print("game start")
    while True:
        if len(logged_in_users) >= 2:
            print("in game")
            time.sleep(1)
        else:
            msg  = "STP"
            sendToClient(sock, msg, "")
            return
            
sock = serverInit()
threading.Thread(target=recvData, args=(sock,), daemon=True).start() #thread for receiving data
threading.Thread(target=playerStatus, daemon=True).start() #thread for printing the players status

while True:   
    main()
