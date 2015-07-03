# DebouncePushbutton.py
# debounce a momentary pushbutton with HIGH == ON state and
# at every push, toggle a LED illuminator
# usage:
# >>> p = pyb.Pin('X1', pyb.Pin.IN, pyb.Pin.PULL_DOWN)
# >>> i = Illuminator(pyb.Pin('X2', pyb.Pin.OUT_PP))
# >>> b = DebouncePushbutton(p,i.toggle)
# >>> while True:
# ...   b.update()
#

import pyb
from illuminator import Illuminator

class DebouncePushbutton:
    debounceDelay = 20 #milliseconds between pushes

    def __init__(self, pin, onHigh=None):
        self.pin = pin
        self.lastDebounceTime = pyb.millis()
        self.lastReading = 0
        self.onHigh = onHigh

    def update(self):
        if pyb.millis() - self.lastDebounceTime > self.debounceDelay:
            reading = self.pin.value()
            if reading != self.lastReading:
                # we got a new value
                self.lastDebounceTime = pyb.millis()
                self.lastReading = reading
                if reading and self.onHigh:
                    self.onHigh()

class IlluminatedPushbutton(DebouncePushbutton) :

    def __init__(self, pin, illum, onAction = None):
        DebouncePushbutton.__init__(self,pin,self.illumOnHigh)
        self.illuminator = illum
        self.onAction = onAction
        
    def illumOnHigh(self):
        if self.onAction:
            self.onAction()
        self.illuminator.toggle()
