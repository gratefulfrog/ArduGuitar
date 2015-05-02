#!/usr/local/bin/python3.4
# vactrolControl.py
# this sends vectors of bits via spi incrementing by one at each send


from pyb import Pin

class vactrolControl:
    """simple class providing on/off functionality of a vactrol
    controlled by a pyboard bin.
    """
    def __init__(self, vactrolPin):
        self.vactrol = Pin(vactrolPin, Pin.OUT_PP)
        self.vactrol.low()

    def on(self):
        self.vactrol.high()

    def off(self):
        self.vactrol.low()
