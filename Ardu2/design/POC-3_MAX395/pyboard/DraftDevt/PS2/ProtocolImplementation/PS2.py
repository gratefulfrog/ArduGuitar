# PS2.py

# some stuff for PS/2...
# after some thought, I realized that the 'request to send' comprises the O value start bit!
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

    def interpretMsgTuple(msgTuple):
        res = 'Payload (HEX): '  + hex(msgTuple[0])[2:].upper()
        res += '\nParity: ' + str(msgTuple[1])
        res += '\nStart: '  +  str(msgTuple[2])
        res += '\nStop: '   +  str(msgTuple[3])
        return res

    
    def checkParity(msgTuple):
        """
        return the comparison of the parity in the msg tuple with the 
        calculated parity of the msg tuple's msg.
        """
        return msgTuple[1] == PS2.getParity(msgTuple[0])

    def __init__(self,clockPinName,dataPinName,debug=True):
        self.clock  = pyb.Pin(clockPinName,pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)
        self.data   = pyb.Pin(dataPinName,pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)
        self.debug = debug
        print('PS2 Obect init: OK')
        print('Debug is ' + str(self.debug))

    def clockHighImpedence(self):
        """
        The clock pin is released!
        """
        self.clock.init(pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)

    def dataHighImpedence(self):
        """
        The data pin is released!
        """
        self.data.init(pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)

    def clockLowValue(self):
        self.clock.init(pyb.Pin.OUT_OD,pull=pyb.Pin.PULL_NONE)
        #pyb.udelay(5)
        self.clock.value(0)

    def dataLowValue(self):
        self.data.init(pyb.Pin.OUT_OD,pull=pyb.Pin.PULL_NONE)
        #pyb.udelay(5)
        self.data.value(0)

    def enableReceive(self):
        self.clockHighImpedence()
        self.dataHighImpedence()

    def request2Send(self):
        # first make a request to send:
        self.clockLowValue()
        pyb.udelay(100)
        self.dataLowValue()  ## this is the start bit, so it has to be taken out of the sending method!
        self.clockHighImpedence()

    def sendBits(self,payloadByte, withStartBit=False):
        """ this is tough!
        1. make the request to send
        2. do the sending
        3. release the data line (high impedence)
        4. wait for data to go low (set by device)
        5. wait for clock to go low (set by device)
        6. wait for both to be high impedence (set by device)
        """
        self.request2Send()
        self.writePS2Payload(payloadByte,withStartBit)
        self.dataHighImpedence()
        if self.debug:
            self.data.value(0)
            self.clock.value(0)
        while self.data.value():
            None # wait for device to bring data low
        while self.clock.value():
            None # wait for device to bring clock low
        if self.debug:
            self.data.value(1)
            self.clock.value(1)
        while not (self.clock.value() and self.data.value()):
                None # wait for device to release clock and data

                
    def writePS2Payload(self, payloadInt, withStartBit=False):
        """
        UPDATE 2015 10 09: After some thinking, it seems that the start bit is part of the
        'request to send' so I have added the argument 'withStartBit' to disable/enable the 
        sending of a zero valued start bit or not.  
        call the sendFunc 11 times, once per bit of msg with values in the following order 
        * start bit : 0 (1 bit)  # I now believe that this zero bit is part of the request to send! so I have 
          added the argument to control if it is sent or not, let's suppose it is not sent!
        * msg: 8 bits least significant first, only a byte of the int is sent, so BE CAREFUL !
        * parity: odd parity on 1 bit
        * stop: 1 (1 bit)
        if the debug argument is True, then the outgoing bit stream is printed to console, in 
        binary string representation, least significant, i.e. first bit to be sent, to the right 
        """
        start  = 0
        stop   = 1
        pBits  = payloadInt & 255 # ensure that we have only one byte of data
        parity = PS2.getParity(pBits)
        nbBits2Send = 10
        bits   = (stop << (nbBits2Send-1)) | (parity << (nbBits2Send-2)) | pBits   # sending order right to left
        if withStartBit:
            nbBits2Send = 11
            bits = bits << 1 | start
        self.debug and print ('bit stream to send (right bit sent first!): ' + bin(bits))
        for i in range(nbBits2Send):
            self.sendFunc((bits>>i) & 1)
            
    def sendFunc(self, bit):
        """
        4)   Wait for the device to bring the Clock line low.
        5)   Set/reset the Data line to send the first data bit
        6)   Wait for the device to bring Clock high.
        7)   Wait for the device to bring Clock low.
        8)   Repeat steps 5-7 for the other seven data bits and the parity bit
        9)   Release the Data line.
        10) Wait for the device to bring Data low.
        11) Wait for the device to bring Clock  low.
        12) Wait for the device to release Data and Clock
        """
        if self.debug:
            self.clock.value(0)
        while (self.clock.value()):
            None
        self.data.value(bit)
        self.debug and print(bit)
        if self.debug:
            self.clock.value(1)
        while not self.clock.value():
            None
            
    def readBits(self):
        """ Read a bit at a time to extract the data from the  PS/2 protocol
        bits are read in the following order
        * startBit: 1 bit
        * payload: 8 bits with LEAST Significant bit FIRST
        * Parity:  1 bit: 0 if odd number of bits are 1,  1 if even number, thus parity + count(msg bits) is always odd!
        * StopBit: 1 bit
        return a tuple of genuine integer values 
        * (payload,parity,start,stop) 
        """
        start = self.readFunc()
        payload = 0
        for i in range(8):
            payload |= self.readFunc() << i
        parity =  self.readFunc()
        stop = self.readFunc()
        resTuple = (payload,parity,start,stop)
        self.debug and print (PS2.interpretMsgTuple(resTuple))
        self.debug and print ('Parity check: ' + str(PS2.checkParity(resTuple)))
        return resTuple

    def readFunc(self):
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
        self.debug and self.clock.value(0)
        while self.clock.value():
            None # wait for the clock to go low
        if self.debug:
            res=rf()
        else:
            res = self.data.value()
        self.debug and self.clock.value(1)
        while not self.clock.value():
            None # wait for clock to go high
        return res
    
    

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
