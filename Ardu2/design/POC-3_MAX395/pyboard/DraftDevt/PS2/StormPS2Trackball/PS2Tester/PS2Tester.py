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

DataPin = pyb.Pin('X1',pyb.Pin.IN) 
ClockPin = pyb.Pin('X2', pyb.Pin.IN)

buff= [] 
head = tail = 0
inhibiting = False

# Open collector utility routines
"""
def hold(pin):
    pin.low()
    pin.init(pyb.Pin.OUT_PP,pyb.Pin.PULL_DOWN) 

def release(pin):
    pin.init(pyb.Pin.IN,pyb.Pin.PULL_UP)
    pin.high() 
"""

def hold(pin):
    pin.value(0)
    pin.init(pyb.Pin.OUT_PP)

def release(pin):
    pin.init(pyb.Pin.IN,pull=pyb.Pin.PULL_UP)

# The ISR for the external interrupt in write mode
def ps2int_read():
  bitcount=0
  incoming=0
  prev_ms=0 
  
  global inhibiting,DataPin,head,BUFFER_SIZE,tail,buff
  
  if (inhibiting):
    return # do nothing when clock manipulated by Arduino

  val = DataPin.value()
  now_ms = pyb.millis()
  if (now_ms - prev_ms > 250):
    bitcount = incoming = 0
  prev_ms = now_ms
  n = bitcount - 1
  if (n <= 7 and n >=0):
    incoming |= (val << n)
  bitcount +=1
  if (bitcount == 11):
    i = head + 1
    if (i >= BUFFER_SIZE):
        i = 0
    if (i != tail):
      buff[i] = incoming
      head = i
    bitcount = 0
    incoming = 0


writeByte =  0
curbit = parity = 0
ack = None

# The ISR for the external interrupt in read mode
def ps2int_write():
    global curbit, writeByte, parity,ClockPin,DataPin
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

# Check if data available in ring buffer
def ps2Available():
  return head != tail

# Read a byte from ring buffer (or return \0 if empty)
def ps2Read():
    global tail, buff, BUFFER_SIZE
    i = tail
    if (i == head):
        return 0
    i +=1
    if (i >= BUFFER_SIZE):
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

def setup():
    global ClockPin, DataPin, head, tail

    #Initialize in listening mode
    release(ClockPin)
    release(DataPin)

    # Clear ring buffer
    head = tail = 0

    # Start listening clock line
    #attachInterrupt(CLOCK_PIN_INT, ps2int_read, FALLING);
    pyb.ExtInt(ClockPin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback=None) 
    pyb.ExtInt(ClockPin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback=ps2int_read)
    print('PS/2 tester. Enter hex pairs to send:')


def loop():
    # // Inhibit communication
    global inhibiting, ClockPin, DataPin, ack, incomingByte, curbit
    inhibiting = True
    hold(ClockPin)

    #// Print data received from PS/2 device
    while(ps2Available()):
        byte = ps2Read() #; // read the next key
        print('%X'%byte)

    # give it an 'enalbe data reporting message' F4
    incomingByte = (fromHex('F') << 4) + fromHex('4')
    
    print('%X'%incomingByte)
    ps2Write(incomingByte) #; // send byte to PS/2 device
    
    pyb.ExtInt(ClockPin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback=None)
    pyb.delay(1)
    pyb.ExtInt(ClockPin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback=ps2int_write)
    
    hold(DataPin)
    release(ClockPin)
    
    while(curbit < 11): # {} // wait until receive complete - MAY HANG!
        None
    # now clock line is held low again and data line is released

    if ack:
        print("*ACK*")
    else:
        print("no ACK") 

    pyb.ExtInt(ClockPin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback=None)
    pyb.delay(1)
    pyb.ExtInt(ClockPin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback=ps2int_read)
    
    
    #// Stop inhibiting comms
    release(ClockPin)
    inhibiting = False
    
    pyb.delay(50) #;//00); //5); // give some time for device to send more
    

