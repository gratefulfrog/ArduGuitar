#!/usr/local/bin/python3.4
# state.py
# 2016 05 30 added Vibrato and Tremolo, then removed it since all the dependencies need to be updated
# 2016 06 06 changed nbShiftRegs to 19 so as to integrate HMI LEDs; added pusbutton colors

class State():
    """
    This class contains all static information required to operate
    the system. 
    These may be technical or domain data.
    Debugging tools are found here.
    Examples:
    - config date for the hardware
    - names used in the system at any leve, e.g. coil names, like 'A'
    The class usage:
    >> from state import State
    >> s = State()
    Then the class variables can be accessed:
    >> print(s.lOff)
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

    # no longer used 2015 12 09
    # vactrol control pin
    #vactrolPinName = 'X4'
    
    # Shift Register info
    # updated to handle 14 Max395s + 5 ShiftRegs for the LED displays
    #nbShiftRegs = 14  # i.e. on [0,13[  from stand alone version of code
    nbShiftRegs = 19  # i.e. on [0,18[
    nbSwitchRegs = 4
    connectionUpdateOnly = 1010

    # Make before Break delay in milliseconds 
    # for quieter switching, hopefully..
    makeBeforeBreakDelay = 5
    
    lOff = None
    l0  = 0
    l1  = 1
    l2  = 2
    l3  = 3
    l4  = 4
    l5  = 5

    # PB Colors
    RED    = 100
    YELLOW = 101
    GREEN  = 102
    BLUE   = 103
    
    Inverter  = -1
    Vol	      = -2
    Tone      = -3
    ToneRange = -4
    #Tremolo   = -5
    #Vibrato   = -6
    
    debug = True #False

    def printT(*thing):
        """ depending on State.debug, print or not
        """
        if State.debug:
            print(thing) 
    
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
