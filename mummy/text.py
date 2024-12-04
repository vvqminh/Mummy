class Mummy:
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
        step = 2  # Slow down the mummy's movement (adjust this value to change the speed)
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
                self.y -= step
            elif down:
                self.y += step
            elif left:
                self.x -= step
            elif right:
                self.x += step
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
        if self.x != self.keyRun['X']:
            if self.x > self.keyRun['X']:  # Move left
                self.update(False, False, True, False)
            else:  # Move right
                self.update(False, False, False, True)
        elif self.y != self.keyRun['Y']:
            if self.y > self.keyRun['Y']:  # Move up
                self.update(True, False, False, False)
            else:  # Move down
                self.update(False, True, False, False)
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
