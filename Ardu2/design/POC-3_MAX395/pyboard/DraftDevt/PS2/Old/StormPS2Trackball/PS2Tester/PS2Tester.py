"""
 * PS2tester.ino - Arduino PS/2 protocol tester
 *
 * (C) Copyright 2012 Joonas Pihlajamaa and others.
 *
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the GNU Lesser General Public License
 * (LGPL) version 2.1 which is available at
 * http://www.gnu.org/licenses/lgpl-2.1.html
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * Contributors:
 *     Joonas Pihlajamaa <jokkebk@codeandlife.com>
 *
 * Partly based on PS2keyboard version 2.4 by Christian Weichel, Paul
 * Stoffregen and others, see PS2keyboard source for all contributors:
 *
 * http://playground.arduino.cc/Main/PS2Keyboard OR
 * http://www.pjrc.com/teensy/td_libs_PS2Keyboard.html
 """

import pyb

# Device specific settings, configured for Arduino Uno
#CLOCK_PIN_INT = 1 # Pin 3 attached to INT1 in Uno

DataPin = pyb.Pin('X1',pyb.Pin.IN,pull=pyb.Pin.PULL_UP) 
ClockPin = pyb.Pin('X2', pyb.Pin.IN,pull=pyb.Pin.PULL_UP)

bufferSize = 45
buff = [] 
head = 0
tail = 0
inhibiting = False

# Open collector utility routines
"""
def hold(pin):
    pin.init(pyb.Pin.OUT_PP,pyb.Pin.PULL_DOWN) 
    pin.low()

def release(pin):
    pin.init(pyb.Pin.OUT_PP,pyb.Pin.PULL_UP)
    pin.high()
    pin.init(pyb.Pin.IN,pyb.Pin.PULL_UP)

"""
def hold(pin):
    # make it ab output pin
    pin.init(pyb.Pin.OUT_PP)
    pin.value(0)
    
def release(pin):
    # make it an input pin
    #pin.init(pyb.Pin.OUT_PP)
    #pin.high()
    pin.init(pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)


bitcount=0
incoming=0
prev_ms=0 

# The ISR for the external interrupt in write mode
def ps2int_read():
  
    global inhibiting,DataPin,head,bufferSize,tail,buff,bitcount,incoming,prev_ms 

    if (inhibiting):
        return # do nothing when clock manipulated by Arduino

    print('In: ps2int_read')
    
    val = DataPin.value()
    now_ms = pyb.millis()
    if (now_ms - prev_ms > 250):
        bitcount = incoming = 0
        print('\tIn: (now_ms - prev_ms > 250)')
    prev_ms = now_ms
    n = bitcount - 1
    if (n <= 7 and n >=0):
        incoming |= (val << n)
        print('\tIn: (n <= 7 and n >=0)')
    bitcount +=1
    if (bitcount == 11):
        print('\tIn: (bitcount == 11)')
        i = head + 1
        print('\tIn: (bitcount == 11), after head..')
        print('\tIn: bufferSize: ', str(bufferSize))
        if (i >= bufferSize):
            print('\t\tIn: (i >= bufferSize)')
            i = 0
        if (i != tail):
            print('\t\tIn: (i != tail)')
            buff[i] = incoming
            head = i
        bitcount = 0
        incoming = 0
    print('Leaving: ps2int_read')
    
writeByte =  0
curbit = parity = 0
ack = None

# The ISR for the external interrupt in read mode
def ps2int_write():
    global curbit, writeByte, parity,ClockPin,DataPin
    
    #Datapin.init(pyb.Pin.OUT_PP,pyb.Pin.PULL_UP)
    if(curbit < 8):
        if(writeByte & 1):
            parity ^= 1
            DataPin.high()
        else:
            DataPin.low()
        writeByte >>= 1
    elif (curbit == 8): # parity
        if(parity):
            DataPin.low()
        else:
            DataPin.high()
    elif(curbit == 9): # time to let go
        release(DataPin)
    else: #/ time to check device ACK and hold clock again
        hold(ClockPin)
        ack = not DataPin.value()
    curbit +=1
    #Datapin.init(pyb.Pin.IN,pyb.Pin.PULL_UP)
    
# Check if data available in ring buffer
def ps2Available():
  return head != tail

# Read a byte from ring buffer (or return \0 if empty)
def ps2Read():
    global tail, buff, bufferSize
    i = tail
    if (i == head):
        return 0
    i +=1
    if (i >= bufferSize):
        i = 0
    c = buff[i]
    tail = i
    return c

# Prepare a byte for sending to PS/2 device
def ps2Write(byte):
    global writeByte, curbit, parity, ack
    writeByte = byte
    curbit = parity = ack = 0

# Utility function to convert hex into number
def fromHex(ch):
    if(ch >= '0' and ch <= '9'):
        return ord(ch) - ord('0')
    elif(ch >= 'A' and ch <= 'F'):
        return ord(ch) - ord('A') + 10
    elif(ch >= 'a' and ch <= 'f'):
        return ord(ch) - ord( 'a') + 10
    return 0

iFunc = ps2int_read

def interFunc(unused):
    global iFunc
    iFunc()

outgoingMsgs = ['FF','FA']
outInd=0

def send2Device():
    global outgoingMsgs, outInd, iFunc, ack
    if (outInd < len (outgoingMsgs)):
        incomingByte = (fromHex(outgoingMsgs[outInd][0]) << 4) + fromHex(outgoingMsgs[outInd][1])
        """
        if(incomingByte < 0x10):
            print("> 0") # // pad a zero
        else:   
            print("> ")
        """
        print('%X'%incomingByte) # print(incomingByte, HEX); // echo back byte sent
        ps2Write(incomingByte) #; // send byte to PS/2 device

        iFunc = ps2int_write

        hold(DataPin)
        release(ClockPin)
        
        while(curbit < 11): # {} // wait until receive complete - MAY HANG!
            None
        #// now clock line is held low again and data line is released
        if ack:
            print('*ACK*')
        else:
            print('no ACK') 
        iFunc = ps2int_read
    outInd +=1
    return (outInd < len (outgoingMsgs))

def setup():
    global ClockPin, DataPin, head, tail, interFunc

    #Initialize in listening mode
    # both pins are INPUTS
    release(ClockPin)
    release(DataPin)

    # Clear ring buffer
    head = tail = 0

    # Start listening clock line
    # attachInterrupt(CLOCK_PIN_INT, ps2int_read, FALLING);
    pyb.ExtInt(ClockPin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_NONE, callback=interFunc)

    print('PS/2 tester. Enter hex pairs to send:')

def loop():
    # // Inhibit communication
    global inhibiting, ClockPin

    inhibiting = True
    hold(ClockPin)

    #// Print data received from PS/2 device
    while(ps2Available()):
        byte = ps2Read() #; // read the next key
        print('%X'%byte)

    send2Device()
    
    #// Stop inhibiting comms
    release(ClockPin)
    inhibiting = False
    
    pyb.delay(500) #;//00); //5); // give some time for device to send more
    

def run():
    setup()
    while(True):
        loop()

        
