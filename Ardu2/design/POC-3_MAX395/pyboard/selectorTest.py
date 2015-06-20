#!/usr/local/bin/python3.4
# selectorTest?py
# exercise the Seclector class
# as needed:

"""
Pyboard:
Selector pins: X1, X2, X3
"""

from pyb import Pin
from selector import Selector

# declare the pin ids
pinIds = ('X1','X2','X3')

# global for selector
s = None

def init():
    global pinIds, s
    s = Selector([Pin(p, Pin.IN, Pin.PULL_DOWN) for p in pinIds])


    
