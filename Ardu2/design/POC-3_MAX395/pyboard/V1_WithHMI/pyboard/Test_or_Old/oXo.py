#oXo.py
# devt of tremolo and vibrato functionalities

import pyb
from hardware import ShakeControl

from q import EnQueueable
from state import State

class TremVib:
    vVec = (State.vibratoLowerLimit, State.vibratoUpperLimit)
    tVec = (State.tremoloLowerLimit, State.tremoloUpperLimit)

    def doTrem(self):
        if not self.aVec[0]:
            return
        print('Tremolo Level:\n',self.tremoloLevel)
        print('Push: M Vol %s'%self.vVec[self.tremoloLevel])
        self.volEnQueueable.push(self.targCoilID,self.vVec[self.tremoloLevel])
        self.tremoloLevel ^= 1
    
    def doVib(self):
        if not self.aVec[1]:
            return
        print('Vibrato Level:\n',self.vibratoLevel)
        print('Push: M Tone %s'%self.tVec[self.vibratoLevel])
        self.toneEnQueueable.push(self.targCoilID,self.tVec[self.vibratoLevel])
        self.vibratoLevel ^= 1

    def toggleTrem(self):
        self.tremOff(not aVec[0])

    def toggleVib(self):
        self.vibOff(not self.aVec[1])

    def tremOff(self,on=False):
        self.off(0,on)

    def vibOff(self,on=False):
        self.off(1,on)

    def off(self,whatIndex,on=False):
        """
        turn on or off the control given by the whatIindex
        """
        self.aVec[whatIndex] = on
        if self.aVec[whatIndex]:
            self.ctrl.doInit()
        print( ('Vibrato' if whatIndex else 'Tremolo')+':\t' + str(self.aVec[whatIndex]))

    def __init__(self,q):
        self.volEnQueueable=EnQueueable(EnQueueable.VOL,q)
        self.toneEnQueueable=EnQueueable(EnQueueable.TONE,q)
        self.targCoilID = 0
        # create the control with no off func, and autoOff disabled, and no leds!
        self.ctrl= ShakeControl(tfx=self.doTrem,
                                tfy=self.doVib)
        #active vect Trem,Vib
        self.aVec = [False,False]
        self.tremoloLevel = self.vibratoLevel = 1

    def mainLoop(self):
        self.aVec = [True,True]
        self.ctrl.doInit()
        while any(self.aVec):
            self.ctrl.update()
            pyb.delay(50)

    def poll(self):
        if any(self.aVec):
            self.ctrl.update()
        
def getTV(q):
    return TremVib(q)

                                
                 
