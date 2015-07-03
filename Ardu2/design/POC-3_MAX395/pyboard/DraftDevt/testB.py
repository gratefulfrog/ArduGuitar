# testB.py
# test helpers for pushbutton classes

from pyb import Pin
from hardware  import *

def pp():
    """ just a little function to be called when the pushbutton goes HIGH
    """
    print('toto')

def test(actionFunc=pp):
    p = Pin('X1', Pin.IN, Pin.PULL_DOWN)
    i = Illuminator(Pin('X2', Pin.OUT_PP))
    b = IlluminatedPushbutton(p, i, actionFunc)
    while True:
        b.update()
        
    
