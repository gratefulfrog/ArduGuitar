import Classes,  SplitPot, TrackBall, oClasses, sParse, stubs
from config import PyGuitarConf
from Presets import Preset

class Q:
    qLen = 20
    
    def __init__(self):
        self.pptr = 0  # put pointer
        self.gptr = 0  # get pointer
        self.qNbObj=0  # object counter
        self.q = [None for i in range(Q.qLen)]

    def push(self,e):
        if self.qNbObj == Q.qLen:
            raise Exception('Q Full! ignoring push!')
        else:
            self.q[self.pptr] = e
            self.pptr = (self.pptr+1) % Q.qLen
            self.qNbObj += 1
            print('push:\t' + hex(e))
            
    def pop(self):
        res = None
        if self.qNbObj:
            res = self.q[self.gptr]
            self.gptr = (self.gptr+1) % Q.qLen
            self.qNbObj -=1
            print('pop:\t' + hex(res))
        return res
            

class HMIMgr:
    funcVec= ['inc', 'pb','conf','vol','tone']
    targVec = [['MVol','MTone'],
               [0,1,2,3,4,5],
               [0,1], #horizontal, vertical
               ['M','A','B','C','D','TR']]

    def __init__(self):
        self.q = Q()
        self.conf = PyGuitarConf()
        self.preset = Preset(self.conf)

        self.ld = Classes.LedDisplay(PyGuitarConf.Layout.oLD,(self.preset.currentDict,self.conf.vocab.configKeys[1:7])) #not an active component, so no Q needed
        
        self.ledPbA = Classes.LedPBArray(PyGuitarConf.Layout.oLPA,self.q,self.preset.currentDict,self.conf.vocab.configKeys[10:]+self.conf.vocab.configKeys[8:10])
        self.spa    = SplitPot.SplitPotArray(PyGuitarConf.Layout.oSPA,HMIMgr.targVec[3],self.q)        
        self.lcdMgr = oClasses.LCDMgr((self.preset.currentDict,'S','Name'),Classes.LCD(PyGuitarConf.Layout.oLCD),self.q,self.validateAndApplyLCDInput)
        self.sh     = Classes.Selector(PyGuitarConf.Layout.oSH,Classes.Selector.white,True,self.q) 
        self.sv     = Classes.Selector(PyGuitarConf.Layout.oSV,Classes.Selector.black,False,self.q)
        self.tb     = TrackBall.TrackBall(PyGuitarConf.Layout.oTB, self.q, PyGuitarConf.Layout.bg) # stubs.hTBFunc,stubs.vTBFunc,PyGuitarConf.Layout.bg)
        self.setVec = [self.inc, self.pb, self.doConf, self.vol, self.tone]
        
        self.loadConf(self.preset.presets[(self.sh.pos,self.sv.pos)])
    
    def pollInterrupters(self):
        self.ld.display()
        self.ledPbA.display()
        self.lcdMgr.display()
        self.sh.display()
        self.sv.display()
        self.tb.display()
    
    def pollPollables(self):    
        self.spa.display()
    
    def display(self):
        self.pollInterrupters()   # Poll interrupt generating objects, includes enqueue, not needed when interupts can happen!
        self.pollPollables()      #  Poll split pots includes enqueue,
        self.processQ()
        
    def processQ(self):
        work = self.q.pop()
        while (work != None):
            self.x(work)
            work = self.q.pop()

    def x(self,twoBytes):
        V = twoBytes & 0xFF
        K = (twoBytes>>8) & 0xFF
        mask = 0x80
        print('X:\tK:\t' + hex(K)) + '\tV:\t'+ hex(V) 
        for i in range(5):
            if K & (mask>>i):
                who = HMIMgr.targVec[min(i,3)][K & 0b111]
                val = (0xFF & V) if (V & 0xFF)<128 else (V & 0XFF)-256
                self.setVec[i](who,val)
                break
    
    def inc(self,who,val):
        # who is 'MVol','MTone'
        print('INC:\t' + str(who) +'\t' + str(val))
        if who == HMIMgr.targVec[0][0]: 
            # its vol
            newVol = max(0,(min(self.preset.currentDict['M'][0] + val,5)))
            self.preset.currentDict['M'][0] = newVol
            print(who +':\t' + str(newVol))
        else:
            newTone = max(0,(min(self.preset.currentDict['M'][1] + val,5)))
            self.preset.currentDict['M'][1] = newTone
            print(who +':\t' + str(newTone))
            
    def vol(self,who,val):
        # who is 'M','A','B','C','D'
        if val != self.preset.currentDict[who][0]:
            print('VOL:\t' + str(who) +'\t' + str(val))
            self.preset.currentDict[who][0] = val

    def tone(self,who,val):
        # who is 'M','A','B','C','D','TR'
        if val != self.preset.currentDict[who][1]:
            print('TONE:\t' + str(who) +'\t' + str(val))
            self.preset.currentDict[who][1] = val
    
    def doConf(self,who,val):
        # who is 0 for horizontal, 1 for vertical    
        print('CONF:\t' + str((val if not who else None,None if not who else val)))
        self.loadConf(self.preset.presets[(self.sh.pos,self.sv.pos)])
    
    def pb(self,who,unused):
        whoFuncs = [(self.ledPbA.ledPbs[0].toggle,stubs.r,self.displayCurrentConf),     # this one has no real function, currently is used for debugging
                    (stubs.y,self.saveCurrentConfAsPreset,self.ledPbA.ledPbs[1].flash), # this is the one saves the preset, 
                    (self.ledPbA.ledPbs[2].toggle,stubs.g),                             # Tremolo
                    (self.ledPbA.ledPbs[3].toggle,stubs.b),                             # Vibrato
                    (self.lcdMgr.onLeftButton,),
                    (self.lcdMgr.onRightButton,)]
        print('PB:\t' + str(who))           
        for f in whoFuncs[who]:
            f()

    
    
    def displayCurrentConf(self):
        print(self.preset.currentDict)
    
    def loadConf(self, conf):
        try:
            sp = sParse.SExpParser(conf[self.conf.vocab.configKeys[7]])
            sp.execute()
            for key in self.preset.currentDict.keys():
                self.preset.currentDict[key] = conf[key]
        except Exception as e:
            print (e)
            sp = sParse.SExpParser(self.conf.presetConf.defaultConfDict[self.conf.vocab.configKeys[7]])
            sp.execute()
            for key in self.conf.presetConf.defaultConfDict.keys():
                self.preset.currentDict[key] = self.conf.presetConf.defaultConfDict[key]
            self.preset.currentDict[self.conf.vocab.configKeys[0]] = 'DEFAULT PRESET'
            
        self.lcdMgr.loadConf()
        self.displayCurrentConf()
        
    def saveCurrentConfAsPreset(self):
        self.preset.saveCurrentConfigAsPreset((self.sh.pos,self.sv.pos))
    
    def validateAndApplyLCDInput(self,confString):
        try:
            sp = sParse.SExpParser(confString.strip())
            sp.execute()
            return True
        except Exception as e:
            print (e)
            return False
    
    """
    def validateLCDInput(self, conf):
        res  = stubs.validateConf(conf.strip())
        if res:
            self.preset.currentDict['S'] = conf.strip()
        return res  # this updates the config
    """
        
            
    
        