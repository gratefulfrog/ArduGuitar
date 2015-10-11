# PinTracker.py

import pyb



def run(check = False):
    _clock = 'X7'
    _data =  'X8'

    clock = pyb.Pin(_clock,mode=pyb.Pin.IN,pull=pyb.Pin.PULL_NONE);
    data  =  pyb.Pin(_data,mode=pyb.Pin.IN,pull=pyb.Pin.PULL_NONE);
    c = 0
    d = 0
    lc = -1
    ld = -1
    while True:
        c =clock.value()
        d= data.value()
        if not d and c:
            for i in range(11):
                if lc and not c:
                    print(data.value())
                lc = c
                ld = d
        
