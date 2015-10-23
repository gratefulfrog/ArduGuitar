# v.py
# some tests...

import pyb
from pyb import Pin


@micropython.viper
def _init(gpio:int):
    set_hi = ptr16(gpio + stm.GPIO_BSRRL)
    set_lo = ptr16(gpio + stm.GPIO_BSRRH)
    
    set_hi[0] = 1 << 0 # write X1=PA0 clock
    set_lo[0] = 1 << 1 # write X2=PA1 data

clock = Pin('X1', Pin.OUT_OD, Pin.PULL_NONE)
data =  Pin('X2', Pin.OUT_OD, Pin.PULL_NONE)

def init():
    _init(stm.GPIOA & 0x7fffffff)

@micropython.viper
def read() -> int:
    x= 0xFFF
    return x

@micropython.viper
def t(r):
    x = r()
    if int(x) >> int(1):
        print (True)
        
