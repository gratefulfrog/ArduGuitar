import Classes,  SplitPot, TrackBall,  oClasses, stubs
from layout import layout

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
        
        self.ld = Classes.LedDisplay(layout.oLD) #not an active component, so no Q needed
        
        self.ledPbA = Classes.LedPBArray(layout.oLPA,self.q)
        self.spa    = SplitPot.SplitPotArray(layout.oSPA,HMIMgr.targVec[3],self.q)        
        self.lcdMgr = oClasses.LCDMgr(stubs.currentDict['S'],Classes.LCD(layout.oLCD),self.q,self.validateLCDInput)
        self.sh     = Classes.Selector(layout.oSH,Classes.Selector.white,True,self.q) 
        self.sv     = Classes.Selector(layout.oSV,Classes.Selector.black,False,self.q)
        
        self.tb     = TrackBall.TrackBall(layout.oTB, stubs.hTBFunc,stubs.vTBFunc,layout.bg)
        
        self.setVec = [self.inc, self.pb,self.conf,self.vol, self.tone]
    
    def display(self):
        self.ld.display()
        self.ledPbA.display()
        self.lcdMgr.display()
        self.sh.display()
        self.sv.display()
        self.tb.display()
        self.spa.display()
        
        
        """
        self.pollInterrupters()   # Poll interrupt generating objects, includes enqueue,
        self.pollSplitPots()      #  Poll split pots includes enqueue,
        """
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
        print('V:\t'+ hex(V) +'\tK:\t' +hex(K))
        for i in range(5):
            if K & (mask>>i):
                who = HMIMgr.targVec[min(i,3)][K & 0b111]
                val = (0xFF & V) if (V & 0xFF)<128 else (V & 0XFF)-256
                """stubs.set(HMIMgr.funcVec[i],
                        who,
                        val)
                """
                self.setVec[i](who,val)
                break
    
    def inc(self,who,val):
        # who is 'MVol','MTone'
        if who == HMIMgr.targVec[0,0]: 
            # its vol
            self.ld.setV(0,stubs.currentDict['M'][0])
        else:
            self.ld.setT(0,stubs.currentDict['M'][1])
    
    def vol(self,who,val):
        # who is 'M','A','B','C','D'
        if val != stubs.currentDict[who][0]:
            stubs.currentDict[who][0] = val
            self.ld.setV(HMIMgr.targVec[3].index(who),stubs.currentDict[who][0])

    def tone(self,who,val):
        # who is 'M','A','B','C','D','TR'
        if val != stubs.currentDict[who][1]:
            stubs.currentDict[who][1] = val
            self.ld.setT(HMIMgr.targVec[3].index(who),stubs.currentDict[who][1])
    
    def conf(self,who,val):
        # who is 0 for horizontal, 1 for vertical    
        print('conf:\t' + str((val if not who else None,None if not who else val)))
    
    def pb(self,who,unused):
        whoFuncs = [(self.ledPbA.ledPbs[0].led.toggle,stubs.r),
                    (self.ledPbA.ledPbs[1].led.toggle,stubs.y),
                    (self.ledPbA.ledPbs[2].led.toggle,stubs.g),
                    (self.ledPbA.ledPbs[3].led.toggle,stubs.b),
                    (self.lcdMgr.onLeftButton,),
                    (self.lcdMgr.onRightButton,)]
                    
        for f in whoFuncs[who]:
            f()

    def validateLCDInput(self, conf):
        return stubs.validateConf(conf)  # this updates the config
        
        
    
    
        