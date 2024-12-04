from bfs_mummy import Graph
import json

import pygame
import sys
from pygame.locals import *

with open('./map.json', 'r') as file:
    dataMap = json.load(file)

grap = Graph(6, 6)
grap.addRectangleEdges()

def getKey(X, Y):
    for item in dataMap:
        if 'X' in item and 'Y' in item and 'key' in item:
            if abs(item['X'] - X) < 5 and abs(item['Y'] - Y) < 5:
                return item["key"]
    return None

def getLocate(key):
    return {"X": dataMap[key]["X"], "Y": dataMap[key]["Y"]}

pygame.init()
DISPLAYSURF = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Mummy maze !")

surfaceMap = pygame.transform.scale(
    pygame.image.load("./image/floor.jpg"), (600, 600))

# (0,0) (60, 0) (120,0) (180,0) (240,0)
playerUp = pygame.image.load("./image/player/move_up.png")
playerDown = pygame.image.load("./image/player/move_down.png")
playerLeft = pygame.image.load("./image/player/move_left.png")
playerRight = pygame.image.load("./image/player/move_right.png")

TIME = 5

mummyUp = pygame.image.load("./image/mummy/redup.png")
mummyDown = pygame.image.load("./image/mummy/reddown.png")
mummyLeft = pygame.image.load("./image/mummy/redleft.png")
mummyRight = pygame.image.load("./image/mummy/redright.png")

Wall_blue = {
    "wallX": 400,
    "wallY": 200,
    "wallW": 10,
    "wallH": 100
}
Wall_red_1 = {
    "wallX": 200,
    "wallY": 400,
    "wallW": 100,
    "wallH": 10
}
Wall_red_2 = {
    "wallX": 200,
    "wallY": 300,
    "wallW": 10,
    "wallH": 100
}
wallX = Wall_blue["wallX"], Wall_red_1["wallX"], Wall_red_2["wallX"]
wallY = Wall_blue["wallY"], Wall_red_1["wallY"], Wall_red_2["wallY"]

class Player:
    mummyGo = 0

    def __init__(self):
        self.x = 0
        self.y = 0
        self.surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.surface.blit(playerDown, (20, 20), (0, 0, 60, 60))

        self.timeSkip = 0
        self.option = 0

        self.go = 0

    def update(self, up, down, left, right):
        if Player.mummyGo == 0 and self.go < 100:
            self.option = (self.timeSkip // TIME) % 5
            if up or down or left or right:
                self.go += 5
                self.timeSkip += 1
                self.surface.fill((0, 0, 0, 0))
                self.animate(up, down, left, right)

            if up and self.y > 0:
                self.y -= 5
            elif down and self.y < 600 - 100:
                self.y += 5
            elif left and self.x > 0:
                self.x -= 5
            elif right and self.x < 600 - 100:
                self.x += 5
        else:
            self.go = 0
            Player.mummyGo = (Player.mummyGo + 1) % 3

    def animate(self, up, down, left, right):
        img = ""
        if up:
            img = playerUp
        elif down:
            img = playerDown
        elif left:
            img = playerLeft
        elif right:
            img = playerRight

        if self.option == 0:
            self.surface.blit(img, (20, 20), (0, 0, 60, 60))
        if self.option == 1:
            self.surface.blit(img, (20, 20), (60, 0, 60, 60))
        if self.option == 2:
            self.surface.blit(img, (20, 20), (120, 0, 60, 60))
        if self.option == 3:
            self.surface.blit(img, (20, 20), (180, 0, 60, 60))
        if self.option == 4:
            self.surface.blit(img, (20, 20), (240, 0, 60, 60))

    def draw(self):
        DISPLAYSURF.blit(self.surface, (self.x, self.y))


class Mummy:
    mummyGo = 0
    def __init__(self):
        self.x = 500
        self.y = 500
        self.surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.surface.blit(mummyDown, (20, 20), (0, 0, 60, 60))
        self.timeSkip = 0
        self.option = 0
        self.go = 0

        self.locat = []
        self.keyRun = {"X": self.x, "Y": self.y}

    def update(self, up, down, left, right):

        if Player.mummyGo == 0:
            if self.go < 100:
                if self.timeSkip <= TIME:  # 0-5
                    self.option = 0
                elif self.timeSkip <= TIME*2:  # 6-10
                    self.option = 1
                elif self.timeSkip <= TIME*3:  # 11-15
                    self.option = 2
                elif self.timeSkip <= TIME*4:
                    self.option = 3
                elif self.timeSkip <= TIME*5:
                    self.option = 4
                elif self.timeSkip > TIME*5:
                    self.timeSkip = 0

                if up or down or left or right:
                    self.go += 5
                    self.timeSkip += 1
                    self.surface.fill((0, 0, 0, 0))
                    self.animate(up, down, left, right)

                if up:
                    self.y -= 5
                elif down:
                    self.y += 5
                elif left:
                    self.x -= 5
                elif right:
                    self.x += 5
            else:
                self.go = 0       
                Player.mummyGo += 1
                if Player.mummyGo == 3:
                    Player.mummyGo = 0
                
    def animate(self, up, down, left, right):
        img = ""
        if up:
            img = mummyUp
        elif down:
            img = mummyDown
        elif left:
            img = mummyLeft
        elif right:
            img = mummyRight

        if self.option == 0:
            self.surface.blit(img, (20, 20), (0, 0, 60, 60))
        if self.option == 1:
            self.surface.blit(img, (20, 20), (60, 0, 60, 60))
        if self.option == 2:
            self.surface.blit(img, (20, 20), (120, 0, 60, 60))
        if self.option == 3:
            self.surface.blit(img, (20, 20), (180, 0, 60, 60))
        if self.option == 4:
            self.surface.blit(img, (20, 20), (240, 0, 60, 60))

    def draw(self):
        DISPLAYSURF.blit(self.surface, (self.x, self.y))

    def run(self, keyPlayer, playerX, playerY):
        # Tìm khóa hiện tại của Mummy
        keyMummy = getKey(self.x, self.y)
        
        # Tìm đường đi từ Mummy đến Player
        listFind = grap.findListPath(keyMummy, keyPlayer)
        
        if listFind:  # Nếu tìm thấy đường đi
            nextStep = getLocate(listFind[0])  # Điểm đến tiếp theo
            if self.x < nextStep["X"]:
                self.update(False, False, False, True)  # Đi sang phải
            elif self.x > nextStep["X"]:
                self.update(False, False, True, False)  # Đi sang trái
            elif self.y < nextStep["Y"]:
                self.update(False, True, False, False)  # Đi xuống
            elif self.y > nextStep["Y"]:
                self.update(True, False, False, False)  # Đi lên
        else:
            keyMummy = getKey(self.x, self.y)
            listFind = grap.findListPath(keyMummy, keyPlayer)

            keyWall = None
            for x, y in zip(wallX, wallY):  # Iterate through each wall coordinate
                keyWall = getKey(x, y)
                if keyWall is not None:
                    break

            # Handle walls (blocking path)
            if keyMummy == keyWall:
                if playerY == wallY:
                    Player.mummyGo = 0
                else:
                    for item in listFind:
                        if item != keyWall - 1:  # Prevent crossing the wall
                            self.keyRun = getLocate(item)
            elif keyMummy == keyWall - 1:  # Adjacent wall
                if playerY == wallY[keyWall - 1]:
                    Player.mummyGo = 0
                else:
                    for item in listFind:
                        if item != keyWall:  # Prevent crossing the wall
                            self.keyRun = getLocate(item)
            else:
                self.keyRun = getLocate(listFind[0])

            # Move two steps if there is a clear path
            if len(listFind) > 1:
                self.keyRun = getLocate(listFind[1])
            elif listFind:  # Only one step left, move towards it
                self.keyRun = getLocate(listFind[0])
            else:
                self.keyRun = {"X": self.x, "Y": self.y}  # Stay in place if no path is found


player = Player()
mummy = Mummy()

up, down, left, right = False, False, False, False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                up = True
            if event.key == K_DOWN:
                down = True
            if event.key == K_LEFT:
                left = True
            if event.key == K_RIGHT:
                right = True

    DISPLAYSURF.blit(surfaceMap, (0, 0))
    pygame.draw.rect(DISPLAYSURF, (0, 0, 255), (Wall_blue["wallX"], Wall_blue["wallY"], Wall_blue["wallW"], Wall_blue["wallH"]))
    pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (Wall_red_1["wallX"], Wall_red_1["wallY"], Wall_red_1["wallW"], Wall_red_1["wallH"]))
    pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (Wall_red_2["wallX"], Wall_red_2["wallY"], Wall_red_2["wallW"], Wall_red_2["wallH"]))

    player.draw()
    player.update(up, down, left, right)
    mummy.draw()
    
    if player.go == 0:
        up, down, left, right = False, False, False, False

    if Player.mummyGo > 0:
        keyPlayer = getKey(player.x, player.y)
        mummy.run(keyPlayer, player.x, player.y)

    pygame.display.update()
    pygame.time.Clock().tick(60)

