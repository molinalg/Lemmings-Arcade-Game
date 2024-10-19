"""
-----SHOVEL CLASS-----

This class is used to create the shovel that will be used in the game, lemmings will dig start digging a hole in a platform if the walk over the shovel it is placed on.

"""
class Shovel:
    # Coordinates X and Y of the shovel
    __coordX = 100
    __coordY = 100

    # Coordinates of the sprite
    __sprite = []
    
    def __init__(self,x,y,sprite):
        # Initializing the attributes
        self.__coordX = x
        self.__coordY = y
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
