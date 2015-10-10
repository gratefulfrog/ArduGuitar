# PinTracker.py

import pyb

_clock = 'X7'
_data =  'X8'

clock = pyb.Pin(_clock,mode=pyb.Pin.IN,pull=pyb.Pin.PULL_NONE);
data  =  pyb.Pin(_data,mode=pyb.Pin.IN,pull=pyb.Pin.PULL_NONE);

def run(check = False):
    global clock, data
    c = d = 0
    lc = ld = -1
    while True:
        (c,d) = (clock.value(),data.value())
        if not d and c:
            for i in range(11):
                if lc and not c:
                    print(data.value())
                (lc,ld)=(c,d)
        
