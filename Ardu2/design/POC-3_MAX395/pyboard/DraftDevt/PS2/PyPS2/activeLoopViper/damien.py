import pyb
from pyb import Pin

@micropython.viper
def test2(gpio:int, bits:int):
    read = ptr32(gpio + stm.GPIO_IDR)
    set_hi = ptr16(gpio + stm.GPIO_BSRRL)
    set_lo = ptr16(gpio + stm.GPIO_BSRRH)
    while bits:
        while read[0] & (1 << 0): # read X1=PA0
            break
        if bits & 1:
            set_hi[0] = 1 << 1 # write X2=PA1
        else:
            set_lo[0] = 1 << 1 # write X2=PA1
        bits >>= 1
        while not read[0] & (1 << 0): # read X1=PA0
            pass

clock = Pin('X1', Pin.IN, Pin.PULL_UP)
data = Pin('X2', Pin.OUT_OD, Pin.PULL_UP)

def run():
    start = pyb.micros()
    test2(stm.GPIOA & 0x7fffffff, 0x7fffffff)
    elapsed = pyb.elapsed_micros(start)
    print(elapsed, elapsed / 31)
    
