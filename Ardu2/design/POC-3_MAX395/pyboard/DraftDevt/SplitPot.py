# SplitPot.py
"""
Using the pyboard ADC which reads 3.3v from on [0,4095].
We split the pot into equal parts after removing the cutoff value, e.g. 5.
if nbSplits = 2, and cutOff = 5, the ranges then become
[0+5, floor(4096/2) - 5[ == [5,2043[  == range(2038) 
[floor(4096/2) + 5, 4096-5[ == [2053,4091[ == range(2038)

in case of nbSplits = 3:
4096/3 = 1365.333
4096*2/3 = 2730.666
[0+5, floor(4096/3) - 5[ == [5,1360[ == range(1355) 
[floor(4096/3) + 5, floor(4096*2/3) - 5[ == [1370, 2725[ == range(1355)
[floor(4096*2/3) + 5, 4096-5[ == [2735,4091[ = range(1356)
*****

Testing revealed a great instability in the ADC.

This meant that a 10K PULL DOWN RESISTOR must be connected to the wiper.
The spacing must be at least 10, maybe more is needed?
Then, leaving enough space: 
>>> s=SplitPot('X1',[0,5],2,10)
>>> s.test()
# a moderately fast swipe..
(0, 0)
(0, 0)
(0, 1)
(0, 1)
(0, 1)
(0, 1)
(0, 1)
(0, 2)
(0, 2)
(0, 2)
(0, 2)
(0, 3)
(0, 3)
(0, 3)
(0, 3)
(0, 3)
(0, 3)
(0, 4)
(0, 4)
(0, 4)
(0, 5)
(1, 0)
(1, 0)
(1, 0)
(1, 0)
(1, 0)
(1, 1)
(1, 1)
(1, 1)
(1, 1)
(1, 1)
(1, 2)
(1, 2)
(1, 2)
(1, 2)
(1, 2)
(1, 3)
(1, 3)
(1, 4)
(1, 4)
(1, 4)
(1, 5)
(1, 5)
(1, 5)
(1, 5)
(1, 5)
(1, 5)
(1, 5)
(1, 5)
(1, 5)
(1, 5)

"""
"""
import sys
# Add the pyboard folder path to the sys.path list
sys.path.append('/home/bob/ArduGuitar/Ardu2/design/POC-3_MAX395/pyboard/')
"""

from outils import *
from pyb import Pin,ADC,delay

def getRanges(nb=2,space=5,low=0,high=4095):
    """ from the range [low,high] we split it into nb ranges with space at each end
    """
    ranges = [[0,0] for i in range(nb)]
    
    for i in range(nb):
        ranges[i][0] = floor(i*(high+1),nb)+space
        ranges[i][1] = floor((i+1)*(high+1),nb)-space
    return ranges
    
class SplitPot:
    def __init__(self,pinName,mapRange,nbSplits=2,cutOff=5):
        self.adc = ADC(pinName)
        self.nbRanges =  nbSplits
        self.ranges = getRanges(nbSplits,cutOff)
        self.mappers = [RMap(r,mapRange,True) for r in self.ranges]

    def update(self,avgNum=5):
        """ returns a tuple(range,value) if reading is ok, or None if not
        uses a rolling average to smooth the results
        """
        res = None
        vADC = 0
        for i in range(avgNum):
            vADC +=  self.adc.read()
            delay(1)
        vADC /=avgNum
        for i in range(self.nbRanges):
            if vADC in range(self.ranges[i][0],self.ranges[i][1]):
                res = (i,self.mappers[i].v(vADC))
        return res

    def test(self):
        """ a little test routine that will conitnually read the pot and print the values
        """
        try:
            while True:
                v = self.update()
                if v!=None:
                    print (v)
        except KeyboardInterrupt:
            print('Done')
