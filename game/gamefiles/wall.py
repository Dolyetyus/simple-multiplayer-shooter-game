class Wall:
    wallList = []

    def __init__(self, xStart, yStart, width, height):
        self.xStart = xStart
        self.yStart = yStart
        self.width = width
        self.height = height
    
    def exists(self):
        for i in self.wallList:
            if i in self.wallList:
                return True
        return 
    
    def addWall(self, xStart, yStart, width, height):
        if not self.exists(self):
            self.wallList.append((self, xStart, yStart, width, height))
        return self.wallList
    
    def removeWall(self, xStart, yStart, width, height):
        if self.exists(self):
            self.wallList.remove((self, xStart, yStart, width, height))

    def collision(self, x, y):
        for i in self.wallList:
            if x in range(i[1], i[3]):
                if y in range(i[2], i[4]):
                    return True
            
