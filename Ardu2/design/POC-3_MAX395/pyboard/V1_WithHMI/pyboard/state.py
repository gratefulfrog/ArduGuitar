#!/usr/local/bin/python3.4
# state.py
# 2016 05 30 added Vibrato and Tremolo, then removed it since all the dependencies need to be updated
# 2016 06 06 changed nbShiftRegs to 19 so as to integrate HMI LEDs; added pusbutton colors and 'PB' id
# 2016 06 10-30 : added new dits for integration of HMI
# 2016 09 04: update pin mappings after conflict issues
# 2016 09 13: updates for I2C LCD and new pin map for TracBall
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
    # debugging switches and methods
    debug = True #False # True
    tvPoll = True
    spaPoll = True
    
    def printT(*thing):
        """ depending on State.debug, print or not
        """
        if State.debug:
            #res = ''
            for t in thing:
                #res += str(t)
                print(t)
            #print(res)
    """
    # for 6Wire version
    lcdConfDict = {'rs_pin'      : 'X18',
                   'enable_pin'  : 'Y7',
                   'd4_pin'      : 'Y8',
                   'd5_pin'      : 'X22', # was X17 # was 'A15', #board.P3
                   'd6_pin'      : 'A14', #board.P4,
                   'd7_pin'      : 'A13', #board.P5,
                   'num_lines'   : 2,
                   'num_columns' : 16}
    """
    # for I2C version
    lcdConfDict = {'i2c_id'      : 1,
                   'i2c_addr'    : 0x20,
                   'num_lines'   : 2,
                   'num_columns' : 16}
    
    # dict maps a pin name string to tuple (line,id)
    pinNameDict = {'X19' :  (0,0),   # selector 0, pin a
                   'X20' :  (1,1),   # selector 0, pin b
                   'X21' :  (2,2),   # selector 0, pin c
                   'Y2'  :  (3,3),   # selector 1, pin a, was X22
                   'X11' :  (4,4),   # selector 1, pin b
                   'X12' :  (5,5),   # selector 1, pin c
                   'X7'  :  (6,2),   # TREM PB pb2
                   'X22' :  (7,3),   # VIB  PB  pb3 # was X17, was Y2
                   'Y3'  :  (8,0),   # TRACK/RED PB  pb0
                   'Y4'  :  (9,1),   # SAVE/YELLOW PB pb1
                   'Y9'  : (10,0),   # TrackBall X axis interrupt
                   'Y10' : (11,1),   # TrackBall Y axis interrupt
                   'Y5'  : (12,4),    # LCD LEFT PB pb4
                   'Y6'  : (13,5)     # LCD RIGHT PB pb5
                   }

    PBPinNameVec = ('Y3','Y4','X7','X22','Y5','Y6')

    SelectorPinNameArray = (('X19', 'X20', 'X21'), # horizontal
                            ('Y2', 'X11', 'X12')) # vertical
                   
    # trackball state data
    trackballStateDict = {'x1' : 'Y9',  # blue wire
                          'x2' : 'Y7',  # yellow wire
                          'y1' : 'Y10', # green wire
                          'y2' : 'Y8'}  # white wire

    splitPotPinNameVec = ('X1',  # 0: Master
                          'X2',  # 1: Coil A
                          'X3',  # 2: Coil B
                          'X4',  # 3: Coil C
                          'Y11', # 4: Coil D
                          'Y12') # 5: ToneRange
    splitPotCutOff               = 30
    splitPotSpacing              = 30
    splitPotTrackingError        = 250
    splitPotTrackingNbReads      = 5
    splitPotNoTrackingNbReadings = 10
    
    # SPI state for pyboard setup
    # define the latching pin
    spiLatchPinName = 'X5'
    # say which side of the pyboard are we using
    spiOnX = True
    
    # Shift Register info
    # updated to handle 14 Max395s + 5 ShiftRegs for the LED displays
    #nbShiftRegs = 14  # i.e. on [0,13[  from stand alone version of code
    nbShiftRegs = 19  # i.e. on [0,18[
    nbSwitchRegs = 4
    nbHIRegs = 5
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

    Inverter  = -1
    Vol	      = -2
    Tone      = -3
    ToneRange = -4
    Tremolo   = 101
    Vibrato   = 102
    Red       = 103
    Yellow    = 104

    vibratoLowerLimit      = l1
    vibratoUpperLimit      = l5
    tremoloLowerLimit      = l1
    tremoloUpperLimit      = l5

    AccpThreshold = 6 #5  # values for 1.5g Freescale accelerometer on [+31,-32]
    AccnThreshold = -6 #-5
    AccreadDelay = 20 # min interval between reads in milliseconds maybe try 5ms???
    AcctimeOut = 2000  # interval after which to call offFunc and turn off associated control

    HWDebounceDelay = 20 #ms
    
    def stateNeg2SetFuncIndex(stateNeg):
        """
        Static method converts one fo the above negative indices into
        a zero based index for use in the component classes
        """
        if stateNeg > 100:
            return 0
        else:
            return abs(stateNeg)-1
    
    coils = ['A','B','C','D','M']
    poles = []
    pb = 'PB'
    
    def __init__(self):
        for c in State.coils:
            State.poles += [(c,0),]
            State.poles += [(c,1),]
