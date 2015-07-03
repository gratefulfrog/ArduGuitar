# tempDecounce.py
# debounce a momentary pushbutton with HIGH == ON state and
# at every push, toggle a LED illuminator

import pyb
from illuminator import Illuminator

def update(dell = 20):
    pin_x1 = pyb.Pin('X1', pyb.Pin.IN, pyb.Pin.PULL_DOWN)
    i = Illuminator(pyb.Pin('X2', pyb.Pin.OUT_PP))
    lastDebounceTime = pyb.millis()
    lastReading = 0
    while True:
        # if we waited long enough since last HIGH
        if pyb.millis() - lastDebounceTime > dell:
            reading = pin_x1.value()
            if reading != lastReading:
                # we got a new value
                lastDebounceTime = pyb.millis()
                lastReading = reading
                if reading:
                    i.toggle()

    
