# hwTester.py
# provides testing  for the application level.
# This is where all the user interface calls are found!

#from bitMgr import BitMgr
#from dictMgr import shuntConfDict
from components import Invertable,VTable,OnOffable
from state import State
#from spiMgr import SPIMgr
from configs import configDict #,mapReplace
#from hardware import ShuntControl,LcdDisplay,PushButtonArray,SelectorInterrupt,TrackBall
from hardware import PushButtonArray,SelectorInterrupt,TrackBall
from q import Q
from config import PyGuitarConf
from Presets import Preset
#import sParse
#from lcdMgr import LCDMgr
import pyb
import gc

class App():
    """
    This class is the top level user facing application TEST class.
    A single instance should be created and maintained during execution.
    Usage:
    >>> from hwTester import App
    >>> a=App()
    >>> a.mainLoop()
    ... lots of stuff happens...
    # user enter CTRL-C to interrupt loop

    finished processing Q, now exiting mainLoop...
    """
    
    targVec = [['M','A','B','C','D','TR'], #['MVol','MTone'],
               [0,1,2,3,4,5],
               [0,1], #horizontal, vertical
               ['M','A','B','C','D','TR']]
    
    def __init__(self):
        """
        Instance creation; creation of member variables which are
        mainly instances of supporting classes.
        some details
        - resetConnections: boolean True if the connections have been reset
                            False, if they need to be reset before any new
                            connections are added.
        - coils is a vector: first is the Master-out, then coils A through D:
          [VTable, Ivertable, Ivertable, Ivertable, Ivertable]
        also,
        after creation of the SPIMgr, the update message is sent to it to 
        initialize all the pins.
        """
        self.gcd=False # true if we just did a garbage collection, false if work has been done and garbage not yet collected
        self.setVec = [self.inc, self.pb, self.doConf, self.vol, self.tone]
        self.q = Q()
        self.conf = PyGuitarConf()
        self.preset = Preset(self.conf)
        #self.pba = PushButtonArray(self.q)
        self.reset()
        #self.lcdMgr= LCDMgr(self.preset.currentDict,'S','Name',self.lcd,self.q,self.validateAndApplyLCDInput)
        self.selectorVec=[None,None]
        for i in range(2):
         self.selectorVec[i] = SelectorInterrupt(State.SelectorPinNameArray[i],i,self.q)
        self.tb = TrackBall(self.q)
        self.currentConfTupleKey = (-1,-1)
        self.doConf(0)  # anonymous value just to fill the argument
        print('**** self.x() ****\n')


    def reset(self):
        #self.shuntControl = ShuntControl(shuntConfDict)
        #self.bitMgr = BitMgr()
        self.state = State()
        self.resetConnections = True
        self.coils = {}
        for coil in State.coils[:-1]:
            self.coils[coil] = Invertable(coil)
        self.coils[State.coils[-1]]= VTable(State.coils[-1])
        self.coils[State.pb] = OnOffable()
        #self.spiMgr = SPIMgr(State.spiOnX,State.spiLatchPinName)
        #self.lcd = LcdDisplay(State.lcdConfDict)
        # shunt, turn all to State.lOff, unshunt
        #self.shuntControl.shunt()
        #self.spiMgr.update(self.bitMgr.cnConfig[BitMgr.cur])
        #self.shuntControl.unShunt()
        gc.collect()
        self.gcd=True

    def pollPollables(self):
        pass

    def mainLoop(self):
        try:
            while True:
                self.pollPollables()
                self.processQ()
                # put a sleep comand here to save energy
                pyb.delay(50)
        except:
            self.processQ()
            print('\nfinished processing Q, now exiting mainLoop...')        
            
    def processQ(self):
        work = self.q.pop()
        worked = False
        while (work != None):
            worked = self.doWork(work) or worked
            work = self.q.pop()
        if worked:
            print('**** self.x() ****\n')
            self.gcd=False
        elif not self.gcd:
            gc.collect()  # time to do this is 5ms
            self.gcd=True

    def doWork(self,twoBytes):
        V = twoBytes & 0xFF
        K = (twoBytes>>8) & 0xFF
        mask = 0x80
        res = False
        print('X:\tK:\t' + bin(K) + '\tV:\t'+ hex(V))
        #print('X:\tK:\t' + bin(K) + '\tV:\t'+ hex(V))
        for i in range(5):
            if K & (mask>>i):
                who = App.targVec[min(i,3)][K & 0b111]
                val = (0xFF & V) if (V & 0xFF)<128 else (V & 0XFF)-256
                res = self.setVec[i](who,val,K&0B11111000) or res
                break
        return res

    def inc(self,who,val,what):
        # updated version works with updated top byte INC | VOL + M,A,B,C,D
        # we need to find if its vol or tone then to which coil then call the appropriate methods
        volMask  = 0B10000
        toneMask = 0B1000
        newVal = 0
        sFunc = None
        print('INC:\t%s\t%s\t%d'%('Vol' if (what & volMask) else 'Tone', who,val))
        if what & volMask:
            sFunc = self.vol
            newVal = max(0,(min(self.preset.currentDict[who][0] + val,5)))
        elif what & toneMask:
            sFunc = self.tone
            newVal = max(0,(min(self.preset.currentDict[who][1] + val,5)))
        return sFunc(who,newVal)

    def vol(self,who,val,unused=None,force=False):
        # who is 'M','A','B','C','D'
        if force or val != self.preset.currentDict[who][0]:
            print('VOL:\t' + str(who) +'\t' + str(val))
            print("a.set('%s',State.Vol,State.l%s)"%(who,(str(val) if val !=0 else 'Off')))
            #self.outgoing.append("a.set('%s',State.Vol,State.l%s)"%(who,(str(val)))) # if val !=0 else 'Off')))
            #self.set(who,State.Vol,eval('State.l%s'%str(val)))
            self.preset.currentDict[who][0] = val
            return True
        return False

    def tone(self,who,val,unused=None,force=False):
        # who is 'M','A','B','C','D','TR'
        if force or val != self.preset.currentDict[who][1]:
            print('TONE:\t' + str(who) +'\t' + str(val))
            trVal = 'Off'
            toneVal = '0'
            if who =='TR':
                trVal =  str(val-1) if val else 'Off'
                targ = 'M'
                toneVal = None
            elif who == 'M':
                targ = who
                trVal = None
                toneVal = str(val-1) if val else 'Off'
            else:
                targ = who
                trVal = '0' if val else 'Off'
                toneVal = str(val-1) if val else 'Off'
            if trVal != None:
                print("a.set('%s',State.ToneRange,State.l%s)"%(targ,trVal))
                #self.outgoing.append("a.set('%s',State.ToneRange,State.l%s)"%(targ,trVal))
                #self.set(targ,State.ToneRange,eval('State.l%s'%trVal))
            if toneVal != None:
                print("a.set('%s',State.Tone,State.l%s)"%(targ,toneVal))
                #self.outgoing.append("a.set('%s',State.Tone,State.l%s)"%(targ,toneVal))
                #self.set(targ,State.Tone,eval('State.l%s'%toneVal))
            self.preset.currentDict[who][1] = val
            return True
        return False

    def doConf(self,who,unused0=None, unused1=None):
        # who is 0 for horizontal, 1 for vertical    
        self.selectorVec[who].setPosition()
        cf = (self.selectorVec[0].currentPosition,self.selectorVec[1].currentPosition)
        if  self.currentConfTupleKey == cf:
            return False
        self.reset()
        print('loading conf: ' + str(cf))
        #self.loadConf(self.preset.presets[cf]) #self.sh.pos,self.sv.pos)])
        self.currentConfTupleKey = cf
        return True

    # stubs!!!!
    def pb(self,who,unused=None,unusedA=None): 
        pass
    def toggleTracking(self):
        pass
    def tracking(self,onOff):
        pass
    def trem(self,onOff):
        pass
    def vib(self,onOff):
        pass
    def toggleTrem(self):
        pass
    def toggleVib(self):
        pass
    
