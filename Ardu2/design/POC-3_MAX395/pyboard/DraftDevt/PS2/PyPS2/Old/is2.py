# is2.py
#
# PS/2 trackball Interrupt version
# here the idea is that all the preparation work is done in advance,
# the interrupt handler on Falling edge either:
## reads a bit into the bit buffer
## ro
## writes a bit from the bitt buffer
## increments bit buffer index
##
# commands are associated with the number of bytes in their response, and any checking that should be done
# the method: SendCommandAndReceiveReply handles the setup of global variables used by the interrupt hander
##

import pyb
from pyb import Pin

clock = Pin('X1',Pin.OUT_OD,Pin.PULL_NONE)
data  = Pin('X2',Pin.OUT_OD,Pin.PULL_NONE)

cv = clock.value
dv = data.value

# nb bits that the buffer cn contain
rBuffSize =  11*16 # 16 full messages

# to be used as circular buffer
rBuffer = [0 for i in range(rBuffSize)]
# the write buffer will hold just the 11 bits of one commande
wBuffer = []
rIndex = wIndex = 0
rrIndex = rBuffSize-1
nbBits2Process = 0

hostSetClockLow = True
reading=False

# command lists: [commandByte,nbReponsebytes,values of response bytes if known!]
reset = [0xFF,3,0xFA,0xAA,0x0] # ACK, BAT, ID
remoteMode = [0xF0,1,0xFA] # ACK
poll = [0xEB,4,0xFA]  # ACK plus 3 data bits


class ParityError(Exception):
    def __init__(self, expected, computed):
        self.computed = computed
        self.expected = expected
    def __repr__(self):
        return 'Expected:  '+ str(self.expected) + ' Computed:  '+ str(self.computed) 
"""
def interruptHandler(unused):
    print('got one!')

"""
def interruptHandler(unused):
    # due stuff on the fallin edge of clock
    # but only if it was not us that set the clock low
    global rBuffer, rIndex, wIndex, nbBits2Process,rBuffSize
    if hostSetClockLow:
        print('host set clock low')
        return
    elif reading:
        print('read!')
        """
        rBuffer[rIndex] = dv()
        rIndex= (rIndex+1)%rBuffSize
        nbBits2Process +=1
        """
    else:
        print('sent!')
        """
        if wIndex < len(wBuffer):
            dv(wBuffer[wIndex])
        wIndex += 1
        """

def command2BitList(command):
    """ 
    takes a byte argument and returns a list of 11 values representing
    the PS/2 message, i.e.
    '0' start bit
    8 computed data bits
    1 computed odd parity bit
    '1' stop bit
    This INCLUDES the request to send!!
    """
    res = []
    # odd parity
    parity = 1
    # start bit
    res += [0]   
    for i in range(8):
        v =(command>>i) & 1
        parity ^= v
        res += [v]
    # partity bit
    res +=[parity]
    # stop bit
    res +=[1]
    return res

def inhibitComms():
    global cv,dv,hostSetClockLow
    hostSetClockLow = True
    dv(1)
    cv(0)

def sendCommand(c):
    """
    c is a list of bits, low order bit first
    set the flags for writing,
    set the first message bit (which is the start bit),
    then let the clock go,
    count clock cycles up to 11 sends,
    then set the reading flag to true
    """
    global cv,dv,rIndex,wIndex,hostSetClockLow,reading,nbBits2Process

    # first reset the counter for nb bits to process
    # no! nbBits2Process=0
    
    # then let the interrupt handler go free!
    reading = False
    hostSetClockLow = False

    # reset rIndex in preparation for the replies
    #rIndex = 0

    # inc the wIndex after the start bit 
    wIndex = 1
    dv(c[0])
    cv(1)
    while wIndex<11:
        pass
    reading = True

def recoverResponse(nbBytes):
    """
    compute number of bits, i.e. clock cycles to let go by
    wait for that to happen,
    then inihibit coms,
    return a list of the bits translated into bytes
    """
    global rIndex,rBuffer
    # compute the number of bits to be read
    rLimit = 11 * nbBytes
    while nbBits2Process < rLimit:
        pass
    inhibitComms()
    reading = False
    return bitList2ByteList()

def bitList2ByteList():
    """
    take the circular rBuffer and 11 by 11 translate into bytes,
    raise an exception if the parity doesnt check out!
    """
    global rrIndex,nbBits2Process
    byteVec= []
    while nbBits2Process > 0:
        byteRead = 0
        parity = 1
        for i in range(11):
            rrIndex = (rrIndex + 1)%rBuffSize
            nbBits2Process -=1
            # start and stop bits, do nothig
            if i == 0 or i == 10:
                pass
            elif i ==9 and parity != rBuffer[rrIndex]:
                raise ParityError(rBuffer[rrIndex],parity)
            elif i == 9:
               byteVec += [byteRead]
            else:
                bit = rBuffer[rrIndex]
                byteRead = byteRead | (bit << (i-1))
                parity ^= bit
                #print(byteRead)
    return byteVec


def sendCommandGetResponse(cStruct):
    """
    a cStruct is [commandByte,nbReponsebytes,values of response bytes if known!]
    this function will send the command
    recover the response
    compare it to expected
    print results
    """
    [cByte,nbResponseBytes] = cStruct[:2]

    sendCommand(command2BitList(cByte))
    responseList = recoverResponse(nbResponseBytes)
    print('Expected:\t' + str([hex(x) for x in cSTruct[:3]] if cSTruct[:3] else None))
    print('Received:\t' + str([hex(x) for x in responseList]))
    
def init():
    rf = pyb.ExtInt.IRQ_FALLING
    pyb.ExtInt(clock,rf,pyb.Pin.PULL_NONE,interruptHandler)
