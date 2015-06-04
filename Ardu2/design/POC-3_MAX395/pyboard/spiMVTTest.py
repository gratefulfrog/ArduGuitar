#!/usr/local/bin/python3.4
# spiMVTTest.py
# exercise some pyboard SPI with as many MAX395's connected
# as needed:

"""
pin   
Shift Reg 1
pin
1  : SCLK  : Pyboard SCK X6
2  : V+    : 5v
3  : Din   : Pyboard MOSI  X8
4  : GND   : Pyboard GND
24 : CS    : Pyboard X5
23 : RESET : 5v
22 : Dout  : to next MAX395-0 pin 3
21 : V-    : -5v
5 - 20 : LEDs

Shift Reg 0
1  : SCLK  : Pyboard SCK X6
2  : V+    : 5v
3  : Din   : from Max395-1 pin 22
4  : GND   : Pyboard GND
24 : CS    : Pyboard X5
23 : RESET : 5v
22 : Dout  : not connected
21 : V-    : -5v
5 - 20 : LEDs

"""

from pyb import SPI,Pin

# declare number of bits
nbBits = 16

# create an SPI.MASTER instance on the 'X' side of the board, 
# first arg=1 means 'X side' of the board
spi = SPI(1,SPI.MASTER)

# create the cs (Chip Select) pin on X5 - this is the "latch" pin
cs = Pin('X5', Pin.OUT_PP)

# register buffer
onReg = []

def init():
    # set all the leds to off"
    global onReg, nbBits
    onReg = [0 for x in range(int(nbBits/8))]
    update()
    return show()

def goodValues(valLis):
    # return the args after filtering out any values above or below range
    global nbBits
    if valLis == (): # then do them all
        return [valid for valid in range(nbBits)]
    else: # filter off the bad values
        return [valid for valid in valLis if valid >= 0 and valid < nbBits]

def on(*qArgs):
    # turn on all the leds in args, as integers on [O,nbBits[
    # if no args, then turn all on
    global onReg
    for q in goodValues(qArgs):
        v = 1 << q % 8
        onReg[int(q/8)] |= v
    update()

def off(*qArgs):
    # turn off all the leds in args, as integers on [O,nbBits[
    # if no args, then turn all off
    global onReg
    for q in goodValues(qArgs):
        v = 1 << (q % 8)
        onReg[int(q/8)] &= ~v
    update()

def update():
    # send the data bits to the shift register
    global cs
    global spi
    # turn off the latch
    cs.low()
    # send the bits
    for r in onReg:
        spi.send(r)
        print("send:\t{0:#b}".format(r))
    # turn on the latch
    cs.high()

def straight(v=True):
    strt = (0,3)
    invt= (1,2)
    if v:
        eval ('off' + str(invt))
        eval ('on' + str(strt))
    else:
        eval ('off' + str(strt))
        eval ('on' + str(invt))
        
def vol(l):
    """ arg is a percent multiple of 20 [0,20,40,60,80,100]
    """
    bits = (2,3,4,5,6,7) 
    eval('off' + str(bits))
    on(bits[int(l/20)])
    return show()
    
def tone(l,r):
    """ arg is a percent multiple of 20 [0,20,40,60,80,100]
    """
    #tOn=7
    bits=(13,14,15,0,1)
    eval('off' + str(bits))
    if (l == 100 or r == 5):
        toneRange(5)
    else:
        toneRange(r)
        on(bits[int(l/20)])
    return show()

def toneRange(r):
    """ 
    arg is a range id on [0,5],
    5 means tone off!
    """
    bits = (12,11,10,9,8) 
    eval('off' + str(bits))
    if (r<5):
        on(bits[r])
    return show()
        
def show():
    global onReg
    return onReg
    
    
"""
import spiTest2
spiTest2.init()
"""

    
