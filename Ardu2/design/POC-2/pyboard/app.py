#!/usr/local/bin/python3.4
# app.py
# provides classes for the application level.
# This is where all the user interface calls are found!

from bitMgr import BitMgr
from components import Invertable,VTable
from state import State
from spiMgr import SPIMgr
from configs import configDict,mapReplace
import pyb

class App():
    """
    This class is the top level user facing application class.
    A single instance should be created and maintained during execution.
    The instance will maintain the user readable component classes as well
    as manage the Bits and SPI interfacing.
    usage:
    a = App()
    a.set(...)
    a.connect(...)
    a.x()
    details:
    >>> from app import App
    >>> a = App()
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	0
	set: LOW
        send:	0b0
        ...
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	1
	set: HIGH
    >>> from state import State
    >>> a.set('A',State.Vol,State.l5)
    masking:  ['4', '0b11000000']
    setting: (4, 5)
    currentConfig:	
    ...
    >>> >>> a.connect('A',0,'B',1)
    setting: (0, 1)
    currentConfig:
    ...
    >>> a.x()
    setting: None
    currentConfig:
    ...
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	0
	set: LOW
        send:	0b10
        ...
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	1
	set: HIGH
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
        """
        self.bitMgr = BitMgr()
        self.state = State()
        self.resetConnections = True
        self.coils = {}
        for coil in State.coils[:-1]:
            self.coils[coil] = Invertable(coil)
        self.coils[State.coils[-1]]= VTable(State.coils[-1])
        self.spiMgr = SPIMgr(State.spiOnX,State.spiLatchPinName)
        # turn all to State.lOff
        self.spiMgr.update(self.bitMgr.cnConfig[BitMgr.cur])
        """

    def reset(self):
        self.bitMgr = BitMgr()
        self.state = State()
        self.resetConnections = True
        self.coils = {}
        for coil in State.coils[:-1]:
            self.coils[coil] = Invertable(coil)
        self.coils[State.coils[-1]]= VTable(State.coils[-1])
        self.spiMgr = SPIMgr(State.spiOnX,State.spiLatchPinName)
        # turn all to State.lOff
        self.spiMgr.update(self.bitMgr.cnConfig[BitMgr.cur])
        

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
        self.softX()
        for coil in self.coils.values():
            coil.x()
        self.bitMgr.x()
        #send bits!
        #self.spiMgr.update(self.bitMgr.cnConfig[BitMgr.cur])
        self.resetConnections = False

    def softX(self):
        """
        This version of the method does the following:
        * sends the new bits ORed with the current bits,
        * waits for the makeBeforeBreakDelay
        * sends the new bits
        usage:
        >>> a.softX()
        """
        self.spiMgr.update(map(lambda x,y: x|y,
                               self.bitMgr.cnConfig[BitMgr.cur],
                               self.bitMgr.cnConfig[BitMgr.nex]))
        #pyb.delay(self.state.makeBeforeBreakDelay)
        self.spiMgr.update(self.bitMgr.cnConfig[BitMgr.nex])


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
    


