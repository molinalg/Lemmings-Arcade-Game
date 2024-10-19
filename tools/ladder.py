"""
-----LADDER CLASS-----

This class defines the ladders present in the game which can be of 2 types: Right or Left

"""
class Ladder:
    # Coordinates X and Y of one extreme of the ladder
    __coordX = 0 
    __coordY = 0
    
    # Direction the ladder points to
    __direction = "Right"
    
    # Name of the script to use for the ladder
    __sprite = []
    
    def __init__(self,x,y,direction,sprite):
        # Initializing the attributes
        self.__coordX = x
        self.__coordY = y
        self.__direction = direction
        self.__sprite = sprite
        
    # We specify the property of the coordinate x
    @property
    def x(self):
        return self.__coordX
    
    # We set the value of x
    @x.setter
    def x(self,value):
        self.__coordX = value
            
    # We specify the property of the coordinate y
    @property
    def y(self):
        return self.__coordY
    
    # We set the value of y
    @y.setter
    def y(self,value):
        self.__coordY = value
    
    # We specify the property of the sprite
    @property
    def sprite(self):
        return self.__sprite
    
    # We set the value of the sprite
    @sprite.setter
    def sprite(self,value):
        self.__sprite = value
