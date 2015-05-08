#!/usr/local/bin/python3.4
# spiMaxTest.py
# exercise some pyboard SPI with a Max395
"""
pin
1  : CLK  : Pyboard SCK X6
2  : V+  : 5v
3  : Din : Pyboard MOSI  X8
4  : GND : Pyboard GND

24 : CS    : Pyboard X5
23 : RESET : 5v
22 : Dout  : not connected (or to next MAX395)
21 : V-    : -5v
 
5 - 20 : LEDs
"""

from pyb import SPI,Pin

# declare number of bits
nbBits = 8

# create an SPI.MASTER instance on the 'X' side of the board, 
# first arg=1 means 'X side' of the board
spi = SPI(1,SPI.MASTER)

# create the cs (chip select) pin on X5 - this is the "latch" pin
cs = Pin('X5', Pin.OUT_PP)

# register buffer
onReg = 0

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
        v = 1 << q
        onReg |= v
    update()

def off(*qArgs):
    # turn off all the leds in args, as integers from 0 to 7
    # if no args, then turn all on
    global onReg
    for q in goodValues(qArgs):
        v = 1 << q
        onReg &= ~v
    update()

def update():
    # send the data bits to the shift register
    global cs
    global spi
    # turn off the latch
    cs.low()
    # send the bits
    spi.send(onReg)
    print("send:\t{0:#b}".format(onReg))
    # turn on the latch
    cs.high()

    
"""
import spiMaxTest
spiMaxTest.init()

"""

    
