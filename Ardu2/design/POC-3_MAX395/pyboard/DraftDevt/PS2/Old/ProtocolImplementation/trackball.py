# trackball.py

# yet more attenpts at making the ps/2 trackball talk to the pyboard


import PS2

def show(p):
    counter=50
    rc= rd=0
    while(True):
        counter -= 1
        rc = (rc<<1) | p.clock.value()
        rd = (rd<<1) | p.data.value()
        if not counter:
            print ('Clock: ' + bin(rc))
            print ('Data: ' + bin(rd))
            counter = 50
            rc=rd=0

def resetListenN(p,n=3):
    print('send a reset, read 3x 11 bits')
    sendReset(p)
    readPN(p,n)

def device(c='X11',d='X12',debug=False):
    print('Return a PS2 instance.')
    return PS2.PS2(c,d,debug)

def t0(p, abort=False):
    """ 
    connect and read
    """
    print('Read forever...')
    readLoop(p,abort)

def t1(p,abort=False):
    """
    connect, send a reset, read
    """
    print('send a reset, read forever')
    sendReset(p)
    readLoop(p,abort)
    
def t2(p,abort = False):
    """
    connect,
    send reset,
    read three x 11 bits
    set remote mode
    read
    """
    print('send a reset, read 3x 11 bits, set remote mode')
    sendReset(p)
    readPN(p,3)
    sendRemote(p)
    readLoop(p, abort)

def t3(p,abort = False):
    """
    connect,
    send reset,
    read three x 11 bits
    set remote mode
    read 1x 11 bits
    poll for data
    read 4x 11 bits
    """
    print('send a reset, read 3x 11 bits, set remote mode, read 1x 11 bits,poll, read 4x 11 bits')
    sendReset(p)
    readPN(p,3)
    sendRemote(p)
    readPN(p,1)
    sendPoll(p)
    readPN(p,4)

def t4(ps2,abort = False):
    """
    suppose that ps2 argument is in remote mode,
    poll for data
    read 4x 11 bits
    """
    print('poll, read 4x 11 bits')
    sendPoll(ps2)
    readPN(ps2,4)

def sendReset(ps2):
    reset = 0xFF
    print('About to send RESET: %X'%reset)
    ps2.sendBits(reset)

def sendRemote(ps2):
    remote = 0xF0
    print('About to send REMOTE: %X'%remote)
    ps2.sendBits(remote)

def sendPoll(ps2):
    poll = 0xEB
    print('About to send POLL: %X'%poll)
    ps2.sendBits(poll)
        
def readLoop(ps2, abortAfter5=True):
    counter =5
    while (True and counter):
        if abortAfter5:
            counter -= 1
        print('About to read 1x 11 bits...')
        ps2.readBits()

def readPN(ps2,n):
    print('About to read %dx 11 bits'%n)
    for i in range(n):
        print('\tRead number %d:'%(i+1))
        ps2.readBits()


    
