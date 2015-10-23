# ps2mouse.py

# version using the class

# clock =  X1
# data = X3

import PS2, pyb

reset = 0xFF
remote = 0xF0
dataRequest = 0xEB

r1 =0
r2 =0
r3 =0
r4 = 0

def init(device):
    global reset, remote,r1,r2,r3,r4
    
    # reset device
    print('Writing the reset')
    device.write(reset)
    # get replies
    print('Reading ack 1')
    r1 = device.read() # ack
    print('Reading blank 1')
    r2 = device.read() # blank
    print('Reading blank 2')
    r3 = device.read() # blank

    # set remote poling mode
    print('Writing the remote mode')
    device.write(remote)
    print('Reading ack 2')
    r4 = device.read() # ack
    
    pyb.udelay(100)
    print('exiting...')
    
def runTest1():
    # just init a mouse!
    tb = PS2.PS2('X1','X3')
    init(tb)

def interpretStatByte(statByte):
    statVec = ['Left',
               'Right',
               'Middle',
               'None',
               '-X',
               '-Y',
               'X Overflow',
               'Y Overflow']
    
    res = '\t'
    for  i in range(8):
        if(stat & (1<<i)):
            res += statVec[i]
            if (i < 7):
                res += ','
    return res
    
def run():
    global dataRequest
    
    tb = PS2.PS2('X1','X2')
    init(tb)

    mstat = 'y'
    lstat = 'n'
    my = mx = 0
    ly = lx = 1

    while(True):
        tb.write(dataRequest)
        tb.read() # ignore ack
        mstat = tb.read()
        mx = tb.read()
        my = tb.read()
        if ((mstat != lstat) or
            (mx != lx) or
            (my !=ly)):
            sCoords = 'STRING X= ' + str(mx) + '\tY= ' + str(my) + interpretStatByte(mstat)
            print(sCoords)
            dCoords = 'DEC X= ' + str(int(mx)) + '\tY= ' + str(int(my)) + interpretStatByte(mstat)
            print(dCoords)
            lstat = mstat
            lx = mx
            ly = my
        delay(20)
        
