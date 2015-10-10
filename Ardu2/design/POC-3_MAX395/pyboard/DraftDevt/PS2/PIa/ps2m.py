#ps2m.py  the mouse polling example

import PS2a, pyb



def mInit(p):
    print('Write RESET')
    print('read ACK')
    print('read BAT')
    print('read ID')
    print('Write REMOTE')
    print('read ACK')
    p.write(0XFF)
    a=p.read()
    print('read ACK:' + hex(a))
    p.read()
    p.read()
    p.write(0XF0)
    p.read()
    pyb.udelay(100)
    print ('Done!')
    
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
    
def run(cName='X7',dName='X8'):
    p = PS2a.PS2(cName,dName)

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
        
                                   
