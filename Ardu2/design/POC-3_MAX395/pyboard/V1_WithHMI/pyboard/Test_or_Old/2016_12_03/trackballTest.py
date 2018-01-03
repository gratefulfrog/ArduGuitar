# hardware.py
# classes corresponding to physical objects in the system
# * ShuntControl
# * SelectorInterrupt  (added 2016 08 24)
# * HWDebouncedPushButton
# * ShakeControl (3-axis shake controller)
# * TremVib  (tremolo and vibrato mgt class)
# * LcdDisplayI2C  (added 2016 09 13)
# * TrackBall (added 2016 08 26)
# * SplitPot & SplitPotArray (added 2016 08 30)
#### obsolete or unused ###
# * LCDDisplay6Wire (added 2016 06 11), moved 2016 09 13
# * Selector
# * Illuminator
# * SWDebouncedPushbutton
# * IlluminatedPushbutton
# * VoltageDividerPot

#####

from pyb import Pin,  ExtInt

# class TrackBall:
# trackball quadrature resolution 1
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

The circuit only has 2 interrupts available so use resolution 1.
x1_ = pyb.Pin(blue,   pyb.Pin.IN)
x2_ = pyb.Pin(yellow, pyb.Pin.IN)
y1_ = pyb.Pin(green,  pyb.Pin.IN)
y2_ = pyb.Pin(white,  pyb.Pin.IN)
"""

class TrackBall:
    def __init__(self,qq):
        self.x1=Pin('Y9', Pin.IN, Pin.PULL_DOWN)
        self.x2=Pin('Y7', Pin.IN, Pin.PULL_DOWN)
        self.y1=Pin('Y10', Pin.IN, Pin.PULL_DOWN)
        self.y2=Pin('Y8', Pin.IN, Pin.PULL_DOWN)
        self.extInts = (ExtInt('Y9',
                               ExtInt.IRQ_RISING,
                               Pin.PULL_DOWN,
                               self.x11),
                        ExtInt('Y10',
                               ExtInt.IRQ_RISING,
                               Pin.PULL_DOWN,
                               self.y11))
            
    def x11(self,unused):
        if self.x2.value():
            print('X axis:\t-1')
        else:
            print('X axis:\t+1')

    def y11(self,unused):
        if self.y2.value():
            print('Y axis:\t-1')
        else:
            print('Y axis:\t+1')

    def __repr__(self):
        res = 'TrackBall:'                                        + \
              '\nvolEnQueueable: \t' + repr(self.volEnQueueable)  + \
              '\ntoneEnQueueable:\t' + repr(self.toneEnQueueable) + \
              '\ntargCoilID:     \t' + str(self.targCoilID)       + \
              '\nx1:             \t' + str(self.x1)               + \
              '\nx2:             \t' + str(self.x2)               + \
              '\ny1:             \t' + str(self.y1)               + \
              '\ny2:             \t' + str(self.y2)               + \
              '\nExtInts:        \t' + str([i for i in self.extInts])
        return res
