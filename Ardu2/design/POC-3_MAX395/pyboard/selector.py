# selector.py
# support for 3 or 5 ... position selector switches

class Selector:
    """ Usage:
    >> pinIds = ('X1','X2','X3')
    >> s = Selector([Pin(p, Pin.IN, Pin.PULL_DOWN) for p in pinIds])
    >> s.currentPostion
    3
    >> # move switch
    >> s.setPostion()
    >> s.currentPostion
    0
    -----
    wiring:
    common on switch to 3.3V
    position 0 side wire to pin 0
    position 2 side wire to pin 1
    position 4 side wire to pin 2
    """
    
    # this defines the switch position pin values
    # note: if a 3 position selector is used, then only the 'upper left' 3x2 part is used
    masterTable = [[1,0,0],  # position 0, i.e. left: left pin is HIGH
                   [1,1,0],  # position 1, i.e. left/middle: left and middle pins are HIGH
                   [0,1,0],  # position 2, i.e. middle: middle pin is HIGH
                   [0,1,1],  # position 3, i.e. middle/right: middle & right pins are HIGH
                   [0,0,1]]  # position 4, i.e. right: right pin is HIGH
    
    def __init__(self,pins):
        """create an instance of a 3 or 5 position switch connected to the 
        pins provided.
        Pins should be configured as Pin('X1', Pin.IN, Pin.PULL_DOWN)
        len(pins) should be 2, for 3 postions, 3, for 5 positions
        incorrect arguments raise exceptions
        """
        if len(pins) not in (2,3):
            raise Exception('invalid nb of pins', pins)
        self.pinLis = []
        for p in pins:
            self.pinLis += [p]
        nbPos = 2*len(pins) -1
        self.truthTable = [x[:len(pins)] for x in Selector.masterTable[:nbPos]]
        self.currentPosition = 0
        self.setPosition()  # reads the pin values and deduces current switch position
        
    def setPosition(self):
        """ reads the pin values and deduces current switch position
        in case of failure, exception is raised.
        """
        tLis  = [p.value() for p in self.pinLis]
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
            '\n\ttruthTable:\t' + str(self.truthTable)  + '\n'                    
