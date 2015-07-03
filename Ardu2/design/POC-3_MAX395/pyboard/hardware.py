# hardware.py
# classes corresponding to physical objects in the system
# * ShuntControl
# * Selector
# * Illuminator
# * Pushbutton
# * IlluminatedPushbutton
#####

from pyb import millis, Pin, Timer
from dictMgr import shuntConfDict
from state import State

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




# Selector
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


# Illuminator
# support leds or other pin controlled lights
class Illuminator__:
    """
    Helper class for Illuminator, see below
    """
    
    def __init__(self,pin):
        """create an instance of a LED connected to the 
        pin provided.
        Pins should be configured as Pin('X1', Pin.OUT_PP)
        """
        self.p = pin
        self.off()
        
    def off(self):
        """ set pin to low
        """
        self.p.low()

    def on(self):
        """ set pin to high
        """
        self.p.high()

    def value(self):
        """ returns 0 or 1 depending on state of pin
        """
        return self.p.value()

class Illuminator(Illuminator__):
    """ Usage:
    >> pinId = 'X1
    >> i = Illuminator(Pin(pinID, Pin.OUT_PP))
    >> i.value()
    0
    >> i.on()
    >> i.value()
    1
    >> i.off()
    >> i.value()
    0
    -----
    wiring:
    from pin to LED+ 
    from LED- to current limiting resistor
    from current limiting resistor to ground
    """

    toggleFuncs = (Illuminator__.on, Illuminator__.off)  # for use in toggle

    def __init__(self,pin):
        """create an instance of a LED connected to the 
        pin provided.
        Pin should be configured as Pin('X1', Pin.OUT_PP)
        """
        Illuminator__.__init__(self,pin)
        
    def toggle(self):
        """ toggles the value of the pin
        """
        type(self).toggleFuncs[self.value()](self)

    def __repr__(self):
        return 'Illuminator:' + \
            '\n\tpin:\t' + str(self.p) +\
            '\n\tvalue:\t' + str(self.p.value())  + '\n'                    


# Pushbutton
# debounce a momentary pushbutton with HIGH == ON state and
# at every push, toggle a LED illuminator
# usage:
# >>> p = pyb.Pin('X1', pyb.Pin.IN, pyb.Pin.PULL_DOWN)
# >>> i = Illuminator(pyb.Pin('X2', pyb.Pin.OUT_PP))
# >>> b = DebouncePushbutton(p,i.toggle)
# >>> while True:
# ...   b.update()
#
class Pushbutton:
    debounceDelay = 20 #milliseconds between pushes

    def __init__(self, pin, onHigh=None):
        self.pin = pin
        self.lastDebounceTime = millis()
        self.lastReading = 0
        self.onHigh = onHigh

    def update(self):
        # if there's been enouh time since last bounce, then take a reading
        if millis() - self.lastDebounceTime > self.debounceDelay:
            reading = self.pin.value()
            # if the reading is different from the last one,
            if reading != self.lastReading:
                # we got a new value:
                # * update bounce time
                # * update reading
                # * and if reading is HIGH, execute the onHigh action
                self.lastDebounceTime = millis()
                self.lastReading = reading
                if reading and self.onHigh:
                    self.onHigh()

class IlluminatedPushbutton(Pushbutton) :
    """
    a Pushbutton with an Illuminator built-in, in addtion to the
    onHigh action, of course.
    """

    def __init__(self, pin, illum, onAction = None):
        Pushbutton.__init__(self,pin,self.illumOnHigh)
        self.illuminator = illum
        self.onAction = onAction
        
    def illumOnHigh(self):
        if self.onAction:
            self.onAction()
        self.illuminator.toggle()
