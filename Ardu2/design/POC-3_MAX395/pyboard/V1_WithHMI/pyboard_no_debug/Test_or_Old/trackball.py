# trackball.py
#
# trackball quadrature resolution 1,2x,4x algos
"""
Wiring:
Red: V+ (checked out OK at both 5v and 3.3V)
Black: GND
Blue: Y-axis channel-A (leads if rotation is upwards, i.e. away from wires)
Green: Y-axis channel-B (leads if rotation is downwards)
Yellow: X-Axis channel-A (leads if rotation is right-wards, i.e. to the right when looking at the device wires at bottom)
White: X-Axis channel-B (leads if rotation is left-wards)

Some simple algorithms:
1x resolution: 
* on rise of channel-A: count += (channel-B==High ? -1 : +1)
2x resolution:  
* on rise of channel-A: count += (channel-B==High ? -1 : +1)
* on drop of channel-A: count += (channel-B==High ? +1 : -1)
4x resolution:
* on rise of channel-A: count += (channel-B==High ? -1 : +1)
* on rise of channel-B: count += (channel-A==High ? +1 : -1)
* on drop of channel-A: count += (channel-B==High ? +1 : -1)
* on drop of channel-B: count += (channel-A==High ? -1 : +1)

The circuit only has 2 interrupts available so
"""


from pyb import Pin, ExtInt
from q import EnQueueable
from state import State

"""
x1_ = pyb.Pin(blue,   pyb.Pin.IN)
x2_ = pyb.Pin(yellow, pyb.Pin.IN)
y1_ = pyb.Pin(green,  pyb.Pin.IN)
y2_ = pyb.Pin(white,  pyb.Pin.IN)
"""

class TrackBall:
    def __init__(self,qq):
        self.volEnQueueable  = EnQueueable((EnQueueable.INC,EnQueueable.VOL),qq)
        self.toneEnQueueable = EnQueueable((EnQueueable.INC,EnQueueable.TONE),qq)
        self.targCoilID = 0;
        self.x1=Pin(State.trackballStateDict['x1'], Pin.IN, Pin.PULL_DOWN)
        self.x2=Pin(State.trackballStateDict['x2'], Pin.IN, Pin.PULL_DOWN)
        self.y1=Pin(State.trackballStateDict['y1'], Pin.IN, Pin.PULL_DOWN)
        self.y2=Pin(State.trackballStateDict['y2'], Pin.IN, Pin.PULL_DOWN)
        self.extInts = (ExtInt(State.trackballStateDict['x1'],
                                   ExtInt.IRQ_RISING,
                                   Pin.PULL_DOWN,
                                   self.x11),
                        ExtInt(State.trackballStateDict['y1'],
                                   ExtInt.IRQ_RISING,
                                   Pin.PULL_DOWN,
                                   self.y11))
            
    def x11(self,unused):
        if self.x2.value():
            self.volEnQueueable.push(self.targCoilID,-1)
        else:
            self.volEnQueueable.push(self.targCoilID,1)

    def y11(self,unused):
        if self.y2.value():
            self.toneEnQueueable.push(self.targCoilID,-1)
        else:
            self.toneEnQueueable.push(self.targCoilID,1)


