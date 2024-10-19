"""
-----MAIN FILE-----

Main file with the game logic. The goal is to guide the lemmings from one door to the other using the tools available.

"""
#Importing necessary libraries and classes
import pyxel
import random
from elements.lemming import Lemming
from elements.cell import Cell
from tools.ladder import Ladder
from tools.umbrella import Umbrella
from tools.blocker import Blocker
from tools.shovel import Shovel
from elements.platforms import Platform
from elements.portal import Portal
from elements.score import Score

class App:
    # Used to define if the lemmings and main board should appear or not
    start = False
    
    # Dimensions of the board
    width = 256
    height = 256
    
    # Variable where the data for the score are stored
    score = 0
    
    # Used to check if all the lemmings have appeared of not
    countInvoked = 0
    
    # Initial coordinates of the cursor
    curX = 240
    curY = 240
    
    # Maximum amount for each element in the game
    maxLemmings = random.randint(10,20)
    maxUmbrellas = 5
    maxLadders = 10
    maxBlockers = 6
    maxTerrain = 7
    maxShovels = 3
    
    # Amount of rows and columns the game window has
    rows = 16
    columns = 16
    
    # Information of all the cells in game
    grid = []
    
    # Background color
    color = 0
    
    # Lists where the objects will be stored
    lemmings = []
    ladders = []
    umbrellas = []
    blockers = []
    shovels = []
    floors = []
    portals = []
    
    def __init__(self):
        # Creation of the game board
        pyxel.init(self.width,self.height)
        
        # Sprites are imported
        pyxel.load("sprites/sprites.pyxres") 
        
        # Creation of the score:
        self.score = Score(1,0,0,0,0,0,0,0)
        
        # Generating the platforms
        for i in range(self.maxTerrain):
            if i == 0:
                # Select randomly if the starting point will be at the top or at the bottom of the screen (board size require a row of platforms to start at one of those 2 points)
                starting = random.randint(0,1)
                if starting == 0:
                    # Select the X coordinate and create the block
                    cdy = 2
                    startingPoint = cdy
                    cdx = random.randint(0,10)
                    longitude = random.randint(5,10)
                    floor = Platform(16*cdx, 16*cdy, longitude, [0,64])
                    self.floors.append(floor)
                else:
                    # Select the X coordinate and create the block
                    cdy = 15
                    startingPoint = cdy
                    cdx = random.randint(0,10)
                    longitude = random.randint(5,10)
                    floor = Platform(16*cdx, 16*cdy, longitude, [0,64])
                    self.floors.append(floor)
            else:
                # Create a row of platforms every 2 rows
                if startingPoint == 2:
                    # Select both X and Y coordinates and create the block
                    cdx = random.randint(0,10)
                    longitude = random.randint(5,10)
                    cdy += 2
                    floor = Platform(16*cdx, 16*cdy, longitude, [0,64])
                    self.floors.append(floor)
                elif startingPoint == 15:
                    # Select both X and Y coordinates and create the block
                    cdx = random.randint(0,10)
                    longitude = random.randint(5,10)
                    cdy -= 2
                    floor = Platform(16*cdx, 16*cdy, longitude, [0,64])
                    self.floors.append(floor)
        
        # Marking in the grid the platforms generated
        for floor in self.floors:
            row = int(floor.y/16)
            column = int(floor.x/16)
            for i in range(0,floor.length):
                if (column+i) < 16 and (row) < 16:
                    self.grid[row][column+i].full = "P"
                            
        # Creation of the portals      
        for t in range(2):
            wright = False
            # A new position for the portal will be selected while the position is not valid  
            while not wright:
                codx = random.randint(0,15)
                cody = random.randint(3,15)
                # There must be a platform below the portal and it must be inside the game board
                if self.grid[cody][codx].full == "P" and not (cody-1) < 2:
                    wright = True
            
            # Starting portal
            if t == 0:
                portal = Portal(codx*16,(cody-1)*16,"START",[16,64])
                self.portals.append(portal)

            # Finishing portal
            elif t == 1:
                done = False
                while not done: 
                    if (codx*16) != self.portals[0].x or (cody*16) != self.portals[0].y:
                        portal = Portal(codx*16,(cody-1)*16,"FINISH",[32,64])
                        self.portals.append(portal)
                        row = int(cody-1)
                        column = int(codx)
                        self.grid[row][column].finishPortal = True
                        done = True
        
        # Run the app
        pyxel.run(self.update, self.draw)
        
    # Creating the matrix  
    for i in range(rows):
          grid.append([])
          for j in range(columns):
              cell = Cell(i,j,"",False,False,"NO","NO")
              grid[i].append(cell)   
        
    # Function to add a right ladder
    def rightLadder(self):
        row = int(self.curY/16)
        column = int(self.curX/16)
        if self.grid[row][column].full == "":
            ladder = Ladder(self.curX,self.curY,"Right",[64,48])
            self.ladders.append(ladder)
            self.grid[row][column].full = "RL"
    
    # Function to add a left ladder
    def leftLadder(self):
        row = int(self.curY/16)
        column = int(self.curX/16)
        if self.grid[row][column].full == "":
            ladder = Ladder(self.curX,self.curY,"Left",[64,64])
            self.ladders.append(ladder)
            self.grid[row][column].full = "LL"
    
    # Function to remove a ladder
    def removeLadder(self):
        row = int(self.curY/16)
        column = int(self.curX/16)
        if self.grid[row][column].full == "LL" or self.grid[row][column].full == "RL":
            self.grid[row][column].full = ""
        counter = 0
        for ladder in self.ladders:
            if ladder.x == self.curX and ladder.y == self.curY:
                del(self.ladders[counter])
            counter += 1
            
    # Function to eliminate lemmings  
    def lemmingGone(self):
        counter = 0
        for lemming in self.lemmings:
            if not lemming.living:
                del(self.lemmings[counter])
            counter += 1
            
    # Function to create an umbrella
    def placeUmbrella(self):
        row = int(self.curY/16)
        column = int(self.curX/16)
        if self.grid[row][column].full == "":
            umbrella = Umbrella(self.curX,self.curY,[48,32])
            self.umbrellas.append(umbrella)
            self.grid[row][column].full = "U"

    # Function to remove an umbrella     
    def removeUmbrella(self):
        row = int(self.curY/16)
        column = int(self.curX/16)
        if self.grid[row][column].full == "U":
            self.grid[row][column].full = ""
        counter = 0
        for umbrella in self.umbrellas:
            if umbrella.x == self.curX and umbrella.y == self.curY:
                del(self.umbrellas[counter])
            counter += 1
    
    # Function to create a blocker
    def placeBlocker(self):
        row = int(self.curY / 16)
        column = int(self.curX / 16)
        if self.grid[row][column].full == "":
            blocker = Blocker(self.curX, self.curY, [32, 32])
            self.blockers.append(blocker)
            self.grid[row][column].full = "B"
    
    # Function to remove a blocker
    def removeBlocker(self):
        row = int(self.curY / 16)
        column = int(self.curX / 16)
        if self.grid[row][column].full == "B":
            self.grid[row][column].full = ""
        counter = 0
        for blocker in self.blockers:
            if blocker.x == self.curX and blocker.y == self.curY:
                del (self.blockers[counter])
            counter += 1
            
    # Function to create a shovel     
    def placeShovel(self):
        row = int(self.curY / 16)
        column = int(self.curX / 16)
        if self.grid[row][column].full == "P":
            shovel = Shovel(self.curX, self.curY, [64, 32])
            self.shovels.append(shovel)
            self.grid[row][column].full = "S"

    # Function to remove a shovel  
    def removeShovel(self):
        row = int(self.curY / 16)
        column = int(self.curX / 16)
        if self.grid[row][column].full == "S":
            self.grid[row][column].full = "P"
        counter = 0
        for shovel in self.shovels:
            if shovel.x == self.curX and shovel.y == self.curY:
                del (self.shovels[counter])
            counter += 1
            
    # Function to set the visuals of the game
    def draw(self):    
        # Background color set to black
        pyxel.cls(0)
        
        # Background
        pyxel.blt(0,32,1,0,32,260,260)
       
        # Score text:     
        pyxel.text(0, 2, "Level:"+str(self.score.level), 10)
        pyxel.text(75, 2, "Alive:"+str(self.score.alive), 10)
        pyxel.text(150, 2, "Saved:"+str(self.score.saved), 10)
        pyxel.text(225, 2, "Dead:"+str(self.score.dead), 10)
        pyxel.text(0, 16, "Ladders(A/D):"+str(self.score.ladders), 7)
        pyxel.text(70, 16, "Umbrellas(W):"+str(self.score.umbrellas), 7)
        pyxel.text(138, 16, "Blockers(S):"+str(self.score.blockers), 7)
        pyxel.text(205, 16, "Shovels(X):"+str(self.score.shovels), 7)
        pyxel.line(0,32,256,32,7)
     
        # Drawing the platforms
        for floor in self.floors:
            for block in range(0,floor.length):            
                pyxel.blt(floor.x+(16*block),floor.y,0,0,64,16,16,0)
        
        # Drawing the portals
        for portal in self.portals:
            pyxel.blt(portal.x,portal.y,0,portal.sprite[0],portal.sprite[1],16,16,0)
        
        # Sprites to draw in case a platform is being broken
        for i in range(16):
            for j in range(16):
                if self.grid[i][j].hole == "1":
                    pyxel.blt(j*16,i*16,0,16,48,16,16,0)
                elif self.grid[i][j].hole == "2":
                    pyxel.blt(j*16,i*16,0,32,48,16,16,0)
                elif self.grid[i][j].hole == "3":
                    pyxel.blt(j*16,i*16,0,48,48,16,16,0)
                elif self.grid[i][j].hole == "DONE":
                    pyxel.blt(j*16,i*16,0,48,64,16,16,0)
                    
        # Drawing the lemmings          
        for lemming in self.lemmings:
            pyxel.blt(lemming.x,lemming.y,0,lemming.sprite[0],lemming.sprite[1],16,16,0)    
            
        # Drawing the ladders
        for ladder in self.ladders:
            row = int((ladder.y)/16)
            column = int((ladder.x)/16)
            if not self.grid[row][column].activated:
                pyxel.blt(ladder.x,ladder.y,0,ladder.sprite[0],ladder.sprite[1],16,16,0)
            else:
                if self.grid[row][column].ladderDone == "1":
                    pyxel.blt(ladder.x,ladder.y,0,ladder.sprite[0]+16,ladder.sprite[1],16,16,0)
                    
                elif self.grid[row][column].ladderDone == "2":
                    pyxel.blt(ladder.x,ladder.y,0,ladder.sprite[0]+32,ladder.sprite[1],16,16,0)
                    
                elif self.grid[row][column].ladderDone == "3":
                    pyxel.blt(ladder.x,ladder.y,0,ladder.sprite[0]+48,ladder.sprite[1],16,16,0)
                    
                elif self.grid[row][column].ladderDone == "4":
                    pyxel.blt(ladder.x,ladder.y,0,ladder.sprite[0]+64,ladder.sprite[1],16,16,0)
                    
                elif self.grid[row][column].ladderDone == "DONE":
                    pyxel.blt(ladder.x,ladder.y,0,ladder.sprite[0]+80,ladder.sprite[1],16,16,0)
        
        # Drawing the umbrellas
        for umbrella in self.umbrellas:
            row = int((umbrella.y)/16)
            column = int((umbrella.x)/16)
            if not self.grid[row][column].activated:
                pyxel.blt(umbrella.x,umbrella.y,0,112,umbrella.sprite[1],16,16,0)
            else:
                pyxel.blt(umbrella.x,umbrella.y,0,umbrella.sprite[0],umbrella.sprite[1],16,16,0)
                
        # Drawing the blockers   
        for blocker in self.blockers:
            row = int((blocker.y)/16)
            column = int((blocker.x)/16)
            if not self.grid[row][column].activated:
                pyxel.blt(blocker.x,blocker.y,0,96,blocker.sprite[1],16,16,0)
            else:
                pyxel.blt(blocker.x,blocker.y,0,blocker.sprite[0],blocker.sprite[1],16,16,0) 
                
        # Drawing the shovels
        for shovel in self.shovels:
            row = int((shovel.y)/16)
            column = int((shovel.x)/16)
            if self.grid[row][column].hole != "DONE":
                if not self.grid[row][column].activated:
                    pyxel.blt(shovel.x,shovel.y,0,128,shovel.sprite[1],16,16,0)
                else:
                    pyxel.blt(shovel.x,shovel.y,0,shovel.sprite[0],shovel.sprite[1],16,16,0)
        
        # Drawing the cursor
        pyxel.blt(self.curX,self.curY,0,0,48,16,16,0)
        
        # Starting screen:
        if not self.start:
            pyxel.cls(0)
            pyxel.text(92,127,"PRESS P TO START",7)
            pyxel.blt(70,120,0,80,16,16,16,0)
            pyxel.blt(160,120,0,80,0,16,16,0)
        
        
        # Game Over screen:
        if self.score.alive == 0 and (self.score.dead + self.score.saved) == self.maxLemmings:
            pyxel.cls(0)
            pyxel.blt(7,110,2,0,0,260,23,0)
            for e in range(2):
                for i in range(16):
                    pyxel.blt(16*i,16*e,0,0,64,16,16,0)
                    
            for e in range(14,16):
                for i in range(16):
                    pyxel.blt(16*i,16*e,0,0,64,16,16,0)
                    
            pyxel.text(60,150,"STATISTICS:",7)
            pyxel.text(120,150,"SAVED:"+str(self.score.saved),7)
            pyxel.text(170,150,"DEAD:"+str(self.score.dead),7)
    
    # Function to set game logics
    def update(self):
        # Exit key
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Creating the lemmings
        if self.start:
            if self.countInvoked < self.maxLemmings:
                if pyxel.frame_count % 25 == 0:       
                        lemming = Lemming(self.portals[0].x,self.portals[0].y,"Right",[0,0],"NO",0,True,False,False,False)
                        self.lemmings.append(lemming)
                        self.score.putLemming()
                        self.countInvoked += 1
        
        # Movement of the lemmings     
        for lemming in self.lemmings: 
            pyxel.frame_count % 50
            row = int(lemming.y/16)
            column = int((lemming.x)/16)

            # Controlling the sprites and screen limits when moving to the left      
            if lemming.direction == "Left":
                if lemming.x == 240 or lemming.x == 0:
                    lemming.turn()
                    if lemming.sprite[1] == 0:
                        lemming.sprite[1] = 16
                    else:
                        lemming.sprite[1] = 0
                if (column) > 0:
                    if self.grid[row][column].full == "P" or self.grid[row][column].full == "B":
                        lemming.turn()
                        if self.grid[row][column].full == "B":
                            self.grid[row][column].activated = True
                        if lemming.sprite[1] == 0:
                            lemming.sprite[1] = 16
                        else:
                            lemming.sprite[1] = 0    

            # Controlling the sprites and screen limits when moving to the right       
            elif lemming.direction == "Right":
                if lemming.x == 240 or lemming.x == 0:
                    lemming.turn()
                    if lemming.sprite[1] == 0:
                        lemming.sprite[1] = 16
                    else:
                        lemming.sprite[1] = 0
                if (column+1) < 16:   
                    if self.grid[row][column+1].full == "P" or self.grid[row][column].full == "B":
                        lemming.turn()
                        if self.grid[row][column].full == "B":
                            self.grid[row][column].activated = True
                        if lemming.sprite[1] == 0:
                            lemming.sprite[1] = 16
                        else:
                            lemming.sprite[1] = 0             
        
        # Gravity        
        for lemming in self.lemmings:
            row = int(lemming.y/16)
            column = int((lemming.x+8)/16)
            
            # If the lemming is not at ground level, it might fall
            if (row+1) < 16:
                # If nothing is below the lemming it will start falling
                if self.grid[row+1][column].full == "" or self.grid[row+1][column].full == "U" or ((self.grid[row+1][column].full == "LL" or self.grid[row+1][column].full == "RL") and self.grid[row+1][column].ladderDone != "DONE"):
                    if self.grid[row+1][column].full == "U":
                        self.grid[row+1][column].activated = True
                    if lemming.direction == "Left":
                        lemming.direction = "Down-Left"
                        lemming.x -= 2
                    elif lemming.direction == "Right":
                        lemming.direction = "Down-Right"
                        lemming.x += 2

                # If there is a platform or a blocker, the lemming can walk over it        
                elif self.grid[row+1][column].full == "P" or self.grid[row+1][column].full == "S":
                    if lemming.direction == "Down-Left":
                        lemming.direction = "Left"
                    elif lemming.direction == "Down-Right":
                        lemming.direction = "Right"
                
                # If there is a ladder, the lemming will not fall
                elif self.grid[row+1][column].full == "RL" or self.grid[row+1][column].full == "LL":
                    if lemming.direction == "Down-Left":
                        lemming.direction = "Left"
                    elif lemming.direction == "Down-Right":
                        lemming.direction = "Right"
            
            # If it reaches the bottom it stops falling
            elif (row+1) >= 16:
                if lemming.direction == "Down-Left":
                    lemming.direction = "Left"
                elif lemming.direction == "Down-Right":
                    lemming.direction = "Right"

            # Move the lemming once with the new direction   
            lemming.move()

            # If the lemming is falling, we will count the frames it has been falling unless it crossed an umbrella  
            if lemming.direction == "Down-Left" or lemming.direction == "Down-Right":
                    if self.grid[row][column].full == "U":
                        lemming.hasUmbrella = True 
                    if lemming.hasUmbrella:
                        if lemming.direction == "Down-Right":
                            lemming.sprite[0] = 80
                            lemming.sprite[1] = 0
                        elif lemming.direction == "Down-Left":
                            lemming.sprite[0] = 80
                            lemming.sprite[1] = 16
                    lemming.fallCount += 1
            
            # If the direction changes to left or right and the fall counter is over 32, the lemming dies without an umbrella
            elif lemming.direction == "Left" or lemming.direction == "Right":
                if lemming.fallCount > 32 and not lemming.hasUmbrella:
                    lemming.living = False
                    self.lemmingGone()
                    self.score.eliminateLemming()
                    self.score.deadLemming()
                    lemming.fallCount = 0
                else:
                    lemming.fallCount = 0
                    lemming.hasUmbrella = False
            
            # If a lemming touches the finish portal, it is removed and counts as saved
            if self.grid[row][column].finishPortal:
                lemming.living = False
                self.lemmingGone()
                self.score.eliminateLemming()
                self.score.savedLemming()
        
        # Code to dig holes
        for lemming in self.lemmings:
            row = int(lemming.y/16)
            column = int((lemming.x+8)/16)
            if (row+1) < 16:
                if self.grid[row+1][column].full == "S":
                    self.grid[row+1][column].activated = True
                    
                    # Controlling the different states of the hole digging
                    if self.grid[row+1][column].hole == "NO" and not lemming.dugHole:
                        self.grid[row+1][column].hole = "1"
                        lemming.dugHole = True
                        
                    elif self.grid[row+1][column].hole == "1" and not lemming.dugHole:
                        self.grid[row+1][column].hole = "2"
                        lemming.dugHole = True
                        
                    elif self.grid[row+1][column].hole == "2" and not lemming.dugHole:
                        self.grid[row+1][column].hole = "3"
                        lemming.dugHole = True
                        
                    elif self.grid[row+1][column].hole == "3" and not lemming.dugHole:
                        self.grid[row+1][column].hole = "DONE"
                        self.grid[row+1][column].full = ""
                        
                else:
                    lemming.dugHole = False
                        
        # Check if a lemming has to go up or down a ladder and build them
        for lemming in self.lemmings:
            row = int(lemming.y/16)
            rowL = int((lemming.y+15)/16)
            columnL = int((lemming.x+8)/16)    
            
            if (row+1) < 16:
                if self.grid[rowL][columnL].full == "RL" and lemming.direction == "Right":
                    
                    # Controlling the different states of ladder building
                    if self.grid[rowL][columnL].ladderDone == "NO" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "1"
                        self.grid[rowL][columnL].activated = True
                        lemming.builtLadder = True
                        
                    elif self.grid[rowL][columnL].ladderDone == "1" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "2"
                        lemming.builtLadder = True
                        
                    elif self.grid[rowL][columnL].ladderDone == "2" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "3"
                        lemming.builtLadder = True
                    
                    elif self.grid[rowL][columnL].ladderDone == "3" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "4"
                        lemming.builtLadder = True
                    
                    elif self.grid[rowL][columnL].ladderDone == "4" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "DONE"
                        lemming.builtLadder = True
                        
                    elif self.grid[rowL][columnL].ladderDone == "DONE":
                        lemming.climb = "UP"
                        lemming.climbUp()
                        
                elif self.grid[rowL][columnL].full == "LL" and lemming.direction == "Left":
                    
                    # Controlling the different states of ladder building
                    if self.grid[rowL][columnL].ladderDone == "NO" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "1"
                        self.grid[rowL][columnL].activated = True
                        lemming.builtLadder = True
                        
                    elif self.grid[rowL][columnL].ladderDone == "1" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "2"
                        lemming.builtLadder = True
                        
                    elif self.grid[rowL][columnL].ladderDone == "2" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "3"
                        lemming.builtLadder = True
                    
                    elif self.grid[rowL][columnL].ladderDone == "3" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "4"
                        lemming.builtLadder = True
                    
                    elif self.grid[rowL][columnL].ladderDone == "4" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "DONE"
                        lemming.builtLadder = True
                        
                    elif self.grid[rowL][columnL].ladderDone == "DONE":
                        lemming.climb = "UP"
                        lemming.climbUp()
                
                # If the ladder if built, it will work along the whole block
                elif self.grid[row+1][columnL].full == "RL" and lemming.direction == "Left" and self.grid[row+1][columnL].ladderDone == "DONE":
                    lemming.climb = "DOWN"
                    self.grid[row+1][columnL].activated = True
                    lemming.goDown()
                elif self.grid[row+1][columnL].full == "LL" and lemming.direction == "Right" and self.grid[row+1][columnL].ladderDone == "DONE":
                    lemming.climb = "DOWN"
                    self.grid[row+1][columnL].activated = True
                    lemming.goDown()
                else:
                    lemming.climb = "NO"
                    lemming.builtLadder = False
            else:
                # Lemming can't use a ladder to go down if it is at the bottom
                if self.grid[rowL][columnL].full == "RL" and lemming.direction == "Right":

                    # Controlling the different states of ladder building
                    if self.grid[rowL][columnL].ladderDone == "NO" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "1"
                        self.grid[rowL][columnL].activated = True
                        lemming.builtLadder = True
                        
                    elif self.grid[rowL][columnL].ladderDone == "1" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "2"
                        lemming.builtLadder = True
                        
                    elif self.grid[rowL][columnL].ladderDone == "2" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "3"
                        lemming.builtLadder = True
                    
                    elif self.grid[rowL][columnL].ladderDone == "3" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "4"
                        lemming.builtLadder = True
                    
                    elif self.grid[rowL][columnL].ladderDone == "4" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "DONE"
                        lemming.builtLadder = True
                        
                    elif self.grid[rowL][columnL].ladderDone == "DONE":
                        lemming.climb = "UP"
                        lemming.climbUp()
                        
                elif self.grid[rowL][columnL].full == "LL" and lemming.direction == "Left":
                    # Controlling the different states of ladder building
                    if self.grid[rowL][columnL].ladderDone == "NO" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "1"
                        self.grid[rowL][columnL].activated = True
                        lemming.builtLadder = True
                        
                    elif self.grid[rowL][columnL].ladderDone == "1" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "2"
                        lemming.builtLadder = True
                        
                    elif self.grid[rowL][columnL].ladderDone == "2" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "3"
                        lemming.builtLadder = True
                    
                    elif self.grid[rowL][columnL].ladderDone == "3" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "4"
                        lemming.builtLadder = True
                    
                    elif self.grid[rowL][columnL].ladderDone == "4" and not lemming.builtLadder:
                        self.grid[rowL][columnL].ladderDone = "DONE"
                        lemming.builtLadder = True
                        
                    elif self.grid[rowL][columnL].ladderDone == "DONE":
                        lemming.climb = "UP"
                        lemming.climbUp()
                else:
                    lemming.climb = "NO"
                    lemming.builtLadder = False
                    
        # Animating the lemmings changing the sprite  
        for lemming in self.lemmings:
            if pyxel.frame_count % 4 == 0:
                if lemming.direction == "Right":
                    lemming.sprite[1] = 0
                    if lemming.sprite[0] == 80:
                        lemming.sprite[0] = 0
                    elif lemming.sprite[0] == 0:
                        lemming.sprite[0] = 16
                    elif lemming.sprite[0] == 16:
                        lemming.sprite[0] = 32
                    elif lemming.sprite[0] == 32:
                        lemming.sprite[0] = 48
                    elif lemming.sprite[0] == 48:
                        lemming.sprite[0] = 0
                    
                elif lemming.direction == "Left":
                    lemming.sprite[1] = 16
                    if lemming.sprite[0] == 80:
                        lemming.sprite[0] = 0
                    elif lemming.sprite[0] == 0:
                        lemming.sprite[0] = 16
                    elif lemming.sprite[0] == 16:
                        lemming.sprite[0] = 32
                    elif lemming.sprite[0] == 32:
                        lemming.sprite[0] = 48
                    elif lemming.sprite[0] == 48:
                        lemming.sprite[0] = 0
                
        # Key to start the game
        if pyxel.btnp(pyxel.KEY_P):
            self.start = True           
         
        # Moving the cursor
        if pyxel.btnp(pyxel.KEY_RIGHT):
            if self.curX < 240:
                self.curX += 16
        
        if pyxel.btnp(pyxel.KEY_LEFT):
            if self.curX > 0:
                self.curX -= 16
            
        if pyxel.btnp(pyxel.KEY_UP):
            if self.curY > 32:
                self.curY -= 16
            
        if pyxel.btnp(pyxel.KEY_DOWN):
            if self.curY < 240:
                self.curY += 16
            
        # Key setting to place the right ladders    
        if pyxel.btnp(pyxel.KEY_D):
            row = int(self.curY/16)
            column = int(self.curX/16)
            if self.grid[row][column].full == "" and self.score.ladders < self.maxLadders:
                self.rightLadder()
                self.score.putLadder()
            elif self.grid[row][column].full == "RL":
                if not self.grid[row][column].activated:
                    self.removeLadder()
                    self.score.eliminateLadder()
                else:
                    self.grid[row][column].activated = False
                    self.removeLadder()
                
                self.grid[row][column].ladderDone = "NO"

        # Key setting to place the left ladders    
        if pyxel.btnp(pyxel.KEY_A):
            row = int(self.curY/16)
            column = int(self.curX/16)
            if self.grid[row][column].full == "" and self.score.ladders < self.maxLadders:
                self.leftLadder()
                self.score.putLadder()
            elif self.grid[row][column].full == "LL":
                if not self.grid[row][column].activated:
                    self.removeLadder()
                    self.score.eliminateLadder()
                else:
                    self.grid[row][column].activated = False
                    self.removeLadder()
                    
                self.grid[row][column].ladderDone = "NO"

        # Key to place the umbrellas
        if pyxel.btnp(pyxel.KEY_W):
            row = int(self.curY/16)
            column = int(self.curX/16)
            if self.grid[row][column].full == "" and self.score.umbrellas < self.maxUmbrellas:
                self.placeUmbrella()
                self.score.putUmbrella()
            elif self.grid[row][column].full == "U":
                if not self.grid[row][column].activated:
                    self.removeUmbrella()
                    self.score.eliminateUmbrella()
                else:
                    self.grid[row][column].activated = False
                    self.removeUmbrella()

        # Key to place the blockers
        if pyxel.btnp(pyxel.KEY_S):
            row = int(self.curY/16)
            column = int(self.curX/16)
            if self.grid[row][column].full == "" and self.score.blockers < self.maxBlockers:
                self.placeBlocker()
                self.score.putBlocker()
            elif self.grid[row][column].full == "B":
                if not self.grid[row][column].activated:
                    self.removeBlocker()
                    self.score.eliminateBlocker()
                else:
                    self.grid[row][column].activated = False
                    self.removeBlocker()

        # Key to place the shovels           
        if pyxel.btnp(pyxel.KEY_X):
            row = int(self.curY/16)
            column = int(self.curX/16)
            if self.grid[row][column].full == "P" and self.score.shovels < self.maxShovels:
                self.placeShovel()
                self.score.putShovel()
            elif self.grid[row][column].full == "S":
                if not self.grid[row][column].activated:
                    self.removeShovel()
                    self.score.eliminateShovel()
                else:
                    self.grid[row][column].activated = False
                    self.removeShovel()
                    
        # Key to kill all the lemmings in game         
        if pyxel.btnp(pyxel.KEY_R):
            self.score.dead = self.score.dead + self.score.alive
            self.score.alive = 0
            self.lemmings = []

# App execution
App()
