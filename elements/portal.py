"""
-----PORTAL CLASS-----

This class defines the portals present in the game used by the lemmings to spawn and despawn.

"""
class Portal:
    # Coordinates X and Y of the portal
    __coordX = 100
    __coordY = 100
    
    # Attribute to define the type of portal
    __function = "START"
    
    # Sprite coordinates:
    __sprite = []
    
    def __init__(self,x,y,function,sprite):
        # Initializing the attributes
        self.__coordX = x
        self.__coordY = y
        self.__function = function
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
        
    # We specify the property for the type of portal
    @property
    def function(self):
        return self.__function
    
    # We set the value of function
    @function.setter
    def function(self,value):
        self.__function = value
        
    # We specify the property of the sprite
    @property
    def sprite(self):
        return self.__sprite
    
    # We set the value of sprite
    @sprite.setter
    def sprite(self,value):
        self.__sprite = value
