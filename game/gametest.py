#In this code, we have a map with boundaries and 2 different players.
#Players move at the same time because I couldn't fix it yet    (EDIT: Yaaaay I fixed this)
#Players are supposed to shoot bullets but I created another class for bullets here because it was easier
#Right now when you hold space, it literally creates art lol
#Now I tried to add your Wall class and file and tried to add some obstacles but it does not work as well lol
#Edit: I added the walls and drew them but they are not obstacles and players can go through them
#Edit2: I kinda fixed the bugs with the balls
#Added player and bullet direction
#I added to add player health and bullet damage/hitbox stuff but the game automatically ends after 3 bullets are shot.
#We need to fix this problem, game should only end if a player's health reaches 0

#I searched the web for free assets that we can use for players, map and walls but could not find something for free


import pygame
import random
import time
from gamefiles.wall import Wall
from clientClass import ClientClass
import sys

class Player:
    def __init__(self, x, y, colour, speed, keys_up, keys_left, keys_down, keys_right, type):
        self.x = x
        self.y = y
        self.colour = colour			# I added colour attribute to distinguish for now
        self.speed = speed
        self.radius = 10				# Since the players are circles, we'll have a radius
        self.bullets = []  				# List to store the player's bullets
        self.shooting = False
        self.bullet_damage = 1
        
        self.keys_up = keys_up			#adding these somehow fixed the moving seperately problem
        self.keys_left = keys_left
        self.keys_down = keys_down
        self.keys_right = keys_right
        self.direction = "D" 			#No "I" this time because it crashed idk why
        self.bulletDirection = "D"
        self.health = 3  				# Both player with start 3 hearts
        self.type = type                # id of the player, so that we know if to print a healthbar or text (can be changed to healthbar only for simplicitys sake)
        self.rect = pygame.Rect(self.x, self.y, 20, 20)

    def getData(self):
        bulletList = []
        for bullet in self.bullets:
            data = bullet.getData()
            if data[0] > 1 and data[0] < 999:
                if data[1] > 1 and data[1] < 699:
                    bulletList.append(data)
        #print(self.x, self.y, self.health, bulletList)
        return [self.direction, self.x, self.y, self.health, bulletList, self.shooting]

    def move(self, keys):				# Keyboard tracking
        self.direction = "I"
        self.shooting = False
        if keys[self.keys_up]:
            self.y -= self.speed
            self.direction = "W"
            self.bulletDirection = "W"
        if keys[self.keys_left]:
            self.x -= self.speed
            self.direction = "A"
            self.bulletDirection = "A"
        if keys[self.keys_down]:
            self.y += self.speed
            self.direction = "S"
            self.bulletDirection = "S"
        if keys[self.keys_right]:
            self.x += self.speed
            self.direction = "D"
            self.bulletDirection = "D"

        # Keep the player within the map boundaries, yes I copied and pasted this part from stackoverflow
        self.x = max(map_x + self.radius, min(self.x, map_x + map_width - self.radius * 2))
        self.y = max(map_y + self.radius, min(self.y, map_y + map_height - self.radius * 2))
        
        # I added collision check with the walls
        for wall in wallList:
            if self.collision_with_wall(wall):
                	# Move player back to the previous position if there is a collision, 1000 IQ move lol
                if keys[self.keys_up]:
                    self.y += self.speed
                if keys[self.keys_left]:
                    self.x += self.speed
                if keys[self.keys_down]:
                    self.y -= self.speed
                if keys[self.keys_right]:
                    self.x -= self.speed
        
        self.rect.x, self.rect.y = self.x, self.y

    def collision_with_wall(self, wall):	# alright, I fixed the bug with the walls
        if (self.x + self.radius >= wall.xStart and self.x + self.radius <= wall.xStart + wall.width and
            self.y + self.radius >= wall.yStart and self.y + self.radius <= wall.yStart + wall.height):
            return True
        return False

    def collisionDetect(self, listOfObject):
        for rectangle in listOfObject:
            if self.rect.colliderect(rectangle):
                listOfObject.remove(rectangle)
                rectangle.picked = True
                if rectangle.type == 1:
                    self.speed += 1
                if rectangle.type == 2:
                    self.health += 1
                if rectangle.type == 3: #idk how to  make the bullet  dmg higher -> i think this  is enough
                    self.bullet_damage += 1      #Bullet damage +1
                client.pickedPowerUp(rectangle.type, rectangle.x, rectangle.y)
                return True
        return False

    def draw(self, window):
        pygame.draw.circle(window, self.colour, (self.x + self.radius, self.y + self.radius), self.radius)
        #pygame.draw.rect(window, (0, 0, 0), self.rect, 1)
        self.printHealth(window)

        for bullet in self.bullets:
            bullet.move()
            bullet.draw(window)
            
    def shoot(self):
        bullet = Bullet(self.x + self.radius, self.y + self.radius, self.colour, self.bulletDirection, 10, self.radius, self.bullet_damage) # Create a bullet
        self.bullets.append(bullet)  # Add the bullet to the player's bullets list
        self.shooting = True
        
        #if self == player1:                    #whenever you shoot - you loose health - that fucks up the code
        #    player2.health -= bullet.damage    #since the bullets are faster than the players - theres no way of getting shot by your own bullets, so lets just skip that + it will be easier later
        #elif self == player2:
        #    player1.health -= bullet.damage
            
    def check_collision(self, bullets):
        for bullet in bullets:
            distance = ((self.x + self.radius) - bullet.x) ** 2 + ((self.y + self.radius) - bullet.y) ** 2
            if distance <= (self.radius + bullet.radius) ** 2:
                self.health -= bullet.damage
                bullets.remove(bullet)
                #del bullet
        
    def new_check_collision(self, data):
        if data != []:
            for i in range(0, len(data)):
                for j in range(1, len(data[i])):
                    if len(data[i][j]) > 0:
                        #print(data)
                        for k in range(0, len(data[i][j])):
                            distance = ((self.x + self.radius) - int(data[i][j][k][1])) ** 2 + ((self.y + self.radius) - int(data[i][j][k][2])) ** 2
                            if distance <= (self.radius + 4) ** 2:
                                self.health -= 1
                                #print(data[i],"\n", data[i][j],"\n", data[i][j][k],"\n")
                                save = data[i][j][k]
                                data[i][j].remove(data[i][j][k])
                                return data[i][0], save
        return [], []
        
    def printHealth(self, window):  #code from geeks for geeks or smth like that
        if self.type == 1:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('Health: ' + str(self.health), True, GREEN, BLACK)
            textRect = text.get_rect()
            textRect.center = (925,20)
            window.blit(text, textRect)
        else:
            if self.health >= 3:
                healthColor = GREEN
            elif self.health == 2:
                healthColor = ORANGE
            else:
                healthColor = RED
            pygame.draw.rect(window, healthColor, (self.x - 5, self.y - 12, 29, 5))

class Bullet:
    def __init__(self, x, y, colour, direction, speed, radius, bullet_damage):
        self.x = x
        self.y = y
        self.colour = colour
        self.direction = direction
        self.speed = speed
        self.damage = bullet_damage 						#Bullet damage changes with powerups
        self.radius = 4					#I changed the bullets into circles

    def getData(self):
        return [self.x, self.y]

    def move(self):								#Okay bullets move now
        if self.direction == "W":
            self.y -= self.speed
        elif self.direction == "A":
            self.x -= self.speed
        elif self.direction == "S":
            self.y += self.speed
        elif self.direction == "D":
            self.x += self.speed
    
        for wall in wallList:
            if self.collision_with_wall(wall):
                	# idk how to remove bullets in this lineup so lets just stop them and turn invisible lol #1000 iq move as before
                if self.speed != 0:
                    self.x = 0
                    self.y = 0
                self.speed = 0
                self.colour = BLACK
                #del self

    def collision_with_wall(self, wall):	# alright, I fixed the bug with the walls
        if (self.x >= wall.xStart and self.x <= wall.xStart + wall.width and
            self.y >= wall.yStart and self.y <= wall.yStart + wall.height):
            return True
        return False

    def draw(self, window):
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.radius)

class PowerUp():
    def __init__(self, num, x, y, window):
        print("new powerup")
    #    self.type = random.randint(1,3)
    #    self.timeToLive = 300
    #    self.timeToRender = 300
    #    self.x = random.randint(0, 900)
    #    self.y = random.randint(0, 600)
        self.type = num
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.picked = False
        self.window = window

    def draw(self):
        global powerUpObjectList
        global powerUpList
        if self.picked:
            #if self in powerUps:
            if self in powerUpObjectList:
                #powerUps.remove(self)
                powerUpObjectList.remove(self)
                powerUpList.remove([self.type, self.x, self.y])
                self.x = 0
                self.y = 0
                self.rect.x, self.rect.y = self.x, self.y
                self.color = WHITE
                del self
                return
        #elif self.timeToLive > 0:
        elif self.x != 0:
            if self.type == 1:
                self.color = GREEN
            elif self.type == 2:
                self.color = RED
            else:
                self.color = PINK
            pygame.draw.rect(self.window, self.color, self.rect, 10)
        else:
            self.x = 0
            self.y = 0
            self.rect.x, self.rect.y = self.x, self.y
    
    def delete(self):
        global powerUpObjectList
        global powerUpList
        if self in powerUpObjectList:
            powerUpObjectList.remove(self)
        if [self.type, self.x, self.y] in powerUpList:
            powerUpList.remove([self.type, self.x, self.y])
        self.x = 0
        self.y = 0
        self.rect.x, self.rect.y = self.x, self.y
        self.color = WHITE
        del self
        return


def draw_walls(window):
    for wall in wallList:
        pygame.draw.rect(window, BLACK, (wall.xStart, wall.yStart, wall.width, wall.height))

pygame.init()

window_width, window_height = 1000, 700							#Window size
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Kuba Musab GTA VI Demo")

client = ClientClass(window)
connect = False
while not connect:
    connect = client.connect()

startGame = "WAIT\n"
while startGame == "WAIT\n":
    startGame = client.getServerData()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (3, 252, 28)
RED = (255, 8, 28)
PINK = (255, 192, 203)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

map_width, map_height = window_width - 10, window_height - 10								#Playable map size
map_x, map_y = (window_width - map_width) // 2, (window_height - map_height) // 2		#Map adjustment center

player_start_position= [(50, 350), (484, 32), (940, 350), (490, 650), (40, 650), (940, 650), (940, 55), (40, 55)]			#Player starts from one of these 8 places, so 12.5% change of starting from the same place -idk this was the easiest way for now.
start_x, start_y = random.choice(player_start_position)											#We could also give an id to a player and make him start from any of these coordinates unless it's taken by another player but
																	#That looks very complicated for now
player1 = Player(start_x, start_y, GREEN, 2, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, 1)
#player2 = Player(950, 350, RED, 2, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, 2)
#powerup = None

timer = 0
sendTimer = 0
bulletCount = 0

clock = pygame.time.Clock()

wallList = []
bulletShoot = True              #prevents bullet spam
inv = False

wall1 = Wall(370, 345, 250, 30)  # Example walls test
wall2 = Wall(475, 240, 30, 250)  # This was really a pain in ass
wall3 = Wall(100, 100, 250, 30)
wall4 = Wall(100, 130, 30, 150)
wall5 = Wall(650, 100, 250, 30)
wall6 = Wall(870, 130, 30, 150)
wall7 = Wall(650, 600, 250, 30)
wall8 = Wall(870, 450, 30, 150)
wall9 = Wall(100, 600, 250, 30)
wall10 = Wall(100, 450, 30, 150)

wallList.append(wall1)
wallList.append(wall2)
wallList.append(wall3)
wallList.append(wall4)
wallList.append(wall5)
wallList.append(wall6)
wallList.append(wall7)
wallList.append(wall8)
wallList.append(wall9)
wallList.append(wall10)
#powerUps = []
powerUpList = []
powerUpObjectList = []

print(window)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client.disconnect()
            time.sleep(1)
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()			#Keyboard tracking

    powerUpData = client.getPowerUpData()
    if powerUpData != [0, 0, 0]:
        if powerUpData not in powerUpList:
            powerUpList.append(powerUpData)
            powerUp = PowerUp(powerUpData[0], powerUpData[1], powerUpData[2], window)
            powerUpObjectList.append(powerUp)

    player1.move(keys)			
    #player2.move(keys)
    
    player1.collisionDetect(powerUpObjectList)
    #player2.collisionDetect(powerUps)

    if not keys[pygame.K_SPACE]:
        bulletShoot = True

    if keys[pygame.K_SPACE]:			#Press space to shoot a bullet
        if bulletShoot == True:
            player1.shoot()
            #player2.shoot()
            bulletShoot = False

    window.fill(BLACK)			#fills black in the non-map part 	
    
    pygame.draw.rect(window, WHITE, (map_x, map_y, map_width, map_height))		#Draw the map
    
    draw_walls(window)  # Draw the walls
    if timer == 600:
    #    if len(powerUps) > 0:
    #        powerup.picked = True
    #    powerup = PowerUp()
    #    powerUps.append(powerup)
        timer = 0
    timer = timer + 1
	
    player1.draw(window)
    data = client.getBulletData()
    if timer % 3 == 0:
        object, bullet = player1.new_check_collision(data)
        if bullet != []:
            client.deleteBullet(object, bullet)

    #player2.draw(window)

    coordinates = client.deletePowerUp()
    if coordinates != []:
        for i in range(0, len(coordinates)):
            coordinates[i] = int(coordinates[i])
        for coord in powerUpObjectList:
            #print(coord.type, coord.x, coord.y)
            if [coord.type, coord.x, coord.y] == coordinates:
                coord.delete()
                coordinates = []
                

    for object in powerUpObjectList:
        object.draw()
    #if len(powerUps) > 0:
    #    powerup.draw(window)

    #player1.check_collision(player2.bullets)
    #player2.check_collision(player1.bullets)

    if sendTimer == 1:
        data = player1.getData()
        sendTimer = 0
        client.setPlayerData(data)
    sendTimer += 1

    if player1.health <= 0: #or player2.health <= 0:  # Check for game over condition
        print("Game over")
        client.disconnect()
        pygame.quit()
        time.sleep(1)
        exit()

    pygame.display.flip()

    clock.tick(60)			#REfresh rate, a.k.a FPS
