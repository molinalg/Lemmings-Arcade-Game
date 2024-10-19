"""
-----SCORE CLASS-----

This class defines the score of the game which is used to keep track of the number of lemmings saved, dead, alive and the tools used.

"""
class Score:
    # Initial values of each field in the score
    __level = 1
    __alive = 0
    __saved = 0
    __dead = 0
    
    __ladders = 0
    __umbrellas = 0
    __blockers = 0
    __shovels = 0
    
    def __init__(self,level,alive,saved,dead,ladders,umbrellas,blockers,shovels):
        # Initializing the attributes
        self.__level = level
        self.__alive = alive
        self.__saved = saved
        self.__dead = dead
        self.__ladders = ladders
        self.__umbrellas = umbrellas
        self.__blockers = blockers
        self.__shovels = shovels
    
    # Properties of the attributes and setting them
    @property
    def level(self):
        return self.__level
    
    @level.setter
    def level(self,value):
        self.__level = value
    
    @property
    def alive(self):
        return self.__alive
    
    @alive.setter
    def alive(self,value):
        self.__alive = value
    
    @property
    def saved(self):
        return self.__saved
    
    @saved.setter
    def saved(self,value):
        self.__saved = value
    
    @property
    def dead(self):
        return self.__dead
    
    @dead.setter
    def dead(self,value):
        self.__dead = value
    
    @property
    def ladders(self):
        return self.__ladders
    
    @ladders.setter
    def ladders(self,value):
        self.__ladders = value
    
    @property
    def umbrellas(self):
        return self.__umbrellas
    
    @umbrellas.setter
    def umbrellas(self,value):
        self.__umbrellas = value
        
    @property
    def blockers(self):
        return self.__blockers
    
    @blockers.setter
    def blockers(self,value):
        self.__blockers = value
    
    @property
    def shovels(self):
        return self.__shovels
    
    @shovels.setter
    def shovels(self,value):
        self.__shovels = value
    
    # Methods to add and eliminate things from the score
    def putLemming(self):
        self.__alive += 1
        
    def eliminateLemming(self):
        self.__alive -= 1
    
    def deadLemming(self):
        self.__dead += 1
        
    def savedLemming(self):
        self.__saved += 1

    def putLadder(self):
        self.__ladders += 1
        
    def eliminateLadder(self):
        self.__ladders -= 1
    
    def putUmbrella(self):
        self.__umbrellas += 1
        
    def eliminateUmbrella(self):
        self.__umbrellas -= 1
    
    def putBlocker(self):
        self.__blockers += 1
        
    def eliminateBlocker(self):
        self.__blockers -= 1
        
    def putShovel(self):
        self.__shovels += 1
        
    def eliminateShovel(self):
        self.__shovels -= 1
