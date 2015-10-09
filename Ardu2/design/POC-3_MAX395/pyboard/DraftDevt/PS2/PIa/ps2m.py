#ps2m.py  the mouse polling example

import PS2, pyb


def pt(c='X3'):
    p = pyb.Pin(c,pyb.Pin.IN,pull=pyb.Pin.PULL_UP)
    print (p.value())
    
    u = pyb.micros()
    p.init(pyb.Pin.OUT_OD,pull=pyb.Pin.PULL_UP)
    p.value(0)
    print(str(pyb.micros()-u))
    print (p.value())

    u = pyb.micros()
    p.value(1)
    while not p.value():
        None
    print(str(pyb.micros()-u))
    u = pyb.micros()
    p.init(pyb.Pin.IN,pull=pyb.Pin.PULL_UP)
    while not p.value():
        None
    print(str(pyb.micros()-u))
    

def tc(c='X11',d='X12'):
    p = PS2.PS2(c,d)
    print('Write RESET')
    p.write(0XFF)
    print('read ACK')
    p.read()
    while True:
        us = pyb.micros()
        while  p.clock.value():
            None
        print('HIGH for %d us'% (pyb.micros()-us))
        print('Data: ' + str(p.data.value()))
        us = pyb.micros()
        while not p.clock.value():
            None
        print('Low for %d us'% (pyb.micros()-us))
        print('Data: ' + str(p.data.value()))



def mInit(p):
    print('Write RESET')
    p.write(0XFF)
    print('read ACK')
    print(hex(p.read()).upper()) # ACK
    print('read BAT')
    print(hex(p.read()).upper()) # BAT
    print('read ID')
    print(hex(p.read()).upper()) # ID
    print('Write REMOTE')
    p.write(0XF0)
    print('read ACK')
    print(hex(p.read()).upper()) # ACK
    pyb.udelay(100)

def interpretStat(st):
    sVec = ["Left",
            "Right",
            "Middle",
            "None",
            "-X",
            "-Y",
            "X Overflow",
            "Y Overflow"]
    res = ""
    for i in range(8):
        if stat and (0x01 << i):
            res +=sVec[i]
            if i< 7:
                res += ', '
    return res
    
def run(cName='X11',dName='X12'):
    p = PS2.PS2(cName,dName)

    mInit(p)

    #setup local loop variabls 
    lmStat = 'y'
    mStat =  'n'
    lmx = '1'
    mx = '0'
    lmy = '1'
    my = '0'

    outputTemplate = 'X=%d\tY=%d\t%s'
    
    while True:
        p.write(0XEB)  # poll
        print('Write POLL')
        p.read()       # ignore the ACK
        mstat = p.read()  # status byte
        mx    = p.read()  # delta-x byte
        my    = p.read()  # delta-y byte

        if mstat != lmstat or mx != lmx or my != lmy:
            print (outputTemplate%(mx,my,interpretStat(mstat)))
            lmstat = mstat
            lmx = mx
            lmy =my
        pyb.delay(20)
        
                                   
