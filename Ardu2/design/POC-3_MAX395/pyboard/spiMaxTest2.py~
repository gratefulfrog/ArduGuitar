#!/usr/local/bin/python3.4
# spiMaxTest2.py
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
onReg = [0 for x in range(int(nbBits/8))]

def init():
    # set all the leds to off"
    update()

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


straight = (0,3)
invert= (1,2)
def vol(l):
    bits = (10,11,12,13,14,15)
    for b in bits:
        off(b)
    on(bits[l/20])

def tone(l):
    tOn=7
    bits=(6,5,4,8,9)
    
    
"""
import spiTest2
spiTest2.init()
"""

    
