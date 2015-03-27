#!/usr/local/bin/python3.4
# state.py 

class State():
    """
    This class contains all static information required to operate
    the system. 
    These may be technical or domain data.
    Examples:
    - config date for the hardware
    - names used in the system at any leve, e.g. coil names, like 'A'
    The class usage:
    >> from state import State
    >> s = State()
    Then the class variables can be accessed:
    >> print(s.off)
    None
    >> s.coils
    ['A', 'B', 'C', 'D', 'M']
    >>
    etc.
    """
    
    # SPI state for pyboard setup
    # define the latching pin
    spiLatchPinName = 'X5'
    # say which side of the pyboard are we using
    spiOnX = True
    
    # Shift Register info
    nbShiftRegs = 13  # i.e. on [0,13[
    nbSwitchRegs = 4
    connectionUpdateOnly = 1010
    
    off = None
    l0  = 0
    l1  = 1
    l2  = 2
    l3  = 3
    l4  = 4
    l5  = 5
    
    Inverter  = -1
    Vol	      = -2
    Tone      = -3
    ToneRange = -4
    
    def stateNeg2SetFuncIndex(stateNeg):
        """
        Static method converts one fo the above negative indices into
        a zero based index for use in the component classes
        """
        return abs(stateNeg)-1
    
    coils = ['A','B','C','D','M']
    poles = []
    
    def __init__(self):
        for c in State.coils:
            State.poles += [(c,0),]
            State.poles += [(c,1),]