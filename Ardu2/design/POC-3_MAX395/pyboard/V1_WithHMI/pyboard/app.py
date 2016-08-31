# app.py
# provides classes for the application level.
# This is where all the user interface calls are found!

from bitMgr import BitMgr
from dictMgr import shuntConfDict
from components import Invertable,VTable,OnOffable
from state import State
from spiMgr import SPIMgr
from configs import configDict,mapReplace
from hardware import ShuntControl,LcdDisplay,PushButtonArray,SelectorInterrupt,TrackBall,SplitPotArray
from q import Q
from config import PyGuitarConf
from Presets import Preset
import sParse
from lcdMgr import LCDMgr
import pyb
import gc

class App():
    """
    This class is the top level user facing application class.
    A single instance should be created and maintained during execution.
    The instance will maintain the user readable component classes as well
    as manage the Bits and SPI interfacing.
    usage:
    from app import App
    from state import State
    a = App()
    a.set(...)
    a.connect(...)
    a.x()
    details:
    >>> from app import App
    >>> a = App()
    >>> from state import State
    >>> a.set('PB',State.Vibrato,State.l0)
    (0, 5) ((0, 223),)
    ('masking: ', ['0', '0b11011111'])
    ('setting: (0, 5)',)
    >>> a.set('PB',State.Tremolo,State.l0)
    (0, 6) ((0, 191),)
    ('masking: ', ['0', '0b10111111'])
    ('setting: (0, 6)',)
    >>> a.x()
    xxxxxxxxxxx6543210
    ('send:\t0b1100000',)

    >>> a.set('A',State.Vol,State.l5)
    ((10, 7), (4, 5), (4, 7)) ((10, 3), (4, 31))
    ('masking: ', ['10', '0b11'])
    ('masking: ', ['4', '0b11111'])
    ('setting: ((10, 7), (4, 5), (4, 7))',)

    >>> a.connect('A',0,'B',1)
    ('setting: (8, 2)',)
    
    >>> a.x()
    setting: None
    ...

    >>> 
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
        self.pba = PushButtonArray(self.q)
        self.reset()
        self.spa = SplitPotArray(State.splitPotPinNameVec,self.q,useTracking=False)
        self.lcdMgr= LCDMgr(self.preset.currentDict,'S','Name',self.lcd,self.q,self.validateAndApplyLCDInput)
        self.selectorVec=[None,None]
        for i in range(2):
         self.selectorVec[i] = SelectorInterrupt(State.SelectorPinNameArray[i],i,self.q)
        self.tb = TrackBall(self.q)
        self.currentConfTupleKey = (-1,-1)
        self.doConf(0)  # anonymous value just to fill the argument
        self.x()

    def reset(self):
        self.shuntControl = ShuntControl(shuntConfDict)
        self.bitMgr = BitMgr()
        self.state = State()
        self.resetConnections = True
        self.coils = {}
        for coil in State.coils[:-1]:
            self.coils[coil] = Invertable(coil)
        self.coils[State.coils[-1]]= VTable(State.coils[-1])
        self.coils[State.pb] = OnOffable()
        self.spiMgr = SPIMgr(State.spiOnX,State.spiLatchPinName)
        self.lcd = LcdDisplay(State.lcdConfDict)
        # shunt, turn all to State.lOff, unshunt
        self.shuntControl.shunt()
        self.spiMgr.update(self.bitMgr.cnConfig[BitMgr.cur])
        self.shuntControl.unShunt()
        gc.collect()
        self.gcd=True

    def pollPollables(self):
        self.spa.poll()

    def mainLoop(self):
        while True:
            self.pollPollables()
            self.processQ()
            # put a sleep comand here to save energy
            pyb.delay(50)
            
    def processQ(self):
        work = self.q.pop()
        worked = False
        while (work != None):
            worked = self.doWork(work) or worked
            work = self.q.pop()
        if worked:
            self.x()
            self.gcd=False
        elif not self.gcd:
            gc.collect()  # time to do this is 5ms
            self.gcd=True

    def doWork(self,twoBytes):
        V = twoBytes & 0xFF
        K = (twoBytes>>8) & 0xFF
        mask = 0x80
        res = False
        State.printT('X:\tK:\t' + bin(K) + '\tV:\t'+ hex(V))
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
        State.printT('INC:\t%s\t%s\t%d'%('Vol' if (what & volMask) else 'Tone', who,val))
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
            #print('VOL:\t' + str(who) +'\t' + str(val))
            #print("a.set('%s',State.Vol,State.l%s)"%(who,(str(val) if val !=0 else 'Off')))
            #self.outgoing.append("a.set('%s',State.Vol,State.l%s)"%(who,(str(val)))) # if val !=0 else 'Off')))
            self.set(who,State.Vol,eval('State.l%s'%str(val)))
            self.preset.currentDict[who][0] = val
            return True
        return False

    def tone(self,who,val,unused=None,force=False):
        # who is 'M','A','B','C','D','TR'
        if force or val != self.preset.currentDict[who][1]:
            #print('TONE:\t' + str(who) +'\t' + str(val))
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
                #self.outgoing.append("a.set('%s',State.ToneRange,State.l%s)"%(targ,trVal))
                self.set(targ,State.ToneRange,eval('State.l%s'%trVal))
            if toneVal != None:
                #self.outgoing.append("a.set('%s',State.Tone,State.l%s)"%(targ,toneVal))
                self.set(targ,State.Tone,eval('State.l%s'%toneVal))
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
        State.printT('loading conf: ' + str(cf))
        self.loadConf(self.preset.presets[cf]) #self.sh.pos,self.sv.pos)])
        self.currentConfTupleKey = cf
        return True

    def pb(self,who,unused=None,unusedA=None):
        whoFuncs = ( # this one toggles splitpot tracking,currently is used for debugging
            (self.toggleTracking,self.displayCurrentConf),  # pb 0
            # this is the one saves the preset,      
            (self.saveCurrentConfAsPreset,),                # pb 1
            # Tremolo
            (self.toggleTrem,),                             # pb 2
            # Vibrato
            (self.toggleVib,),                              # pb 3
            (self.lcdMgr.onLeftButton,),                    # pb 4
            (self.lcdMgr.onRightButton,))                   # pb 5

        State.printT('PB:\t' + str(who))  
        res = False         
        for f in whoFuncs[who]:
            res = f() or res
        return res # True if who in [2,3] else False

    def toggleTracking(self):
        self.preset.currentDict[self.conf.vocab.configKeys[10]] = 0 if self.preset.currentDict[self.conf.vocab.configKeys[10]] else 1
        self.spa.track(self.preset.currentDict[self.conf.vocab.configKeys[10]])
        State.printT('Tracking:\t%d'%self.preset.currentDict[self.conf.vocab.configKeys[10]])
        return False
    
    def tracking(self,onOff):
        self.preset.currentDict[self.conf.vocab.configKeys[10]] = 1 if onOff else 0
        self.spa.track(self.preset.currentDict[self.conf.vocab.configKeys[10]])
        State.printT('Tracking:\t%d'%self.preset.currentDict[self.conf.vocab.configKeys[10]])
        return False
    
    def trem(self,onOff):
        res = ((onOff and not self.preset.currentDict[self.conf.vocab.configKeys[8]]) or (self.preset.currentDict[self.conf.vocab.configKeys[8]] and not onOff))
        self.preset.currentDict[self.conf.vocab.configKeys[8]] = 1 if onOff else 0
        v = str(0) if self.preset.currentDict[self.conf.vocab.configKeys[8]] else 'Off'
        print ("CANNOT YET SEND:\ta.set('M',State.Tremolo,l%s)"%v)
        return res
    
    def vib(self,onOff):
        res = ((onOff and not self.preset.currentDict[self.conf.vocab.configKeys[9]]) or (self.preset.currentDict[self.conf.vocab.configKeys[9]] and not onOff))
        self.preset.currentDict[self.conf.vocab.configKeys[9]] = 1 if onOff else 0
        v = str(0) if self.preset.currentDict[self.conf.vocab.configKeys[9]] else 'Off'
        print ("CANNOT YET SEND:\ta.set('M',State.Vibtrato,l%s)"%v)
        return res
    
    def toggleTrem(self):
        #trem =2, vibrato =3
        self.preset.currentDict[self.conf.vocab.configKeys[8]] = 0 if self.preset.currentDict[self.conf.vocab.configKeys[8]] else 1
        v = str(0) if self.preset.currentDict[self.conf.vocab.configKeys[8]] else 'Off'
        print ("CANNOT YET SEND:\ta.set('M',State.Tremolo,l%s)"%v)
        return True
    
    def toggleVib(self):
        #trem =2, vibrato =3
        self.preset.currentDict[self.conf.vocab.configKeys[9]] = 0 if self.preset.currentDict[self.conf.vocab.configKeys[9]] else 1
        v = str(0) if self.preset.currentDict[self.conf.vocab.configKeys[9]] else 'Off'
        print ("CANNOT YET SEND:\ta.set('M',State.Vibtrato,l%s)"%v)
        #self.outgoing.append("a.set('M',State.Vibtrato,l%s)"%v)
        return True
    
    def displayCurrentConf(self):
        return self.preset.currentDict
    
    def loadConf(self, conf):
        State.printT('loading conf: ' + str(conf))
        try:
            #res = self.doParse(conf[self.conf.vocab.configKeys[7]])
            self.doParse(conf[self.conf.vocab.configKeys[7]])
            """
            for e in res:
                #print(e)
                self.outgoing.append(e)
            """
            for key in self.preset.currentDict.keys():
                self.preset.currentDict[key] = conf[key]
        except Exception as e:
            print (e)
            self.doParse(self.conf.presetConf.defaultConfDict[self.conf.vocab.configKeys[7]])
            for key in self.conf.presetConf.defaultConfDict.keys():
                self.preset.currentDict[key] = self.conf.presetConf.defaultConfDict[key]
            self.preset.currentDict[self.conf.vocab.configKeys[0]] = 'DEFAULT PRESET'
        
        self.tone('TR',self.preset.currentDict['TR'][1],force=True)
        for c in ['A','B','C','D','M']:
            self.vol(c,self.preset.currentDict[c][0],force=True)
            self.tone(c,self.preset.currentDict[c][1],force=True)
        self.lcdMgr.loadConf()
        self.trem(self.preset.currentDict[self.conf.vocab.configKeys[8]])
        self.vib(self.preset.currentDict[self.conf.vocab.configKeys[9]])
        self.tracking(self.preset.currentDict[self.conf.vocab.configKeys[10]])
        gc.collect()
        self.gcd=True

    def doParse(self,confString):
        sp = sParse.SExpParser(self,confString.strip())
        #return sp.execute()
        sp.execute()

    def saveCurrentConfAsPreset(self):
        self.preset.saveCurrentConfigAsPreset(self.currentConfTupleKey)
        #(self.selectorVec[0].currentPosition,self.selectorVec[1].currentPosition))
        #((self.sh.pos,self.sv.pos))
    
    def validateAndApplyLCDInput(self,confString):
        try:
            #res = self.doParse(confString.strip())
            self.doParse(confString.strip())
            """
            for e in res:
               #print(e)
               self.outgoing.append(e)
            """
            #self.sendX()
            self.x()
            self.preset.currentDict[self.conf.vocab.configKeys[7]]=confString.strip()
            return True
        except Exception as e:
            print (e)
            return False


##################  old stuff !!
     
    def set(self,name,att,state):
        """
        This is called to set a coil's V or T or TR or I attribute to 
        the state argument.
        It simply looks up the instance in the coils vector and applies
        the coil's method with the state given as argument. Note that 
        the attribute is converted to an index to be passed to the coil's
        setFuncs vector to find the correct method to call.
        Once the user representation is updated, the bitMgr is called
        with the same arguments to update the NEXT bit vectors.
        usage:
        >>> a.set('M',State.Vol,State.l0)
        """
        self.coils[name].setFuncs[State.stateNeg2SetFuncIndex(att)](state)
        self.bitMgr.update(name,att,state)

    def connect(self,name,pole,otherName,otherPole):
        """
        Similar to the set method, this method calls the coil's connect
        method with the arguments as given. Then the bit representation
        is updated with the same arguments.
        The subtlty here is that if the connections have not yet been reset,
        i.e. if self.resetConnections is False, then the connections must be 
        set to 0 in the NEXT bit vector. This is only done once per updating 
        session. That means that the connections are reset, then n number of
        connection updates are applied, then the updates are exectued, 
        and only then will the NEXT vector be reset.
        """
        if not self.resetConnections:
            # if the connections have not been reset, then reset just
            # the switches part of the NEXT vector
            self.bitMgr.reset(BitMgr.switchRegEndPoints, 
                              curBool=False,
                              nexBool=True)
            self.resetConnections = True
        self.coils[name].connect(pole,(otherName,otherPole))
        self.bitMgr.update((name,pole),
                           (otherName,otherPole))

    def x(self):
        """
        This method calls the x() method on each of the coils, then on the
        bitMgr, then sends the bits to the spiMgr for hardware updating, and
        finally assigns 'False' to the resetConnections member in view of 
        future connection updates.
        usage:
        >>> a.x()
        """
        for coil in self.coils.values():
            coil.x()
        self.bitMgr.x()
        # shunt
        self.shuntControl.shunt()
        #send bits!
        self.spiMgr.update(self.bitMgr.cnConfig[BitMgr.cur])
        #unshunt
        self.shuntControl.unShunt()
        self.resetConnections = False
      
    def loadConfig(self,confName):
        """ loads a predefined configuration.
        Arg 0 : the name of the conf to load, for lookup in configDict
        Note:
        - this resets next bitMgr config and each coils next config
          before beginning since there is no 'addition' of settings here
        - it also resets all the coils connection and vtri values prior
          to executing.
        """
        self.bitMgr.reset(BitMgr.allRegEndPoints,
                          curBool=False,
                          nexBool=True)
        for coil in self.coils.values():
            coil.resetNext()
        for expr in mapReplace('self',
                               configDict[confName]):
            State.printT('Evalutating:\t' + expr)
            eval(expr , globals(),{'self':self})
        self.x()

    def showConfig(self):
        State.printT(self.bitMgr)

    def lcdSetLine(self, lineNb, line):
        State.printT('Setting LCD Line:\t%d\t"%s"'%(lineNb, line))
        self.lcd.setLn(lineNb, line)

        
