# sutbs
class Q:
    def __init__(self):
        self.q=[]
    def push(self,e):
        self.q.append(e)


class Thing:
    def __init__(self,n,t=True):
        self.name=n
        self.yes = t

    def pollFunc(self):
        return (self.name, self.yes)

# end stubs

        
class PollMgr:
    class Pollable:
        def __init__(self,pf):
            self.pollFunc = pf

        def poll(self):
            return self.pollFunc()

    def __init__(self,queue):
        self.pollables = []
        self.q = queue

    def addPollable(self,pf):
        # pf is a poll function, returns key,value on None
        # pollables are ordered FiFo
        self.pollables.append(PollMgr.Pollable(pf))

    def pollAll(self):
        for p in self.pollables:
            res = p.poll()
            if res:
                self.q.push(res)



class LCDMgr:
    display = 0
    editing = 1
    eoEdit  = 2
    error   = 3
    states = [display, editing, eoEdit, error]
    cursorOff =-1
    cursorStart = 0
    eoLine = 15
    letters = ['A','B','C','D']
    symobls = ['(',')','|','+',' ']

    def initChars():
        return LCDMgr.letters + LCDMgr.smybols
    
    def __init_(self,stateString):
        self.state = stateString
        self.mode = LCDMgr.display
        self.displayString = stateString

    def setDisplayMode(self):
        self.mode = LCDMgr.display:
        self.cursor = LCDMgr.cursorOff
        self.displayString = stateString
        
    def setEditingMode(self):
        self.mode=LCDMgr.editing
        self.cursor = 0
        self.lettersLeft = LCDMgr.letters
        self.charPtr = 0
        self.sList = self.lettersLeft + LCDMgr.symobls
        self.displayString[self.cursor]= self.slist[charPtr]
        
    def setEOEMode(self):
        self.mode   = LCDMgr.eoEdit
        self.cursor = LCDMgr.cursorOff

    def advanceCursor(self):
        self.cursor +=1
        
    def onLeftButton(self):
        if self.mode == LCDMgr.display:
            # set edit mode
            self.setEditingMode()
        elif self.cursor == LCDMgr.eoLine:
            #end of theline, set eoline mode
            self.setEOEMode()
        elif self.mode == LCDMgr.eoEdit:
            # return to editing mode
            self.setEditingMode()
        elif self.mode =  LCDMgr.error:
            self.setEditingMode()
        else:
            self.advanceCursor()

    def incATCursor(self):
        self.charPtr = self.charPtr+1 % len(self.sList)
        self.displayString[self.cursor]= self.slist[charPtr]
            
    def onRightButton(self):
        if self.mode == LCDMgr.display:
            return
        elif self.mode == LCDMgr.eoEdit:
            self.doConfirm()
        elif self.mode ==LCDMgr.error:
            self.setDisplayMode()
        else:
            self.incATCursor()
            

    
