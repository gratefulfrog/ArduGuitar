# vs2.py
# non class version to implement ps2 protocol as per PS2 arduino library
# wiring:
# pins must be wired with external 1k pull up resistors!
# pin ids are hard wired in this version 

import pyb
from pyb import Pin, udelay

clock = Pin('X1', Pin.OUT_OD, Pin.PULL_NONE)
data =  Pin('X2', Pin.OUT_OD, Pin.PULL_NONE)


# external user calls: Be sure to init first!
def init():
    _init(stm.GPIOA & 0x7fffffff)
    pyb.delay(20)
    
def read():
    """ returns the unsigned byte read
    """
    return _read(stm.GPIOA & 0x7fffffff)

def write(data):
    """ write one byte of data to the ps/2 device
    """
    _write(stm.GPIOA & 0x7fffffff, data & 0xFF & 0x7fffffff)

#######
# viper code follows
######

@micropython.viper
def _init(gpio:int):
    set_hi = ptr16(gpio + stm.GPIO_BSRRL)
    set_lo = ptr16(gpio + stm.GPIO_BSRRH)

    # release clock and data
    set_hi[0] = 1 << 0 # write X1=PA0 clock
    set_hi[0] = 1 << 1 # write X2=PA1 data

@micropython.viper
def _write(gpio:int, data:int):
    read   = ptr32(gpio + stm.GPIO_IDR)
    set_hi = ptr16(gpio + stm.GPIO_BSRRL)
    set_lo = ptr16(gpio + stm.GPIO_BSRRH)

    parity = 1  # negative parity
    
    # release clock and data, waith 300us
    set_hi[0] = 1 << 1 # write X2=PA1 data
    set_hi[0] = 1 << 0 # write X1=PA0 clock
    udelay(300)
    
    # lock the clock, wait another 300us
    set_lo[0] = 1 << 0 # write X1=PA0 clock
    udelay(300)

    #lock the data, wait 10us, why???
    set_lo[0] = 1 << 1 # write X1=PA0 data
    udelay(10)

    # release the clock, this is the zero start bit
    # start bit = 0
    set_hi[0] = 1 << 0 # write X1=PA0 clock

    udelay(10) # why is this delay needed?
    
    # wait for device to take control of clock
    # wait for a LOW clock, then send a bit
    while read[0] & (1 << 0): # read X1=PA0 clock
        pass
    # clear to send data
    for i in range(8):
        if(data & 0x01):
            set_hi[0] = 1 << 1 # write X2=PA1 data
        else:
            set_lo[0] = 1 << 1 # write X2=PA1 data
        # bit is sent!
        
        # wait for clock to go HIGH
        while not read[0] & (1 << 0): # read X1=PA0 clock
            pass
        # wait for clock to go LOW
        while read[0] & (1 << 0): # read X1=PA0 clock
            pass
        # factor in the parity
        parity ^= (data & 0x01)
        # shift the data to position the next bit to send
        data >>= 1
        
    # at this point, we have sent all the data,
    # now send the parity bit
    if parity:
        set_hi[0] = 1 << 1 # write X2=PA1 data
    else:
        set_lo[0] = 1 << 1 # write X2=PA1 data
    # wait for clock to go HIGH
    while not read[0] & (1 << 0): # read X1=PA0 clock
        pass
    # wait for clock to go LOW
    while read[0] & (1 << 0): # read X1=PA0 clock
        pass
       
    # now the stop bit
    set_hi[0] = 1 << 1 # write X2=PA1 data
    
    # wait for clock to go HIGH
    while not read[0] & (1 << 0): # read X1=PA0 clock
        pass
    # wait for clock to go LOW
    while read[0] & (1 << 0): # read X1=PA0 clock
        pass

    # mode switch
    while not ( read[0] & (1 << 0) and read[0] & (1 << 1)):
        pass
    
    # hold up incoming data by locking the clock
    set_lo[0] = 1 << 0 # write X2=PA1 clock
        
@micropython.viper
def _read(gpio:int) -> int:
    read = ptr32(gpio + stm.GPIO_IDR)
    set_hi = ptr16(gpio + stm.GPIO_BSRRL)
    set_lo = ptr16(gpio + stm.GPIO_BSRRH)

    bit = 0X01
    res = 0

    # release the clock and data
    set_hi[0] = 1 << 0 # write X1=PA0 clock
    set_hi[0] = 1 << 1 # write X2=PA1 data
    
    udelay(50)  # I don't know why we wait for 1/2 clock cycle?

    # wait for the clock to go LOW
    while read[0] & (1 << 0): # read X1=PA0 clock
        pass

    # ignore start bit
    while not read[0] & (1 << 0): # read X1=PA0 clock
        pass

    # now read in the 8 data bits
    for i in range(8):
        # wait for the clock to go LOW
        while read[0] & (1 << 0): # read X1=PA0 clock
            pass
        #read the bit on the data pin
        if read[0] & (1 << 1): # read X2=PA1 data
            res |= bit 
        while not read[0] & (1 << 0): # read X1=PA0 clock
            pass
        bit <<= 1
        
    #ignore parity bit, wait a full clock cycle
    while read[0] & (1 << 0): # read X1=PA0 clock
        pass
    while not read[0] & (1 << 0): # read X1=PA0 clock
        pass

    #ignore stop bit, wait a full clock cycle
    while read[0] & (1 << 0): # read X1=PA0 clock
        pass
    while not read[0] & (1 << 0): # read X1=PA0 clock
        pass

    #hold incoming data, lock the clock
    set_lo[0] = 1 << 0 # write X1=PA0 clock
    return res

