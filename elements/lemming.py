"""
-----LEMMING CLASS-----

This class defines the characters present in the game which have their own attributes and functions to move and interact with the environment.

"""
class Lemming:
    # Coordinates X and Y of the Lemming
    __coordX = 0 
    __coordY = 240
    
    # Direction of the Lemming (Left or Right)
    __direction = "Right"
    
    # Coordinates of the sprites to use for the lemmings
    __sprite = []
    
    # Movement related attributes
    __climb = "NO"
    __fallCount = 0
    
    # Check if a lemming is alive
    __living = True
    
    # Check if a lemming has an umbrella
    __hasUmbrella = False
    
    # Control attributes for ladders and holes
    __builtLadder = False
    __dugHole = False
    
    def __init__(self,x,y,direction,sprite,climb,fallCount,living,hasUmbrella,builtLadder,dugHole):
        # Initializing the attributes
        self.__coordX = x
        self.__coordY = y
        self.__sprite = sprite
        self.__direction = direction
        self.__climb = climb
        self.__fall = fallCount
        self.__living = living
        self.__hasUmbrella = hasUmbrella
        self.__builtLadder = builtLadder
        self.__dugHole = dugHole
    
    # We specify the property of the coordinate X
    @property
    def x(self):
        return self.__coordX
    
    # We set the value of x
    @x.setter
    def x(self,value):
        self.__coordX = value
            
    # We specify the property of the coordinate Y
    @property
    def y(self):
        return self.__coordY
    
    # We set the value of y
    @y.setter
    def y(self,value):
        self.__coordY = value
            
    # We specify the property of the direction
    @property
    def direction(self):
        return self.__direction
    
    # We set the value of the direction
    @direction.setter
    def direction(self,value):
        self.__direction = value
    
    # Functions to define the direction and movement of the lemming
    def move(self):
        if self.__direction == "Right":
            self.__coordX = self.__coordX + 1
                
        elif self.__direction == "Left":
            self.__coordX = self.__coordX - 1
        
        elif (self.__direction == "Down-Left" or self.__direction == "Down-Right") and self.__hasUmbrella:
            self.__coordY += 0.5
            
        elif self.__direction == "Down-Left" or self.__direction == "Down-Right":
            self.__coordY += 1
            
    # Function to change the direction of the lemming           
    def turn(self):
        if self.__direction == "Left":
            self.__direction = "Right"
        elif self.__direction == "Right":
            self.__direction = "Left"
    
    # Function to create upper diagonal movement together with move()             
    def climbUp(self):
        self.__coordY -= 1
    
    # Function to create low diagonal movement together with move()    
    def goDown(self):
        self.__coordY += 1

    # We specify the property of the sprite
    @property
    def sprite(self):
        return self.__sprite
    
    # We set the value of the sprite
    @sprite.setter
    def sprite(self,value):
        self.__sprite = value
    
    # We specify the property of the climb attribute
    @property
    def climb(self):
        return self.__climb
    
    # We set the value of the climb attribute
    @climb.setter
    def climb(self,value):
        self.__climb = value
        
    # We specify the property of the fallCount attribute
    @property
    def fallCount(self):
        return self.__fallCount
    
    # We set the value of the fallCount attribute
    @fallCount.setter
    def fallCount(self,value):
        self.__fallCount = value
    
    # We specify the property that shows if the lemming is alive
    @property
    def living(self):
        return self.__living
    
    # We set the value of the living attribute
    @living.setter
    def living(self,value):
        self.__living = value
    
    # We specify the property that shows if the lemming has an umbrella
    @property
    def hasUmbrella(self):
        return self.__hasUmbrella
    
    # We set the value of the hasUmbrella attribute
    @hasUmbrella.setter
    def hasUmbrella(self,value):
        self.__hasUmbrella = value
    
    # We specify the property that shows if the lemming has built a part of a ladder in the cell it is in
    @property
    def builtLadder(self):
        return self.__builtLadder
    
    # We set the value of the builtLadder attribute
    @builtLadder.setter
    def builtLadder(self,value):
        self.__builtLadder = value
    
    # We specify the property that shows if the lemming has dug a part of a hole in the cell it is in
    @property
    def dugHole(self):
        return self.__dugHole
    
    # We set the value of the dugHole attribute
    @dugHole.setter
    def dugHole(self,value):
        self.__dugHole = value
