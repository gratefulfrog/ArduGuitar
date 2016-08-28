# SplitPot.py
"""
Using the pyboard ADC which reads 3.3v from on [0,4095].
We split the pot into equal parts after removing the cutoff value, e.g. 30.
*****

Testing revealed a great instability in the ADC.

This meant that a 10K PULL DOWN RESISTOR must be connected to the wiper.
The cutOff must be at least 25? Indeed, 30 is better!
In additon, we poll the ADC 10 times at 1ms intervals to get an avg value and if any of the polls
are bad, then all is rejected.
Results:
>>> from SplitPot import *
>>> test()
sp_0            sp_1            sp_2            sp_3            sp_4            sp_5_ToneRage
(None, None)    (None, None)    (None, None)    (None, None)    (None, None)    (None, None)
(None, None)    (1, 3)          (None, None)    (None, None)    (None, None)    (None, None)
(None, None)    (1, 1)          (None, None)    (None, None)    (None, None)    (None, None)
(None, None)    (1, 1)          (1, 0)          (None, None)    (None, None)    (None, None)
(None, None)    (1, 1)          (1, 0)          (None, None)    (0, 4)          (None, None)
(None, None)    (1, 1)          (1, 0)          (None, None)    (0, 3)          (None, None)
(None, None)    (1, 1)          (1, 0)          (None, None)    (0, 4)          (None, None)
(None, None)    (1, 1)          (0, 3)          (0, 3)          (0, 4)          (None, None)
(None, None)    (1, 1)          (0, 3)          (1, 1)          (0, 4)          (None, None)
(None, None)    (0, 4)          (0, 3)          (1, 1)          (0, 4)          (None, None)
(None, None)    (0, 4)          (1, 1)          (1, 1)          (0, 4)          (None, None)
(None, None)    (1, 0)          (1, 1)          (1, 1)          (0, 4)          (None, None)
(None, None)    (1, 1)          (1, 1)          (1, 1)          (0, 4)          (None, None)
(1, 1)          (1, 1)          (1, 1)          (1, 1)          (0, 4)          (None, None)
(1, 2)          (1, 1)          (1, 1)          (1, 1)          (0, 4)          (None, None)
(1, 3)          (1, 1)          (1, 1)          (1, 1)          (0, 4)          (None, None)
(1, 3)          (1, 1)          (1, 1)          (1, 1)          (0, 4)          (1, 1)      
(1, 3)          (1, 1)          (1, 1)          (1, 1)          (0, 3)          (1, 1)      
(1, 3)          (1, 1)          (1, 1)          (1, 1)          (1, 1)          (1, 1)      
(1, 3)          (0, 4)          (1, 1)          (1, 0)          (1, 1)          (1, 1)      
(1, 3)          (1, 0)          (1, 1)          (1, 0)          (1, 1)          (1, 1)      
(1, 3)          (1, 1)          (1, 1)          (1, 0)          (1, 1)          (1, 1)      
(1, 3)          (1, 1)          (1, 1)          (0, 4)          (1, 1)          (1, 1)      
(1, 3)          (1, 1)          (0, 2)          (0, 4)          (1, 1)          (1, 1)      
(1, 3)          (0, 3)          (0, 2)          (0, 4)          (1, 1)          (1, 1)      
(1, 4)          (0, 3)          (0, 2)          (0, 4)          (1, 1)          (1, 1)      
Done.
"""

from outils import *
from pyb import Pin,ADC,delay

class SplitPot:
    """"
    This version only works for 2 pot split,
    reads the ADC 10 times over 10ms, and aborts if any of the values is out of scope!
    """
    def __init__(self,pinName,isToneRange=False,outputRangeTuple=(0,5),cutOff=25,spacing=30):
        """
        Create an instance:
        * pinName is used for the creation of the ADC, be sure to use a pin with an ADC!
        * outputRangeTuple is the range for output values after conversion & mapping
        * cutOff is the analog reading below wich a reading is considered NOISE, and is thus ignored
        * spacing is the number of readings between the 2 pots
        * if isToneRange, then the first range is reduced to length of 0
        """
        self.adc      = ADC(pinName)
        self.cutOff   = cutOff
        self.ranges   = [(cutOff,cutOff+1 if isToneRange else 2048-round(spacing/2.0)),
                         (2048+round(spacing/2.0),4095-cutOff)]
        self.rMaps    = [RMap(r,outputRangeTuple,True) for r in self.ranges]
        self.isToneRange = isToneRange
        self.tracking  = False
        self.update    = self.noTrackingUpdate

    def track(self,onOff):
        self.tracking  = onOff
        if onOff:
            self.update = self.trackingUpdate
        else:
            self.update = self.noTrackingUpdate
        # other stuff to be added here.
        """
        if onOff:
            self.volEnQueueable = EnQueueable((EnQueueable.INC,EnQueueable.VOL),self.q)
            self.toneEnQueueable = EnQueueable((EnQueueable.INC,EnQueueable.TONE),self.q)
            self.vt=self.doTrackingVT
        else:
            self.volEnQueueable = EnQueueable(EnQueueable.VOL,self.q)
            self.toneEnQueueable = EnQueueable(EnQueueable.TONE,self.q)
            self.vt=self.doVT
        """
    def trackingUpdate(self, error=400):
        """ error allows for a bad finger move at start of tracking
        """
        vInit=self.adc.read()
        if vInit<self.cutOff or (vInit>self.ranges[0][1] and vInit<self.ranges[1][0]) or vInit>self.ranges[1][1]:
            return None
        vADCmin = vADCmax = v = vInit
        curRange = None
        for i in range((1 if self.isToneRange else 0),2): # 2 splits if not ToneRange, only second split if ToneRange
            if vInit >= self.ranges[i][0] and vInit<=self.ranges[i][1]:
                curRange=i
                break
        if curRange==None:
            return None
        while v >= self.ranges[curRange][0] and v<=self.ranges[curRange][1]:
            vADCmin = min(vADCmin,v)
            vADCmax = max(vADCmax,v)
            v=self.adc.read()
        sign = +1
        if abs(vADCmax-vInit)<=error:
            sign = -1
        print (vADCmax,vADCmin,vInit,sign)
        return (curRange, sign*(max(1,self.rMaps[curRange].v(vADCmax-vADCmin))))

    def noTrackingUpdate(self, nbReadings=10):
        """
        takes nbReadings reads, then avgs them and maps the result to the appropriate range and returns it.
        returns None if no valid value read
        """
        vADC = 0
        for i in range(nbReadings):
            v=self.adc.read()
            if v<self.cutOff or (v>self.ranges[0][1] and v<self.ranges[1][0]) or v>self.ranges[1][1]:
                #print(v)
                return None
            vADC += v
            delay(1)
        vADC /= nbReadings
        #print(vADC)
        for i in range((1 if self.isToneRange else 0),2): # 2 splits if not ToneRange, only second split if ToneRange
            if vADC >= self.ranges[i][0] and vADC<=self.ranges[i][1]:
                return (i,self.rMaps[i].v(vADC))
            
class SplitPotArray:
    """
    This is the apllication class that will be used to manage the split pots in an array
    the last split pot is the ToneRange.
    polling takes 10ms per pot, so a total of 60ms for the 6 pots!
    Be careful to consider that time when putting a delay in the app mainloop between polls
    """
    
    def __init__(self,pinNames,cut):
        self.spvVec = []
        for pn in pinNames[:-1]:
            self.spvVec.append([SplitPot(pn,cutOff=cut),(None,None)])
        self.spvVec.append([SplitPot(pinNames[-1],isToneRange=True,cutOff=cut),(None,None)])
                               
    def poll(self):
        newVals = False
        for spv in self.spvVec:
            v = spv[0].update()
            if v!=None:# and v!=spv[1]:
                spv[1]=v
                newVals=True
        return newVals

    def track(self,onOff):
        for spv in self.spvVec:
            spv[0].track(onOff)
    

splitPotPinNameVec = ('X1',  # 0: Master
                      'X2',  # 1: Coil A
                      'X3',  # 2: Coil B
                      'X4',  # 3: Coil C
                      'Y11', # 4: Coil D
                      'Y12') # 5: ToneRange


def output(lis,headings=False):
    """ print out the list with tabs between the elts
    """
    res=''
    for e in lis[:-1]:
        res += ljust(str(e),12) + '\t'
    res += ljust(str(lis[-1])+('_ToneRage' if headings else ''),12)
    print(res)

def test(d=10,cut=30,track=False):
    """
    create the SplitPotArray,
    then poll it every 'd' milliseconds
    and output the results if there is a new valid value
    """
    spa=SplitPotArray(splitPotPinNameVec,cut)
    spa.track(track)
    output(['sp_'+str(i) for i in range(len(spa.spvVec))],True)
    output([v[1] for v in spa.spvVec])
    #try:
    while True:
        if spa.poll():
            output([v[1] for v in spa.spvVec])
        delay(d)
    #except:
    #    print('Done.')
