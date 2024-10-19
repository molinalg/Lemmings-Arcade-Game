"""
-----PLATFORM CLASS-----

This class defines the platforms present in the game over which the lemmings walk.

"""

class Platform:
    # Coordinates X and Y of the Platform:
    __coordX = 100
    __coordY = 100
    
    # Length of the platforms
    __length = 10

    # Coordinates of the sprite
    __sprite = []
    
    def __init__(self,x,y,length,sprite):
        # Initializing the attributes
        self.__coordX = x
        self.__coordY = y
        self.__length = length
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
        
    # We specify the property of the length
    @property
    def length(self):
        return self.__length
    
    # We set the value of the length
    @length.setter
    def length(self,value):
        self.__length = value
        
    # We specify the property of the sprite
    @property
    def sprite(self):
        return self.__sprite
    
    # We set the value of sprite
    @sprite.setter
    def sprite(self,value):
        self.__sprite = value
