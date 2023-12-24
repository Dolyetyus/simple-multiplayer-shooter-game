import pygame
import threading
import time
from gamefiles.wall import Wall

class Enemy():
    def __init__(self, address, window):
        self.id = address
        self.window = window
        self.x = 5
        self.y = 5
        self.health = 3
        self.direction = "D"
        self.colour = (125, 125, 125) # black as a template
        self.radius = 10
        self.shooting = False
        self.bulletList = []
        self.bullets = []
        self.dead = False
        self.speed = 0.1
        self.timer = 0

        self.wallStuff()
        threading.Thread(target=self.printEnemy).start()
    
    def setData(self, direction, x, y, health, bullets, shooting, dead):
        self.x = x
        self.y = y
        self.health = health
        self.direction = direction
        self.bullets = bullets
        self.shooting = shooting
        self.dead = dead
        if not self.dead:
            self.timer = 0

        self.length = len(self.bullets) - 1
        if self.shooting:
            bullet = Bullet(self.bullets[self.length][0], self.bullets[self.length][1], self.colour, 4)
            self.bulletList.append(bullet)
        while len(self.bulletList) != len(self.bullets):
            bullet = self.bulletList.pop()
            bullet.delete()

    def getData(self):
        return self.x, self.y, self.health, self.direction

    def getId(self):
        return self.id
    
    def deleteEnemy(self):
        self.x = 0
        self.y = 0
        self.health = 0
        self.radius = 0
        self.colour = (0, 0, 0)
        del self
    
    def deleteBullet(self, bullet):
        return
        if bullet != None:
            bullet.delete(bullet)

    def printEnemy(self):
        while True:
            if self.dead:
                self.deadReckon()
            pygame.draw.circle(self.window, self.colour, (self.x + self.radius, self.y + self.radius), self.radius)
            i = 0
            for bullet in self.bulletList:
                bullet.updateBullet(self.bullets[i][0], self.bullets[i][1], self.window)
                if self.length > i:
                    i = i + 1
            self.timer += 1
            if self.timer == 1000:
                self.dead = True
            time.sleep(0.001)

    def deadReckon(self):
        if self.direction == "W":
            self.y -= self.speed
        if self.direction == "A":
            self.x -= self.speed
        if self.direction == "S":
            self.y += self.speed
        if self.direction == "D":
            self.x += self.speed

        self.x = max(self.map_x + self.radius, min(self.x, self.map_x + self.map_width - self.radius * 2))
        self.y = max(self.map_y + self.radius, min(self.y, self.map_y + self.map_height - self.radius * 2))
        
        # I added collision check with the walls
        for wall in self.wallList:
            if self.collision_with_wall(wall):
                	# Move player back to the previous position if there is a collision, 1000 IQ move lol
                if self.direction == "W":
                    self.y += self.speed
                if self.direction == "A":
                    self.x += self.speed
                if self.direction == "S":
                    self.y -= self.speed
                if self.direction == "D":
                    self.x -= self.speed
        
    def collision_with_wall(self, wall):	# alright, I fixed the bug with the walls
        if (self.x + self.radius >= wall.xStart and self.x + self.radius <= wall.xStart + wall.width and
            self.y + self.radius >= wall.yStart and self.y + self.radius <= wall.yStart + wall.height):
            return True
        return False
    
    def getBulletData(self):
        toReturn = []
        for bullet in self.bulletList:
            entry = [bullet, bullet.x, bullet.y]
            toReturn.append(entry)
        return toReturn
    
    def wallStuff(self):
        self.wallList = []
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

        self.wallList.append(wall1)
        self.wallList.append(wall2)
        self.wallList.append(wall3)
        self.wallList.append(wall4)
        self.wallList.append(wall5)
        self.wallList.append(wall6)
        self.wallList.append(wall7)
        self.wallList.append(wall8)
        self.wallList.append(wall9)
        self.wallList.append(wall10)

        self.map_width, self.map_height = 990, 690								#Playable map size
        self.map_x, self.map_y = (1000 - self.map_width) // 2, (700 - self.map_height) // 2		#Map adjustment center

class Bullet():
    def __init__(self, x, y, colour, radius): 
        self.x = x
        self.y = y
        self.colour = colour
        self.radius = radius

    def updateBullet(self, x, y, window):
        self.x = x
        self.y = y
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.radius)

    def delete(self):
        #self.colour = (0, 0, 0)
        #self.x = 0
        #self.y = 0
        del self