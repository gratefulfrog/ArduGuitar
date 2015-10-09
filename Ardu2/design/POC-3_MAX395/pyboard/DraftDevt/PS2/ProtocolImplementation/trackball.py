# trackball.py

# yet more attenpts at making the ps/2 trackball talk to the pyboard


import PS2


def t0(c='X1',d='X2'):
    """ 
    connect and read
    """
    p=PS2.PS2(c,d)
    readLoop(p)

def t1(c='X1',d='X2'):
    """
    connect, send a reset, read
    """
    p=PS2.PS2(c,d)
    sendReset(p)
    readLoop(p)
    
def t2(c='X1',d='X2'):
    """
    connect,
    send reset,
    read three x 11 bits
    set remote mode
    read
    """
    p=PS2.PS2(c,d)
    sendReset(p)
    readPN(p,3)
    sendRemote(p)
    readLoop(p)

def t3(c='X1',d='X2'):
    """
    connect,
    send reset,
    read three x 11 bits
    set remote mode
    read 1x 11 bits
    poll for data
    read 4x 11 bits
    return the ps2 device for further pollingp
    """
    p=PS2.PS2(c,d)
    sendReset(p)
    readPN(p,3)
    sendRemote(p)
    readPN(p,1)
    sendPoll(p)
    readPN(p,4)
    return p

def t4(ps2):
    """
    suppose that ps2 argument is in remote mode,
    poll for data
    read 4x 11 bits
    """
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
        counter -= 1
        print('About to read 1x 11 bits...')
        ps2.readBits()

def readPN(ps2,n):
    print('About to read %dx 11 bits'%n)
    for i in range(n):
        print('\tRead number %d:'%(i+1))
        ps2.readBits()


    
