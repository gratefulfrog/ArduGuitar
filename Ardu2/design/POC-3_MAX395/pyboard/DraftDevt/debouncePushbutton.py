# DebouncePushbutton.py
# updated 2015 11 15 to allow for onState =0, ie Pullup!
# debounce a momentary pushbutton with ON state argument and
# at every push, toggle a LED illuminator
# usage:
# >>> p = pyb.Pin('X1', pyb.Pin.IN, pyb.Pin.PULL_UP)
# >>> i = Illuminator(pyb.Pin('X2', pyb.Pin.OUT_PP))
# >>> b = DebouncePushbutton(p,i.toggle,0)
# >>> while True:
# ...   b.update()
#

import pyb
from illuminator import Illuminator

class DebouncePushbutton:
    debounceDelay = 20 #milliseconds between pushes

    def __init__(self, pin, doOn=None, onState=0):
        self.pin = pin
        self.lastDebounceTime = pyb.millis()
        self.lastReading = 0
        self.doOn = doOn
        self.onState = onState

    def update(self):
        if pyb.millis() - self.lastDebounceTime > self.debounceDelay:
            reading = self.pin.value()
            if reading != self.lastReading:
                # we got a new value
                self.lastDebounceTime = pyb.millis()
                self.lastReading = reading
                if reading == self.onState and self.doOn:
                    self.doOn()

class IlluminatedPushbutton(DebouncePushbutton) :

    def __init__(self, pin, illum, onAction = None, onState = 0):
        DebouncePushbutton.__init__(self,pin,self.illumDo,onState)
        self.illuminator = illum
        self.onAction = onAction
        
    def illumDo(self):
        if self.onAction:
            self.onAction()
        self.illuminator.toggle()
