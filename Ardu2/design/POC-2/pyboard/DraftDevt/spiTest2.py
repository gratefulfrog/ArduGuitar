#!/usr/local/bin/python3.4
# spiTest2.py
# exercise some pyboard SPI with as many 74HC595 shift registers connected
# as needed:

"""
pin   
Shift Reg 1
8  : GND
9  : Shift Reg 0, pin 14 (serial data out-> serial data in)
10 : 5v
11 : X6 SHCP (latch)
12 : X5 STCP 
13 : GND (Output Enable)
14 : X8  (Serial Data In - MOSI)
16 : 5v
Q0-Q7 : LEDs 8-15

Shift Reg 0
8  : GND
9  : not connected
10 : 5v
11 : X6 SHCP (latch)
12 : X5 STCP 
13 : GND (Output Enable)
14 : X8  (Serial Data In - MOSI)
16 : 5v
Q0-Q7 : LEDs 0-7
"""

from pyb import SPI,Pin

# declare number of bits
nbBits = 16

# create an SPI.MASTER instance on the 'X' side of the board, 
# first arg=1 means 'X side' of the board
spi = SPI(1,SPI.MASTER)

# create the shcp pin on X5 - this is the "latch" pin
shcp = Pin('X5', Pin.OUT_PP)

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
    global shcp
    global spi
    # turn off the latch
    shcp.low()
    # send the bits
    for r in onReg:
        spi.send(r)
        print("send: %d"% r)
    # turn on the latch
    shcp.high()

    
"""
import spiTest2
spiTest2.init()

"""

    
