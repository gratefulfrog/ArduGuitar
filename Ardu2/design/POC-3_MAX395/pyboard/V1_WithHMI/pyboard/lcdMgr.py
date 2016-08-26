#lcdMgr.py

from outils import ljust

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
    letters = ['A','a','B','b','C','c','D','d']  # lower case => inverted
    symbols = ['(','|','+',')']

    def initChars():
        #print('initChars')
        return LCDMgr.letters + LCDMgr.smybols
        
    def setDisplayMode(self):
        #print('setDisplayMode')
        self.lastClick='r'
        self.mode = LCDMgr.display
        self.cursor = LCDMgr.cursorOff
        #self.displayCharList = list(self.stateString.ljust(LCDMgr.lineLength))
        self.displayCharList = list(ljust(self.stateString,LCDMgr.lineLength))
        self.lcd.setLn(0,self.stateString)
        self.lcd.setLn(1,self.stateName)
    
    def loadConf(self):
        print('in lcd mgr loading conf...')
        self.stateString = self.stateDict[self.sKey]
        self.stateName = self.stateDict[self.nKey][:16]
        self.lcd.setLn(0,self.stateString)
        self.lcd.setLn(1,self.stateName)
        self.setDisplayMode()

    def __init__(self,stateDict,sKey,nKey,lcdd, q, validateFunc):
        self.stateDict = stateDict
        self.sKey = sKey
        self.nKey = nKey
        self.lcd = lcdd
        self.validateFunc = validateFunc
        #self.lcdPba = Classes.LCDPBArray(q)
                
    def display(self):
        self.lcd.display()
        #self.lcdPba.display()
    
    def setSList(self):
        #print('setSList')
        self.sList = [' '] + LCDMgr.symbols + self.lettersLeft
        
    def setEditingMode(self, special = None):
        #print('setEditingMode')
        self.mode=LCDMgr.editing
        self.lastClick='r'
        self.cursor = 0
        self.lettersLeft = LCDMgr.letters
        self.charPtr = 0
        self.setSList()
        self.displayCharList = list(' ' * (LCDMgr.lineLength))
        self.updateEditDisplay(special)

    def updateEditDisplay(self, special=None):
        # this is a stub
        msg = ''.join(self.displayCharList)
        self.lcd.setLn(0,msg)
        #print(msg)
        if self.cursor>=0:
            msg = ' '* self.cursor  + '^' + ' Error!' if special else ' '* self.cursor  + '^'
            #print(msg)
            self.lcd.setLn(1,msg)
        
    def setConfirmAbortMode(self):
        #print('setConfirmAbortMode')
        self.mode = LCDMgr.confirmAbortMode
        
    def doConfirm(self):
        #     '0123456789ABCDEF'
        msg = 'Abort - Confirm'
        self.lcd.setLn(1,msg)
        #print(msg)
        self.setConfirmAbortMode()
            
    def setEOEMode(self):
        #print('setEOEMode')
        self.mode   = LCDMgr.eoEdit
        #self.cursor = LCDMgr.cursorOff
        self.doConfirm()
        
    def advanceCursor(self):
        #print('advanceCursor')
        self.cursor +=1
        self.charPtr = 0
        self.lettersLeft = [x for x in self.lettersLeft 
                            if x.upper() not in self.displayCharList[0:self.cursor] and 
                               x.lower() not in self.displayCharList[0:self.cursor]]
        self.setSList()
        self.updateEditDisplay()

    def onLeftButton(self):
        #print('onLeftButton')
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
        #self.updateDisplay()

    def incAtCursor(self):
        #print('incAtCursor')
        self.charPtr = (self.charPtr+1) % len(self.sList)
        self.displayCharList[self.cursor]= self.sList[self.charPtr]
        self.updateEditDisplay()
        

    def confirmed(self):
        if self.validateFunc(self.lcd.getLn(0)): # put a real test here for the display Char list
            self.stateString = ''.join([c for c in self.displayCharList if c != ' '])
            self.lcd.setLn(0,self.stateString)
            self.lcd.setLn(1,self.stateName)
            self.setDisplayMode()
        else:
            self.setEditingMode(True)               
        
    def onRightButton(self):
        #print('onRightButton')
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
        #self.updateDisplay()

            
