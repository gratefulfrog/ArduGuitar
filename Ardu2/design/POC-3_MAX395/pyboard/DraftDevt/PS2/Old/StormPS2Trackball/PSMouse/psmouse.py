# psmouse.py
"""
a port from the arduino PSMouse.ino
"""
import pyb

clockDelay = 300 # microseconds
dataDelay  = 10  # microseconds
stopDelay  = 50  # microseconds
shortDelay = 5   # microseconds
oneHundredMicroSeconds = 100

dataPinName = 'X1'
clockPinName = 'X2'

dataPin = pyb.Pin(dataPinName,pyb.Pin.IN,pull=pyb.Pin.PULL_NONE) 
clockPin = pyb.Pin(clockPinName, pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)

def goHi(p):
    """ set the pin to INPUT mode with PULL_UP
    """
    p.init(pyb.Pin.IN,pull=pyb.Pin.PULL_UP)
    #p.value(1)
    #p.init(pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)

def goLo(p):
    """ set the pin to OUTPUT mode, then set it at LOW
    """
    p.init(pyb.Pin.OUT_PP,pull=pyb.Pin.PULL_NONE)
    p.value(0)

def waitClockCycle():
    global clockPin
    while (not clockPin.value()):
        None
    while (clockPin.value()):
        None

def mouseWrite(data):
    global clockDelay,dataDelay,stopDelay,shortDelay,oneHundredMicroSeconds,dataPin,clockPin
    parity = 1

    goHi(dataPin)
    goHi(clockPin)
    pyb.udelay(clockDelay)
    goLo(clockPin)
    pyb.udelay(clockDelay)
    goLo(dataPin)
    pyb.udelay(dataDelay)

    # start bit 
    goHi(clockPin)
    # wait for mouse to take control of clock)
    while(clockPin.value()):
        None
        
    # clock is now low, and we are clear to send data */
    for i in range(8):
        if (data & 0x01):
            goHi(dataPin)
        else:
            goLo(dataPin)
        
        # wait for clock cycle */
        waitClockCycle()
        parity = parity ^ (data & 0x01)
        data = data >> 1
    
    # parity */
    if (parity):
        goHi(dataPin)
    else:
        goLo(dataPin)

    waitClockCycle()
    
    # stop bit 
    goHi(dataPin)
    pyb.udelay(stopDelay)
    while (clockPin.value()):
        None
    # wait for mouse to switch modes */
    while ((not clockPin.value()) or (not dataPin.value())):
        None
    # put a hold on the incoming data. 
    goLo(clockPin)
    

# Get a byte of data from the mouse
def mouseRead():
    global clockDelay,dataDelay,stopDelay,shortDelay,oneHundredMicroSeconds,dataPin,clockPin
    data = 0x00
    bit = 0x01

    #  Serial.print("reading byte from mouse\n")
    # start the clock */
    goHi(clockPin)
    goHi(dataPin)
    pyb.udelay(stopDelay)
    while (clockPin.value()):
        None
    pyb.udelay(shortDelay)  # not sure why */
    while (not clockPin.value()): # eat start bit */
        None
    for i in range(8):
        while (clockPin.value()):
            None
        if (dataPin.value()):
            data = data | bit
        while (clockPin.value()):
            None
        bit = bit << 1
  
    # eat parity bit, which we ignore */
    waitClockCycle()
    while (clockPin.value()):
        None
    while (not clockPin.value()):
        None
    # eat stop bit */
    waitClockCycle()
    while (clockPin.value()):
        None    
    while (not clockPin.value()):
        None
    # put a hold on the incoming data. */
    goLo(clockPin)
    # Serial.print("Recvd data ")
    #  Serial.print(data, HEX)
    #  Serial.print(" from mouse\n")
    return data 


def mouseInit():
    global clockDelay,dataDelay,stopDelay,shortDelay,oneHundredMicroSeconds,dataPin,clockPin

    """
    the dialogue should be (in decimal!)

    Sending reset to mouse
    250
    170
    0
    Sending remote mode code
    250

    Sending reset to mouse
    251
    36
    36
    Sending remote mode code
    243
    >>> psmouse.setup()
    Sending reset to mouse
    228
    228
    228
    Sending remote mode code
    251
    >>> psmouse.setup()
    Sending reset to mouse
    251
    36
    36
    Sending remote mode code
    251

    """

    
    goHi(clockPin)
    goHi(dataPin)
    print('Sending reset to mouse')
    mouseWrite(0xff)
    print(mouseRead())  # ack byte */
    #  Serial.print("Read ack byte1\n");
    print(mouseRead()) # blank */
    print(mouseRead()) # blank */
    print('Sending remote mode code')
    mouseWrite(0xf0)  # remote mode */
    print(mouseRead() ) # mouseRead()  # ack */
    #  Serial.print("Read ack byte2\n");
    pyb.udelay(oneHundredMicroSeconds);

def setup():
    mouseInit()

def interpretStatByte(stat):
    statVec = ["Left",
               "Right",
               "Middle",
               "None",
               "-X",
               "-Y",
               "X Overflow",
               "Y Overflow"]
    res = '\t'
    for i in range(8):
        if(stat & (1<<i)):
            res += statVec[i]
            if (i != 7):
                res+= ', '
    return(res)

mstat='y'
lmstat = 'n'
mx ='0'
lmx = '1'
my ='0'
lmy = '1'
maxX =0
maxY = 0

def loop():
    global mstat,lmstat,mx,lmx,my,lmy,maxX,maxY
    #get a reading from the mouse */
    mouseWrite(0xeb) #  /* give me data! */
    mouseRead()    #  /* ignore ack */
    mstat = mouseRead()
    mx = mouseRead()
    my = mouseRead()

    if((mstat != lmstat) or
       (mx !=lmx) or
       (my != lmy)):
      #/* send the data back up */
      #//Serial.print(mstat, BIN);
        print('X=',str(mx),'\tY=',str(my) + interpretStatByte(mstat))
        lmstat = mstat
        lmx = mx
        lmy = my
        #maxX = max(mx,maxX);
        #maxY = max(my,maxY);
        """
        Serial.print("maxX: ");
        Serial.print(maxX,DEC);
        Serial.print("\tmaxY: ");
        Serial.println(maxY,DEC);
        """
        pyb.delay(20)
        
def run():
    setup()
    while(True):
        loop()

