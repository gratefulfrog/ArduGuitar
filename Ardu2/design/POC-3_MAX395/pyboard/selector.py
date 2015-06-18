# selector.py
# support for 3 or 5 ... position selector switches

class Selector:
    masterTable = [[True,False,False],
                   [True,True,False],
                   [False,True,False],
                   [False,True,True],
                   [False,False,True]]

    
    def __init__(self,pins):
        """create an instance of a 3 or 5 position switch connected to the 
        pins provided. 
        len(pins) should be 2, for 3 postions, 3, for 5 positions
        incorrect arguments raise exceptions
        """
        if len(pins) not in (2,3):
            raise Exception('invalid nb of pins', pins, nbPos)
        self.pinLis = []
        for p in pins:
            self.pinLis += [p]
        nbPos = 2*len(pins) -1
        self.truthTable = [x[:len(pins)]  for x in Selector.masterTable[0:nbPos]]
        #self.setPosition(map(readVals,pins))
        
    def setPosition(self,tLis):
        """ argument list of pin values as read are matched
        to truth table values, if correspondance is found, index 
        of position is returned, else exception is raised.
        """
        if len(tLis) != len(self.truthTable[0]):
            raise Exception('wrong nb pins', tLis)
        i = 0
        found = False
        while not found:
            if all(map(lambda x,y: x==y,tLis,self.truthTable[i])):
                found = True
            else:
                i +=1
        if not found:
            raise Exception('position not found', tLis)
        self.currentPosition = i

    def __repr__(self):
        return 'Selector:' + \
            '\n\tpostion:\t' + str(self.currentPosition) +\
            '\n\tpinLis:\t' + str(self.pinLis) +\
            '\n\ttruthTable:\t' + str(self.truthTable)                       
