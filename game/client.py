############################CHANGES##############################
# For taking keyboard inputs, keyboard library is added
# General message format is created but it's not complete yet (check the thinking out loud file)
# The printing cum here: msg is removed because now I just want it to print the player direction and stuff
# A new function is added to keep track of the keyboard keys
# IDK why but does not take two keyboard inputs simultuaneusly -idk how to spell this word either lol- so you can't move and shoot at the same time. I also tried using "elif x and space" but it did not work. So I added dead reckoning direction to calculate the last moving direction. However, if you hold 2 keys at the same time, it does not respond. You can press the keys as fast as it allows you to (time.sleep is the limit)
# The server should assign players as player 1 and player 2 and the clients should create a seperate player object using classes to keep record of the positions etc
# The threading for movement() should start some time after the STP-OK message, that should be fixed later and it's an easy fix 
# Edit: Debugging part might take some time and the visualization of the game will be difficult (Probably)

import socket
import threading
import time
import keyboard  # using module keyboard - keyboard module doesnt work for me - i am not a root user on my WSL, so we have to change it to something different prob - i was also thinking, since we will prob use pygame, why cant we just have the client code and rendering code as one? ig what we have right now is more readable - for now im gonna assume that the input works fine
from gamefiles.player import Player    # Adds the player class to the client.py

hostPort = ("127.0.0.1", 1112)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.settimeout(0.1)
tEvent = threading.Event()

# MESSAGE = flag + player_id + x_coordinate + y_coordinate + direction + shoot + powerup         and then this message should also be handled in the client

players = {}  # Dictionary to store players

def connect(sock):
    while True:
        try:
            sock.sendto("SYN\n".encode("utf-8"), hostPort)
            data, address = sock.recvfrom(1024)
            data = data.decode()
            while data != "SYN-OK\n":
                if data == "SYN-OK\n":
                    break
                elif data == "FAIL\n":
                    print("server full")
                    quit()
                else:
                    data, address = sock.recvfrom(1024)
                    data = data.decode()
            return
        except:
            print("cumming")

def disconnect(sock):
    tEvent.set()
    time.sleep(0.1)
    while True:
        try:
            sock.sendto("FIN\n".encode("utf-8"), hostPort)
            data, address = sock.recvfrom(1024)
            data = data.decode()
            while data != "FIN-OK\n":
                data, address = sock.recvfrom(1024)
                data = data.decode()
            return
        except:
            print("came")

def sendData(msg):
    msg = msg + "\n"
    sock.sendto(msg.encode("utf-8"), hostPort)
    return
    
def receiveData(sock):
    while tEvent.is_set() == False:
        try:
            data, address = sock.recvfrom(1024)
            data = data.decode()
            print(data)
            handleData(data)
        except socket.timeout:
            continue

def handleData(data):
    if data == "STR\n":
        sendData("STR-OK")
    elif data == "WAIT\n":
        print("waiting")
    elif data == "STP\n":
        sendData("STP-OK")
    elif data[:4] == "MOVE":
	    handle_server_message(data)	#If the message flag is MOVE, then the player stats should change
	
def handle_server_message(message):
    player_id, x, y, direction, shoot, powerup = message.split()    #This part is written assuming that: MESSAGE = flag + player_id + x_coordinate + y_coordinate + direction + shoot + powerup

    # Check if the player already exists in the dictionary
    if player_id in players:
        player = players[player_id]  # Get the existing player object
    else:
        # Create a new player object if it doesn't exist
        player = Player((int(x), int(y)), direction)          #For player creating part, the direction should be "I" by default and the x and y coordinates should be determined by the server.
        players[player_id] = player

    player.update_position((int(x), int(y)))
    player.set_direction(direction)
    player.set_shoot(shoot == "True")			#This is a comparison, if the received shoot value is True, then it shoots. If it's false, then it does not. 1==1 ot 0==1 but simpler.
    player.set_powerup(int(powerup))			#This value is already explained in the player.py but in short: 0 = None, 1 = Extra Heart, 2 = Faster Bullets, 3 = Increased bullet damage

def movement():
    deadReckoningDirection = "I" # keeps track of the last direction if a bullet is shot
    direction = ''
    shoot = False
    flag = "MOVE"
    print("in movement")
    while True: 
        if keyboard.is_pressed('w'):
            direction = "W"
            deadReckoningDirection = direction
        elif keyboard.is_pressed('a'):
            direction = "A"
            deadReckoningDirection = direction
        elif keyboard.is_pressed('s'):
            direction = "S"
            deadReckoningDirection = direction
        elif keyboard.is_pressed('d'):
            direction = "D"
            deadReckoningDirection = direction
        elif keyboard.is_pressed(' '):
            shoot = True
            direction = deadReckoningDirection
        else:
            direction = "I" # stands for idle
            deadReckoningDirection = direction

        message = flag + " " + direction + " " +str(shoot)
        print("button pressed message", message)
        sendData(message)
        time.sleep(0.1)
        direction = ''
        shoot = False

def main():
    connect(sock)
    threading.Thread(target=receiveData, args=(sock,), daemon=True).start()
    threading.Thread(target=movement, daemon=True).start()
    while True:
        msg = input()
        sendData(msg)
        if msg == "1":
            break
	    	
    disconnect(sock)

main()
