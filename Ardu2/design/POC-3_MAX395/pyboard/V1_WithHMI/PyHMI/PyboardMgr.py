import pyboard,time

class PyboardMgr():
    
    def __init__(self,portName='/dev/ttyACM0'):
        self.sendCounter = 0
        self.pyb = pyboard.Pyboard(portName)
        self.pyb.enter_raw_repl()
        try:
            #self.doBlink()
            self.send(['None',])
        except:
            pass
    
    def doBlink(self):
        self.pyb.enter_raw_repl()
        self.doBlink_()
        self.pyb.exit_raw_repl()
        
    def doBlink_(self):
        # must already have opened the chanel
        for i in range(1,5):
            self.pyb.exec('pyb.LED(%d).on()'%i)
            time.sleep(.1)
            self.pyb.exec('pyb.LED(%d).off()'%i)
            time.sleep(.1)
    
    def send(self,strList):
        #print(strList)
        # strList is  a list of string commands to send to pyb
        # channel is already open, strings sent, blink is done, channel is not closed
        res ='\n********** START SEND: %d  **********\n\n'%self.sendCounter
       # self.pyb.enter_raw_repl()
        
        strList[-1] = 'ret__='+strList[-1]
        for s in strList:
            res += self.pyb.exec(s)
        res+= self.pyb.exec('print(ret__)')
        #self.doBlink_()
        #self.pyb.exit_raw_repl()
        
        res += '\n********** END SEND: %d **********\n'%self.sendCounter
        self.sendCounter +=1
        return res
    
    