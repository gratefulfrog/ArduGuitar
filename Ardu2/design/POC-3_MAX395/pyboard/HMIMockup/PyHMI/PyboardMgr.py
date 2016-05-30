import pyboard,time

class PyboardMgr():
    
    def __init__(self,portName='/dev/ttyACM0'):
        self.sendCounter = 0
        self.pyb = pyboard.Pyboard(portName)
        self.pyb.enter_raw_repl()
        self.doBlink()
    
    """
    def open(self):
        return
        #self.pyb.enter_raw_repl()
    def close(self): 
        return   
        #self.pyb.exit_raw_repl()
    """    
    def doBlink(self):
        #self.open()
        self.doBlink_()
        #self.close()
        
    def doBlink_(self):
        # must already have opened the chanel
        for i in range(1,5):
            self.pyb.exec('pyb.LED(%d).on()'%i)
            time.sleep(.1)
            self.pyb.exec('pyb.LED(%d).off()'%i)
            time.sleep(.1)
    
    def send(self,strList):
        # strList is  a list of string commands to send to pyb
        # channel is opened, strings sent, blink is done, channel is closed
        res ='\n********** START SEND: %d  **********\n\n'%self.sendCounter
        #print(strList)
        strList[-1] = 'ret__='+strList[-1]
        #self.open()
        for s in strList:
            res += self.pyb.exec(s)
        res+= self.pyb.exec('print(ret__)')
        #self.doBlink_()
        #self.close()
        res += '\n********** END SEND: %d **********\n'%self.sendCounter
        self.sendCounter +=1
        return res
    
    