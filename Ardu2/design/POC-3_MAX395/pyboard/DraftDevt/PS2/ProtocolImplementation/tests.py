# tests.py

# some stuff for PS/2...

import pyb

class PS2:
    def getParity(byte):
        """ 
        return the odd parity value of the byte, no checkin of the argument:
        odd parity is such that the number of 1s in the binary representation of the byte
        plus the parity value is always an odd number.
        """
        parity = 1
        for i in range(8):
            parity += (byte>>i) & 1
        parity %=2
        return parity

    def __int__(self,clockPinName,dataPinName):
        self.clock  = pyb.Pin(clockPinInName,pyb.Pin.IN,pull=pyb.PULL_NONE)
        self.data   = pyb.Pin(dataPinName,pyb.PIN.IN,pull=pyb.PULL_NONE)

    def clockHighImpedence(self):
        self.clock.init(pyb.Pin.IN,pull=pyb.PULL_NONE)

    def dataHighImpedence(self):
        self.data.init(pyb.Pin.IN,pull=pyb.PULL_NONE)

    def clockLowValue(self):
        self.clock.init(pyb.Pin.OUT_OD,pull=pyb.PULL_NONE)
        #pyb.udelay(5)
        self.clock.value(0)

    def dataLowValue(self):
        self.data.init(pyb.Pin.OUT_OD,pull=pyb.PULL_NONE)
        #pyb.udelay(5)
        self.data.value(0)

    def request2Send(self):
        # first make a request to send:
        self.clockLowValue()
        pyb.udelay(110)
        self.dataLowValue()
        self.clockHighImpedence()

    def sendBits(self,payloadByte):
        self.request2Send()
        self.writePS2Payload(payloadByte,debug=True)
        

def writePS2Payload(payloadInt, sendFunc, debug=True):
    """
    call the sendFunc 11 times, once per bit of msg with values in the following order 
    * start: 0 (1 bit)
    * msg: 8 bits least significant first, only a byte of the int is sent, so BE CAREFUL !
    * parity: odd parity on 1 bit
    * stop: 1 (1 bit)
    if the debug argument is True, then the outgoing bit stream is printed to console, in 
    binary string representation, least significant, i.e. first bit to be sent, to the right 
    """
    start  = 0
    stop   = 1
    pBits  = payloadInt & 255
    parity = getParity(pBits)
    bits   = (stop << 10) | (parity << 9) | (pBits << 1) | start  # sending order right to left
    debug and print ('bit stream to send (right bit sent first!): ' + bin(bits))
    for i in range(11):
        sendFunc((bits>>i) & 1)


def readPS2Bits(readFunc):
    """ Read a bit at a time to extract the data from the  PS/2 protocol
    bits are read in the following order
    * startBit: 1 bit
    * payload: 8 bits with LEAST Significant bit FIRST
    * Parity:  1 bit: 0 if odd number of bits are 1,  1 if even number, thus parity + count(msg bits) is always odd!
    * StopBit: 1 bit
    return a tuple of genuine integer values 
    * (payload,parity,start,stop) 
    """
    start = readFunc()
    payload = 0
    for i in range(8):
        payload |= readFunc() << i
    parity =  readFunc()
    stop = readFunc()
    return (payload,parity,start,stop)

def readFunc(clockPin,dataPin):
    """
    The Data and Clock lines are both open collector.  A resistor is connected between each line and +5V, 
    so the idle state of the bus is high. When the keyboard or mouse wants to send information, it first 
    checks the Clock line to make sure it's at a high logic level.  If it's not, the host is inhibiting 
    communication and the device must buffer any to-be-sent data until the host releases Clock.  The 
    Clock line must be continuously high for at least 50 microseconds before the device can begin to 
    transmit its data. 
    
    As I mentioned in the previous section, the keyboard and mouse use a serial protocol with 11-bit frames.  
    These bits are:
    1 start bit.  This is always 0.
    8 data bits, least significant bit first.
    1 parity bit (odd parity).
    1 stop bit.  This is always 1.

    The keyboard/mouse writes a bit on the Data line when Clock is high, 
    and it is read by the host when Clock is low.
    The Data line changes state when Clock is high and that data is valid when Clock is low.
    """
    while(clockPin.value():
          None # wait for the clock to go low
    return dataPin.value()

    
def checkParity(msgTuple):
    """
    return the comparison of the parity in the msg tuple with the 
    calculated parity of the msg tuple's msg.
    """
    return msgTuple[1] == getParity(msgTuple[0])


#"""
#test writing func
def wf(b):
    print(b)

# Test variables and functions for reading  
iCount = 0
msg = '00000001'  # least significant to the right!!!
par = str((msg.count('1') + 1 ) % 2) 
start = '0'
stop = '1'
sBits = '0b'+ stop + par + msg + start
bits =  eval(sBits)

def rf():
    global iCount, bits
    if iCount==11:
        reset()
    res = 0
    if bits & (1 << iCount):
        res = 1    
    iCount += 1
    return res

def reset():
    global iCount,bits
    iCount = 0
    par = str((msg.count('1') + 1 ) % 2)
    bits = eval('0b'+ stop + par + msg + start)

#"""
