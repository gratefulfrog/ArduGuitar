#!/usr/local/bin/python3.4
# spiMgr.py
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

class SPIMgr():
    def __init__(self,spiOnX,latchPin):
        # create an SPI.MASTER instance on the 'X' side of the board, 
        # first arg=1 means 'X side' of the board
        boardSide = 1
        if not spiOnX:
            boardSide = 2
        self.spi = SPI(boardSide,SPI.MASTER)
        # create the shcp pin on the "latch" pin
        self.shcp = Pin(latchPin, Pin.OUT_PP)

    def update(self,bitArray):
        # send the data bits to the shift register
        # turn off the latch
        self.shcp.low()
        # send the bits
        for r in bitArray:
            self.spi.send(r)
            #### COMMENT NEXT LINE FOR Off-Board TESTS!
            print("send:\t{0:#b}".format(r))
        # turn on the latch
        self.shcp.high()

    def __repr__(self):
        return 'SPIMgr:' + \
            '\n' + str(self.spi) + \
            '\nSHCP:\n' + str(self.shcp)
