"""
-----CELL CLASS-----

This class defines the cells present in the game which have their own attributes to store information about the board.

"""
class Cell:
    # Coordinates X and Y of the cell
    __coordX = 0 
    __coordY = 0
    
    # Attribute that shows what is inside a cell
    __full = ""
    
    # Chek if a portal is the finish line
    __finishPortal = False
    
    # Check if a tool has been activated
    __activated = False
    
    # Check how much of a ladder has been built
    __ladderDone = "NO"
    
    # Check how much has a hole been dug
    __hole = "NO"
    
    def __init__(self,x,y,full,finishPortal,activated,ladderDone,hole):
        # Initializing the attributes
        self.__coordX = x
        self.__coordY = y
        self.__full = full
        self.__finishPortal = finishPortal
        self.__activated = activated
        self.__ladderDone = ladderDone
        self.__hole = hole
    
    # We specify the property of the coordinate X
    @property
    def x(self):
        return self.__coordX
    
    # We set the value of x
    @x.setter
    def x(self,value):
        self.__coordX = value
        
        if value < 0 or value > 256:
            self.__coordX = 0
            
    # We specify the property of the coordinate Y
    @property
    def y(self):
        return self.__coordY
    
    # We set the value of y
    @y.setter
    def y(self,value):
        self.__coordY = value
        
        if value < 0 or value > 256:
            self.__coordY = 0        
    
    # We specify the property of the attribute full
    @property
    def full(self):
        return self.__full
    
    # We set the value of full
    @full.setter
    def full(self,value):
        self.__full = value

    # We specify the property of the attribute finishPortal
    @property
    def finishPortal(self):
        return self.__finishPortal
    
    # We set the value of finishPortal
    @finishPortal.setter
    def finishPortal(self,value):
        self.__finishPortal = value
        
    # We specify the property of the attribute activated  
    @property
    def activated(self):
        return self.__activated
    
    # We set the value of activated
    @activated.setter
    def activated(self,value):
        self.__activated = value
    
    # We specify the property of the attribute ladderDone
    @property
    def ladderDone(self):
        return self.__ladderDone
    
    # We set the value of ladderDone
    @ladderDone.setter
    def ladderDone(self,value):
        self.__ladderDone = value
    
    # We specify the property of the attribute hole
    @property
    def hole(self):
        return self.__hole
    
    # We set the value of hole
    @hole.setter
    def hole(self,value):
        self.__hole = value
