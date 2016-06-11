#!/usr/local/bin/python3.4
# app.py
# provides classes for the application level.
# This is where all the user interface calls are found!

#from vactrolControl import vactrolControl
from bitMgr import BitMgr
from dictMgr import shuntConfDict
from components import Invertable,VTable,OnOffable
from state import State
from spiMgr import SPIMgr
from configs import configDict,mapReplace
from hardware import ShuntControl,LcdDisplay
import pyb

class App():
    """
    This class is the top level user facing application class.
    A single instance should be created and maintained during execution.
    The instance will maintain the user readable component classes as well
    as manage the Bits and SPI interfacing.
    usage:
    from app import App
    from state import State
    a = App()
    a.set(...)
    a.connect(...)
    a.x()
    details:
    >>> from app import App
    >>> a = App()
    >>> from state import State
    >>> a.set('PB',State.Vibrato,State.l0)
    (0, 5) ((0, 223),)
    ('masking: ', ['0', '0b11011111'])
    ('setting: (0, 5)',)
    >>> a.set('PB',State.Tremolo,State.l0)
    (0, 6) ((0, 191),)
    ('masking: ', ['0', '0b10111111'])
    ('setting: (0, 6)',)
    >>> a.x()
    xxxxxxxxxxx6543210
    ('send:\t0b1100000',)

    >>> a.set('A',State.Vol,State.l5)
    ((10, 7), (4, 5), (4, 7)) ((10, 3), (4, 31))
    ('masking: ', ['10', '0b11'])
    ('masking: ', ['4', '0b11111'])
    ('setting: ((10, 7), (4, 5), (4, 7))',)

    >>> a.connect('A',0,'B',1)
    ('setting: (8, 2)',)
    
    >>> a.x()
    setting: None
    ...

    >>> 
    """
    def __init__(self):
        """
        Instance creation; creation of member variables which are
        mainly instances of supporting classes.
        some details
        - resetConnections: boolean True if the connections have been reset
                            False, if they need to be reset before any new
                            connections are added.
        - coils is a vector: first is the Master-out, then coils A through D:
          [VTable, Ivertable, Ivertable, Ivertable, Ivertable]
        also,
        after creation of the SPIMgr, the update message is sent to it to 
        initialize all the pins.
        """
        self.reset()

    def reset(self):
        self.shuntControl = ShuntControl(shuntConfDict)
        self.bitMgr = BitMgr()
        self.state = State()
        self.resetConnections = True
        self.coils = {}
        for coil in State.coils[:-1]:
            self.coils[coil] = Invertable(coil)
        self.coils[State.coils[-1]]= VTable(State.coils[-1])
        self.coils[State.pb] = OnOffable()
        self.spiMgr = SPIMgr(State.spiOnX,State.spiLatchPinName)
        self.lcd = LcdDisplay(State.lcdConfDict)
        # shunt, turn all to State.lOff, unshunt
        self.shuntControl.shunt()
        self.spiMgr.update(self.bitMgr.cnConfig[BitMgr.cur])
        self.shuntControl.unShunt()

    def set(self,name,att,state):
        """
        This is called to set a coil's V or T or TR or I attribute to 
        the state argument.
        It simply looks up the instance in the coils vector and applies
        the coil's method with the state given as argument. Note that 
        the attribute is converted to an index to be passed to the coil's
        setFuncs vector to find the correct method to call.
        Once the user representation is updated, the bitMgr is called
        with the same arguments to update the NEXT bit vectors.
        usage:
        >>> a.set('M',State.Vol,State.l0)
        """
        self.coils[name].setFuncs[State.stateNeg2SetFuncIndex(att)](state)
        self.bitMgr.update(name,att,state)

    def connect(self,name,pole,otherName,otherPole):
        """
        Similar to the set method, this method calls the coil's connect
        method with the arguments as given. Then the bit representation
        is updated with the same arguments.
        The subtlty here is that if the connections have not yet been reset,
        i.e. if self.resetConnections is False, then the connections must be 
        set to 0 in the NEXT bit vector. This is only done once per updating 
        session. That means that the connections are reset, then n number of
        connection updates are applied, then the updates are exectued, 
        and only then will the NEXT vector be reset.
        """
        if not self.resetConnections:
            # if the connections have not been reset, then reset just
            # the switches part of the NEXT vector
            self.bitMgr.reset(BitMgr.switchRegEndPoints, 
                              curBool=False,
                              nexBool=True)
            self.resetConnections = True
        self.coils[name].connect(pole,(otherName,otherPole))
        self.bitMgr.update((name,pole),
                           (otherName,otherPole))

    def x(self):
        """
        This method calls the x() method on each of the coils, then on the
        bitMgr, then sends the bits to the spiMgr for hardware updating, and
        finally assigns 'False' to the resetConnections member in view of 
        future connection updates.
        usage:
        >>> a.x()
        """
        for coil in self.coils.values():
            coil.x()
        self.bitMgr.x()
        # shunt
        self.shuntControl.shunt()
        #send bits!
        self.spiMgr.update(self.bitMgr.cnConfig[BitMgr.cur])
        #unshunt
        self.shuntControl.unShunt()
        self.resetConnections = False
      
    def loadConfig(self,confName):
        """ loads a predefined configuration.
        Arg 0 : the name of the conf to load, for lookup in configDict
        Note:
        - this resets next bitMgr config and each coils next config
          before beginning since there is no 'addition' of settings here
        - it also resets all the coils connection and vtri values prior
          to executing.
        """
        self.bitMgr.reset(BitMgr.allRegEndPoints,
                          curBool=False,
                          nexBool=True)
        for coil in self.coils.values():
            coil.resetNext()
        for expr in mapReplace('self',
                               configDict[confName]):
            State.printT('Evalutating:\t' + expr)
            eval(expr , globals(),{'self':self})
        self.x()

    def showConfig(self):
        print(self.bitMgr)

    def lcdSetLine(self, lineNb, line):
        print('Setting LCD Line:\t%d\t"%s"'%(lineNb, line))
        self.lcd.setLn(lineNb, line)


