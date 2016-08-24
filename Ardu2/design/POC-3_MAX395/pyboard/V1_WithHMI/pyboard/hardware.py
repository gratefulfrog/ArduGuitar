# hardware.py
# classes corresponding to physical objects in the system
# * ShuntControl
# * SelectorInterrupt  (added 2016 08 24)
# * HWDebouncedPushButton
# * ShakeControl (3-axis shake controller)
# * LCDDisplay (added 2016 06 11)
#### obsolete or unused ###
# * Selector
# * Illuminator
# * SWDebouncedPushbutton
# * IlluminatedPushbutton
# * VoltageDividerPot

#####

from pyb import millis, Pin, Timer, delay, Accel, LED, ADC, ExtInt
from pyb_gpio_lcd import GpioLcd
from dictMgr import shuntConfDict
from state import State
from q import EnQueueable

#import micropython
#micropython.alloc_emergency_exception_buf(100)

class ShuntControl:
    """simple class providing on/off functionality of a vactrol
    controlled by a pyboard bin.
    """
    def __init__(self, confData):
        p = Pin(confData['p'] , mode=Pin.OUT_PP)
        tim = Timer(confData['t'],freq=confData['f'])
        self.control = tim.channel(confData['c'],Timer.PWM, pin=p)
        self.control.pulse_width_percent(0)

    def shunt(self, percent = 20):
        State.printT('Shunting')
        self.control.pulse_width_percent(percent)

    def unShunt(self):
        State.printT('UNshunting')
        self.control.pulse_width_percent(0)

    def __repr__(self):
        return 'ShuntControl: ' + '\n\t'  \
            'Timer.channel:\t' + str(self.control)

# SelectorInterrupt
# support for 3 or 5 ... position selector switches
class SelectorInterrupt (EnQueueable):
    """ Usage:
    >> pinIds = ('X1','X2','X3')
    >> s = SelectorInterrupt(pinNames,id,q)   
    >> s.currentPostion
    3
    >> # move switch
    >> s.setPostion()
    >> s.currentPostion
    0
    -----
    wiring:
    common on switch to GND
    position 0 side wire to pin 0
    position 2 side wire to pin 1
    position 4 side wire to pin 2
    """
    
    # this defines the switch position pin values
    # note: it is a diction of dictionaries, where at the top level we have number of pins,
    # then at next level the mapping of pin values to positions
    masterDict = {2: {(0,1): 0,  # position 0, i.e. left: left pin is GND
                      (0,0): 1,  # position 1, i.e. middle: left and right pins are GND
                      (1,0): 2}, # position 2, i.e. right: right pin is GND
                  3: {(0,1,1): 0,  # position 0, i.e. left: left pin is GND
                      (0,0,1): 1,  # position 1, i.e. left/middle: left and middle pins are GND
                      (1,0,1): 2,  # position 2, i.e. middle: middle pin is GND
                      (1,0,0): 3,  # position 3, i.e. middle/right: middle & right pins are GND
                      (1,1,0): 4}} # position 4, i.e. right: right pin is GND
    
    def __init__(self,pinNames,id,q):
        """create an instance of a 3 or 5 position switch connected to the 
        pins provided.
        Pins should be configured as Pin('X1', Pin.IN, Pin.PULL_DOWN)
        len(pins) should be 2, for 3 postions, 3, for 5 positions
        incorrect arguments raise exceptions
        """
        EnQueueable.__init__(self,EnQueueable.CONF,q)
        if len(pinNames) not in (2,3):
            raise Exception('invalid nb of pins', pinNames)
        self.pinLis =  [Pin(p, Pin.IN, Pin.PULL_UP) for p in pinNames]
        nbPos = 2*len(pinNames) -1
        self.truthDict = SelectorInterrupt.masterDict[nbPos]
        self.id = id
        self.currentPosition = 0
        self.setPosition()  # reads the pin values and deduces current switch position
        self.extIntVec = [None for p in pinNames]
        for i in range(len(pins)):
            self.extIntVec[i]=ExtInt(pinNames[i],
                                     ExtInt.IRQ_RISING_FALLING,
                                     Pin.PULL_UP,
                                     self.callback)

    def callback(self,unusedLine):
        self.push(self.id)
        print('CONF:\t',self.id)
        
    def setPosition(self):
        """ reads the pin values and deduces current switch position
        in case of failure, exception is raised.
        """
        tLis  = [p.value() for p in self.pinLis]
        self.currentPosition = self.self.truthDict[tuple(tLis)]
        """
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
        """
        
    def __repr__(self):
        return 'Selector:' + \
            '\n\tpostion:\t' + str(self.currentPosition) +\
            '\n\tpinLis:\t' + str(self.pinLis) +\
            '\n\ttruthTable:\t' + str(self.truthDict)  + '\n'


# HWDebouncedPushButton
# uses interrupts and queueing to indicate a push
class HWDebouncedPushButton(EnQueueable):
    """
    an interrupt generating pushbutton, using the q to manage actions
    """
    def __init__(self,pinName,q):
        EnQueueable.__init__(self,EnQueueable.PB,q)
        self.extInt = ExtInt(pinName, ExtInt.IRQ_FALLING, Pin.PULL_UP, self.callback)
        self.id = State.pinNameDict[pinName][1]
        
    def callback(self,unusedLine):
        self.push(self.id)
        print('PB:\t',self.id)

    def __repr__(self):
        return 'HWDebouncedPushButton:\n  ID:\t%d\n%s'%(self.id,repr(self.extInt))

# PushButtonArray
# an array of HWDebouncedPushputton
class PushButtonArray():
    def __init__(self,q):
        self.pbVec = []
        for pinName in State.PBPinNameVec:
            self.pbVec.append(HWDebouncedPushButton(pinName,q))

    def __repr__(self):
        res = ''
        for pb in self.pbVec:
            res += repr(pb) +'\n'
        return res
                    

class ShakeControl1:
    """ 
    provides single axis shake control; when there is shake in the
    axis, then the appropriate toggle function is called.  IF there is no shake for
    a timeout period, then the appropriate off function is called.
    """

    pThreshold = 5  # values for 1.5g Freescale accelerometer on [+31,-32]
    nThreshold = -5
    readDelay = 20 # min interval between reads in milliseconds maybe try 5ms???
    timeOut = 2000  # interval after which to call offFunc and turn off associated control
    
    def __init__(self, readFunc, toggleFunc, offFunc,
                 pt=pThreshold,nt=nThreshold,rd=readDelay,to=timeOut):
        """ 
        Instance Creation:
        provides default values for thresholds, read delay, and timeout
        other args are:
         readFunc: will be called to read the value of the accelerometer
         toggleFunc: will be called when the value read is in a zone that is 
                     different from previous zone, but only if over a threshold
         offFunc: will be called in case of inactivity lasting for the timeout period
        baseVal: is used to cancel gravity in each axis, so the accelerometer will read
                 as if there were no gravity.
        prevZone: is the zone value from when we last read the accelerometer
        lastActionTime: is milis since a toggle or an off action was called
        lastReadTime: is millis since call to readFunc (failed or not)
        """
        self.rf = readFunc
        self.tf = toggleFunc
        self.of = offFunc
        self.pt = pt
        self.nt = nt
        self.rd = rd
        self.to = to
        self.baseVal  = 0
        self.prevZone = 0
        self.lastActionTime = 0
        self.lastReadTime = 0
        self.doInit()

    def doInit(self, loopDelay=5):
        """
        sets the base value so that gravity is cancelled out from the initial postion
        loopDelay is the time in ms between attempts to read the accelerometer.
        """
        self.baseVal=0
        init=False
        while not init:
            delay(loopDelay)
            init,self.baseVal = self.readA()
        self.lastActionTime = millis()
        print ('Initialized!')
        
    def readA(self):
        """
        calls the read func, which we know may return a big value to indicate a failed reading
        if  value is ok, returns True and value
        if not returns False and None
        we only read every read-delay milliseconds, if called earlier, returns failure,
        at every read, the read timer is reset, even in the case of a failed read!
        """
        if millis()-self.lastReadTime < self.rd:  # too soon!
            return False, None
        res = self.rf()
        self.lastReadTime  = millis()  # we made a read, so the timer is reset, even if the
                                       # read turns out to be bad!
        if res > 31 or res < -32:  # error
            return False, None
        else:
            return True, res

    def detectionZone(self, val):
        """
        returns the detection zone for the val arg:
        if val >= pos threshold <- +1
        if val <= ned threshold <- -1
        else <- 0
        """
        res = 0
        if val >= self.pt:
            res = 1
        elif val <- self.nt:
            res = -1
        return res

    def update(self):
        ok,v = self.readA()
        if ok:  # read went ok
            curZone = self.detectionZone(v - self.baseVal)
            if (curZone): # we have passed a threshold,
                if curZone != self.prevZone: # changed zones!
                    self.tf() #tfunc must be not None
                    self.lastActionTime = millis()
                    self.prevZone = curZone
            if millis() - self.lastActionTime > self.timeOut:
                self.of() # oFunc must be not None
                self.lastActionTime = millis()

    def __repr__(self):
        return 'ShakeControl1:' + \
            '\n\treadFunc\t'         + str(self.rf)  + \
            '\n\ttoggle Func\t'      + str(self.tf)  + \
            '\n\toff Func\t'         + str(self.of) + \
            '\n\tpos Threshold\t'    + str(self.pt)  + \
            '\n\tneg Threshold\t'    + str(self.nt)  + \
            '\n\tread Delay\t'       + str(self.rd)  + \
            '\n\ttime Out\t'         + str(self.to)  + \
            '\n\tbase Value\t'       + str(self.baseVal)   + \
            '\n\tprevious Zone\t'    + str(self.prevZone)  + \
            '\n\tlast Action Time\t' + str(self.lastActionTime)  + \
            '\n\tlast Read Time\t'   + str(self.lastReadTime)
        
    
class ShakeControl:
    """ 
    provides 3-axis shake control; when there is shake in the appropriate
    axes, then the appropriate toggle function is called, LEDS always toggle!
    """
    ledVec = [[LED(4),0], # blue   -> x-axis
              [LED(3),0], # yellow -> y-axis
              [LED(2),0]] # green  -> z-axis

    def makeTFunc(tf,i):
        """
        this class method takes a toggle function tf, and a led index
        and returns a new toggle function that toggles the led before
        executing the external toggle call.
        and 'None' toggle function is okay!
        """
        def f():
            if ShakeControl.ledVec[i][1]:
                ShakeControl.ledVec[i][1]=0
                ShakeControl.ledVec[i][0].off()
            else:
                ShakeControl.ledVec[i][1]=1
                ShakeControl.ledVec[i][0].on()
            tf and tf()
        return f

    def makeOFunc(of,i):
        """
        similar to to above, this class method takes an off function of, and a led index
        and returns a new off function that turns off the led before
        executing the external off call.
        and 'None' off function is okay!
        """
        def f():
            ShakeControl.ledVec[i][1]=0
            ShakeControl.ledVec[i][0].off()
            of and of()
        return f
              
    def __init__(self,
                 tfx=None, tfy=None, tfz=None,
                 ofx=None, ofy=None, ofz=None):
        """
        creates a 3-axis instance with default values, or as per args.
        """
        self.a = Accel()
        self.sVec= list(map(lambda r,t,o: ShakeControl1(r,t,o),
                            [self.a.x,self.a.y,self.a.z],
                            [ShakeControl.makeTFunc(i,f) for (f,i) in map(lambda ind,f: (ind,f),
                                                                          range(3),
                                                                          [tfx,tfy,tfz])],
                            [ShakeControl.makeOFunc(i,f) for (f,i) in map(lambda ind,f: (ind,f),
                                                                          range(3),
                                                                          [ofx,ofy,ofz])]))

    def update(self):
        """ the update method just calls update on all the individual shake controls
        """
        for s in self.sVec:
            s.update()

# LcdDisplay
# Wiring:
# LCD PIN - connected to
#  1 - Vss (aka Ground) - Connect to one of the ground pins on you pyboard.
#  2 - VDD - connected to VIN which is 5 volts when your pyboard is powerd vi USB
#  3 - VE - connected to VIN (Contrast voltage) - I'll discuss this below
#  4 - RS (Register Select) connect to Y12 (as per call to GpioLcd)
#  5 - RW (Read/Write) - connect to ground
#  6 - EN (Enable) connect to Y11 (as per call to GpioLcd)
#  7 - D0 - leave unconnected
#  8 - D1 - leave unconnected
#  9 - D2 - leave unconnected
# 10 - D3 - leave unconnected
# 11 - D4 - connect to Y5 (as per call to GpioLcd)
# 12 - D5 - connect to Y6 (as per call to GpioLcd)
# 13 - D6 - connect to Y7 (as per call to GpioLcd)
# 14 - D7 - connect to Y8 (as per call to GpioLcd)
# 15 - A (BackLight Anode) - Connect to VIN
# 16 - K (Backlight Cathode) - Connect to Ground
#
# The Contrast line (pin 3) typically connects to the center tap of a
# 10K potentiometer, and the other 2 legs of the 10K potentiometer are
# connected to pins 1 and 2 (Ground and VDD)
#
# The wiring diagram on the followig page shows a typical "base" wiring:
# http://www.instructables.com/id/How-to-drive-a-character-LCD-displays-using-DIP-sw/step2/HD44780-pinout/
# Add to that the EN, RS, and D4-D7 lines.

class LcdDisplay(GpioLcd):
    """
    Wiring:
    LCD PIN - connected to
     1 - Vss (aka Ground) - Connect to one of the ground pins on you pyboard.
     2 - VDD - connected to VIN which is 5 volts when your pyboard is powerd vi USB
     3 - VE - connected to VIN (Contrast voltage) - I'll discuss this below
     4 - RS (Register Select) connect to Y12 (as per call to GpioLcd)
     5 - RW (Read/Write) - connect to ground
     6 - EN (Enable) connect to Y11 (as per call to GpioLcd)
     7 - D0 - leave unconnected
     8 - D1 - leave unconnected
     9 - D2 - leave unconnected
    10 - D3 - leave unconnected
    11 - D4 - connect to Y5 (as per call to GpioLcd)
    12 - D5 - connect to Y6 (as per call to GpioLcd)
    13 - D6 - connect to Y7 (as per call to GpioLcd)
    14 - D7 - connect to Y8 (as per call to GpioLcd)
    15 - A (BackLight Anode) - Connect to VIN
    16 - K (Backlight Cathode) - Connect to Ground
    
    The Contrast line (pin 3) typically connects to the center tap of a
    10K potentiometer, and the other 2 legs of the 10K potentiometer are
    connected to pins 1 and 2 (Ground and VDD)
    
    The wiring diagram on the followig page shows a typical "base" wiring:
    http://www.instructables.com/id/How-to-drive-a-character-LCD-displays-using-DIP-sw/step2/HD44780-pinout/
    Add to that the EN, RS, and D4-D7 lines.
    """
    def __init__(self,confDict):
        GpioLcd.__init__(self,
                         Pin(confDict['rs_pin']),
                         Pin(confDict['enable_pin']),
                         Pin(confDict['d4_pin']),
                         Pin(confDict['d5_pin']),
                         Pin(confDict['d6_pin']),
                         Pin(confDict['d7_pin']),
                         confDict['num_lines'],
                         confDict['num_columns'])
        self.lns =['0123456789ABCDEF','0123456789ABCDEF']
   
    def setLn(self, lineNb, val):
        """
        Set the LCD line linNb to display the val;
        val is left justified to num_cols to overwrite any 
        characters leftover from previous writes.
        """
        self.lns[lineNb] = '%-*s' % ((self.num_columns), val) # left justify with spaces to nb of display cols
        self.move_to(0,lineNb)
        self.putstr(self.lns[lineNb])
        return self
  
    def getLn(self, lineNb):
        return self.lns[lineNb]


#############  Obsolete or Unused ############
# Selector
# support for 3 or 5 ... position selector switches
# class Selector:
#     """ Usage:
#     >> pinIds = ('X1','X2','X3')
#     >> s = Selector([Pin(p, Pin.IN, Pin.PULL_DOWN) for p in pinIds])
#     >> s.currentPostion
#     3
#     >> # move switch
#     >> s.setPostion()
#     >> s.currentPostion
#     0
#     -----
#     wiring:
#     common on switch to 3.3V
#     position 0 side wire to pin 0
#     position 2 side wire to pin 1
#     position 4 side wire to pin 2
#     """
#     
#     # this defines the switch position pin values
#     # note: if a 3 position selector is used, then only the 'upper left' 3x2 part is used
#     masterTable = [[1,0,0],  # position 0, i.e. left: left pin is HIGH
#                    [1,1,0],  # position 1, i.e. left/middle: left and middle pins are HIGH
#                    [0,1,0],  # position 2, i.e. middle: middle pin is HIGH
#                    [0,1,1],  # position 3, i.e. middle/right: middle & right pins are HIGH
#                    [0,0,1]]  # position 4, i.e. right: right pin is HIGH
#     
#     def __init__(self,pins):
#         """create an instance of a 3 or 5 position switch connected to the 
#         pins provided.
#         Pins should be configured as Pin('X1', Pin.IN, Pin.PULL_DOWN)
#         len(pins) should be 2, for 3 postions, 3, for 5 positions
#         incorrect arguments raise exceptions
#         """
#         if len(pins) not in (2,3):
#             raise Exception('invalid nb of pins', pins)
#         self.pinLis = []
#         for p in pins:
#             self.pinLis += [p]
#         nbPos = 2*len(pins) -1
#         self.truthTable = [x[:len(pins)] for x in Selector.masterTable[:nbPos]]
#         self.currentPosition = 0
#         self.setPosition()  # reads the pin values and deduces current switch position
#         
#     def setPosition(self):
#         """ reads the pin values and deduces current switch position
#         in case of failure, exception is raised.
#         """
#         tLis  = [p.value() for p in self.pinLis]
#         i = 0
#         found = False
#         while not found:
#             if all(map(lambda x,y: x==y,tLis,self.truthTable[i])):
#                 found = True
#             else:
#                 i +=1
#         if not found:
#             raise Exception('position not found', tLis)
#         self.currentPosition = i
# 
#     def __repr__(self):
#         return 'Selector:' + \
#             '\n\tpostion:\t' + str(self.currentPosition) +\
#             '\n\tpinLis:\t' + str(self.pinLis) +\
#             '\n\ttruthTable:\t' + str(self.truthTable)  + '\n'

# Illuminator
# # support leds or other pin controlled lights
# class Illuminator__:
#     """
#     Helper class for Illuminator, see below
#     """
#     
#     def __init__(self,pin):
#         """create an instance of a LED connected to the 
#         pin provided.
#         Pins should be configured as Pin('X1', Pin.OUT_PP)
#         """
#         self.p = pin
#         self.off()
#         
#     def off(self):
#         """ set pin to low
#         """
#         self.p.low()
# 
#     def on(self):
#         """ set pin to high
#         """
#         self.p.high()
# 
#     def value(self):
#         """ returns 0 or 1 depending on state of pin
#         """
#         return self.p.value()
# 
# class Illuminator(Illuminator__):
#     """ Usage:
#     >> pinId = 'X1
#     >> i = Illuminator(Pin(pinID, Pin.OUT_PP))
#     >> i.value()
#     0
#     >> i.on()
#     >> i.value()
#     1
#     >> i.off()
#     >> i.value()
#     0
#     -----
#     wiring:
#     from pin to LED+ 
#     from LED- to current limiting resistor
#     from current limiting resistor to ground
#     """
# 
#     toggleFuncs = (Illuminator__.on, Illuminator__.off)  # for use in toggle
# 
#     def __init__(self,pin):
#         """create an instance of a LED connected to the 
#         pin provided.
#         Pin should be configured as Pin('X1', Pin.OUT_PP)
#         """
#         Illuminator__.__init__(self,pin)
#         
#     def toggle(self):
#         """ toggles the value of the pin
#         """
#         type(self).toggleFuncs[self.value()](self)
# 
#     def __repr__(self):
#         return 'Illuminator:' + \
#             '\n\tpin:\t' + str(self.p) +\
#             '\n\tvalue:\t' + str(self.p.value())  + '\n'                    
# 
# 
# # SWDebouncedPushbutton
# # debounce a momentary pushbutton with HIGH == ON state and
# # at every push, toggle a LED illuminator
# # usage:
# # >>> p = pyb.Pin('X1', pyb.Pin.IN, pyb.Pin.PULL_DOWN)
# # >>> i = Illuminator(pyb.Pin('X2', pyb.Pin.OUT_PP))
# # >>> b = DebouncePushbutton(p,i.toggle)
# # >>> while True:
# # ...   b.update()
# #
# class SWDebouncedPushbutton:
#     debounceDelay = 20 #milliseconds between pushes
# 
#     def __init__(self, pin, onHigh=None):
#         self.pin = pin
#         self.lastDebounceTime = millis()
#         self.lastReading = 0
#         self.onHigh = onHigh
# 
#     def update(self):
#         # if there's been enouh time since last bounce, then take a reading
#         if millis() - self.lastDebounceTime > self.debounceDelay:
#             reading = self.pin.value()
#             # if the reading is different from the last one,
#             if reading != self.lastReading:
#                 # we got a new value:
#                 # * update bounce time
#                 # * update reading
#                 # * and if reading is HIGH, execute the onHigh action
#                 self.lastDebounceTime = millis()
#                 self.lastReading = reading
#                 if reading and self.onHigh:
#                     self.onHigh()
# 
#     def __repr__(self):
#         return 'Pushbutton:' + \
#             '\n\tpin:\t' + str(self.pin) + \
#             '\n\tlastDebounceTime:\t' + str(self.lastDebounceTime)  + \
#             '\n\tlastReading:\t' + str(self.lastReading)  + \
#             '\n\tonHigh:\t' + str(self.onHigh)  + '\n'
#

# class IlluminatedPushbutton(SWDebouncedPushbutton) :
#     """
#     a Pushbutton with an Illuminator built-in, in addtion to the
#     onHigh action, of course.
#     """
# 
#     def __init__(self, pin, illum, onAction = None):
#         SWDebouncedPushbutton.__init__(self,pin,self.illumOnHigh)
#         self.illuminator = illum
#         self.onAction = onAction
#         
#     def illumOnHigh(self):
#         if self.onAction:
#             self.onAction()
#         self.illuminator.toggle()
# 
#     def __repr__(self):
#         return 'IlluminatedPushbutton:' + \
#             '\n\tilluminator:\t' + str(self.illuminator) + \
#             '\n\tonAction:\t' + str(self.onAction)  + \
#             '\n' + SWDebouncedPushbutton.__repr__(self)
#

    
# class VoltageDividerPot:
#     """
#     Encapsulate the reading of an analog pot in voltage divider configuration
#     """
#     def __init__(self,pin,rm=None):
#         """
#         instance creation, args:
#         * pin is a pyb.Pin object as per: pyb.Pin('X1', pyb.Pin.ANALOG)
#         * an optional RMap instance to provide a reading in the proper range
#         """
#         self.a = ADC(pin)
#         if rm:
#             self.v = lambda x: rm.v(x)
#         else:
#             self.v = lambda x:x
# 
#     def update(self):
#         """
#         returns the current reading as per config
#         """
#         return self.v(self.a.read())
# 
