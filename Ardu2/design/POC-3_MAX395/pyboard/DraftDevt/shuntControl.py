#!/usr/local/bin/python3.4
# shuntControl.py

from pyb import Pin,Timer
from dictMgr import shuntConfDict
from state import State

class ShuntControl:
    """simple class providing on/off functionality of a vactrol
    controlled by a pyboard bin.
    """
    def __init__(self, confData):
        p = Pin(confData['p'] , mode=Pin.OUT_PP)
        tim = Timer(confData['t'],freq=confData['f'])
        self.control = tim.channel(confData['c'],Timer.PWM, pin=p)
        self.control.pulse_width_percent(0)

    def shunt(self, percent = 20):
        State.printT('Shunting')
        self.control.pulse_width_percent(percent)

    def unShunt(self):
        State.printT('UNshunting')
        self.control.pulse_width_percent(0)

    def __repr__(self):
        return 'ShuntControl: ' + '\n\t'  \
            'Timer.channel:\t' + str(self.control)
