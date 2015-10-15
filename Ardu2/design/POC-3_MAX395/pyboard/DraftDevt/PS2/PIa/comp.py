import pyb
from pyb import Pin

def test0(ck, da, bits:int):
    while bits:
        while ck():
            break
        da(bits & 1)
        bits >>= 1
        while not ck():
            pass


@micropython.bytecode
def test(ck, da, bits:int):
    while bits:
        while ck():
            break
        da(bits & 1)
        bits >>= 1
        while not ck():
            pass

@micropython.native
def testN(ck, da, bits:int):
    while bits:
        while ck():
            break
        da(bits & 1)
        bits >>= 1
        while not ck():
            pass

@micropython.viper
def testV(ck, da, bits:int):
    while bits:
        while ck():
            break
        da(bits & 1)
        bits >>= 1
        while not ck():
            pass

clock = Pin('X1', Pin.IN, Pin.PULL_UP)
data = Pin('X2', Pin.OUT_OD, Pin.PULL_UP)
ck = clock.value
da = data.value

def run0():
    start = pyb.micros()
    test0(ck, da, 0x7fffffff)
    elapsed = pyb.elapsed_micros(start)
    print(elapsed, elapsed / 31) 

def runt():
    start = pyb.micros()
    test(ck, da, 0x7fffffff)
    elapsed = pyb.elapsed_micros(start)
    print(elapsed, elapsed / 31) 

def runtN():
    start = pyb.micros()
    testN(ck, da, 0x7fffffff)
    elapsed = pyb.elapsed_micros(start)
    print(elapsed, elapsed / 31) 

def runtV():
    start = pyb.micros()
    testV(ck, da, 0x7fffffff)
    elapsed = pyb.elapsed_micros(start)
    print(elapsed, elapsed / 31) 

"""
results:
no spec
>>> comp.run0()
914 29.48387

* micropython.bytecode :
>>> comp.runt()
910 29.35484

@micropython.native
>>> comp.runtN()
766 24.70968

@micropython.viper
>>> comp.runtV()
243 7.83871

"""

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
"""
clock = Pin('X1', Pin.IN, Pin.PULL_UP)
data = Pin('X2', Pin.OUT_OD, Pin.PULL_UP)
"""

def runt2():
    start = pyb.micros()
    test2(stm.GPIOA & 0x7fffffff, 0x7fffffff)
    elapsed = pyb.elapsed_micros(start)
    print(elapsed, elapsed / 31)

"""
results:
>>> comp.runt2()
37 1.193548
"""
