# ihmAppTests.py


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
    confirmAbortMode = 4
    #modes = [display, editing, eoEdit, error,confirmAbortMode]
    cursorOff =-1
    cursorStart = 0
    eoLine = 15
    lineLength = 16
    letters = ['A','B','C','D']
    symobls = ['(',')','|','+',' ']

    def initChars():
        print('initChars')
        return LCDMgr.letters + LCDMgr.smybols
        
    def setDisplayMode(self):
        print('setDisplayMode')
        self.lastClick='r'
        self.mode = LCDMgr.display
        self.cursor = LCDMgr.cursorOff
        self.displayCharList = list(self.stateString.ljust(LCDMgr.lineLength))

    def __init__(self,state):
        self.stateString = state
        self.setDisplayMode()
        self.error=False

    def setSList(self):
        print('setSList')
        self.sList = [' '] + self.lettersLeft + LCDMgr.symobls
        
    def setEditingMode(self):
        print('setEditingMode')
        self.mode=LCDMgr.editing
        self.lastClick='r'
        self.cursor = 0
        self.lettersLeft = LCDMgr.letters
        self.charPtr = 0
        self.setSList()
        self.displayCharList = list(' ' * (LCDMgr.lineLength))

    def updateDisplay(self):
        # this is a stub
        print(''.join(self.displayCharList))
        if self.cursor>=0:
            spaces = ' '* self.cursor
            print(spaces + '^')

    def setConfirmAbortMode(self):
        print('setConfirmAbortMode')
        self.mode = LCDMgr.confirmAbortMode
        
    def doConfirm(self):
        # put real confirmation here
        if (not self.error): # put a real test here for the display Char list
            print('Abort: Left - Confirm: Right')
            self.setConfirmAbortMode()
        else:
            print('Error - Rejected!')
            self.setDisplayMode()        
            
    def setEOEMode(self):
        print('setEOEMode')
        self.mode   = LCDMgr.eoEdit
        #self.cursor = LCDMgr.cursorOff
        self.doConfirm()
        
    def advanceCursor(self):
        print('advanceCursor')
        self.cursor +=1
        self.charPtr = 0
        self.lettersLeft = [x for x in self.lettersLeft if x not in self.displayCharList[0:self.cursor]]
        self.setSList()
        
    def onLeftButton(self):
        print('onLeftButton')
        if self.mode == LCDMgr.display:
            # set edit mode
            self.setEditingMode()
        elif self.cursor == LCDMgr.eoLine:
            #end of theline, set eoline mode
            self.setEOEMode()
        elif self.mode == LCDMgr.eoEdit:
            # return to editing mode
            self.setEditingMode()
        elif self.mode ==  LCDMgr.error:
            self.setEditingMode()
        elif self.mode == LCDMgr.confirmAbortMode:
            self.setDisplayMode()
        elif  self.lastClick == 'l':
            self.doConfirm()
        else:
            self.advanceCursor()
        self.lastClick ='l'

    def incAtCursor(self):
        print('incAtCursor')
        self.charPtr = (self.charPtr+1) % len(self.sList)
        self.displayCharList[self.cursor]= self.sList[self.charPtr]

    def confirmed(self):
        ###
        print('confirmed')
        self.stateString = ''.join([c for c in self.displayCharList if c != ' '])
        self.setDisplayMode()
        
    def onRightButton(self):
        print('onRightButton')
        if self.mode == LCDMgr.display:
            return
        elif self.mode == LCDMgr.eoEdit:
            self.doConfirm()
        elif self.mode ==LCDMgr.error:
            self.setDisplayMode()
        elif self.mode == LCDMgr.confirmAbortMode:
            self.confirmed()
        else:
            self.incAtCursor()
        self.lastClick='r'
            

