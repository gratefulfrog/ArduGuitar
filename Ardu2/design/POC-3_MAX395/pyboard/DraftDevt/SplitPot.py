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
The cutOff must be at least 20? Indeed, 10 is not enough... 20 is better!
cutOff of 15 still fails, producing unwanted 0 results when pressure is released.
let's go for 20 !

Then, leaving enough space: 
>>> s=SplitPot('X1',(0,5),2,20)
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
    
class SplitPotOld:
    def __init__(self,pinName,mapRange,nbSplits=2,cutOff=30):
        self.cutOff=cutOff
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
            v= self.adc.read()
            #print(v)
            vADC +=v
            delay(1)
        vADC /=avgNum
        if vADC >= self.cutOff:
            for i in range(self.nbRanges):
                if vADC in range(self.ranges[i][0],self.ranges[i][1]):
                    res = (i,self.mappers[i].v(vADC))
        return res

    def test(self):
        """ a little test routine that will conitnually read the pot and print the values
        """
        lastV = None
        try:
            while True:
                v = self.update()
                if v!=None and v!=lastV:
                    print (v)
                    lastV=v
        except KeyboardInterrupt:
            print('Done')

class SplitPot:
    """"
    less general version only works for 2 pot split,
    reads the ADC 10 times over 10ms, and aborts if any of the values is out of scope!
    """
    def __init__(self,pinName,outputRangeTuple=(0,5),cutOff=25,spacing=30):
        """
        Create an instance:
        * pinName is used for the creation of the ADC, be sure to use a pin with an ADC!
        * outputRangeTuple is the range for output values after conversion & mapping
        * cutOff is the analog reading below wich a reading is considered NOISE, and is thus ignored
        * spacing is the number of readings between the 2 pots
        """
        self.adc      = ADC(pinName)
        self.cutOff   = cutOff
        self.ranges   = [(cutOff,2048-round(spacing/2.0)),
                         (2048+round(spacing/2.0),4095)]
        self.rMaps    = [RMap(r,outputRangeTuple,True) for r in self.ranges]

    def update(self, nbReadings=10):
        """
        takes nbReadings reads, then avgs them and maps the result to the appropriate range and returns it.
        returns None if no valid value read
        """
        vADC = 0
        for i in range(nbReadings):
            v=self.adc.read()
            if v<self.cutOff or (v>self.ranges[0][1] and v<self.ranges[1][0]) or v>self.ranges[1][1]:
                return None
            vADC += v
            delay(1)
        vADC /= nbReadings
        #print(vADC)
        for i in range(2): # 2 splits
            if vADC >= self.ranges[i][0] and vADC<=self.ranges[i][1]:
                return (i,self.rMaps[i].v(vADC))
            
class SplitPotArray:
    def __init__(self,pinNames,cut):
        self.spvVec = []
        for pn in pinNames:
            self.spvVec.append([SplitPot(pn,cutOff=cut),(None,None)])
                               
    def poll(self):
        newVals = False
        for spv in self.spvVec:
            v = spv[0].update()
            if v!=None and v!=spv[1]:
                spv[1]=v
                newVals=True
        return newVals

splitPotPinNameVec = ('X1',  # 0: Master
                      'X2',  # 1: Coil A
                      'X3',  # 2: Coil B
                      'X4',  # 3: Coil C
                      'Y11', # 4: Coil D
                      'Y12') # 5: ToneRange


def test(d=10,cut=30):
    spa=SplitPotArray(splitPotPinNameVec,cut)
    try:
        while True:
            if spa.poll():
                print([v[1] for v in spa.spvVec])
            delay(d)
    except:
        print('Done.')
