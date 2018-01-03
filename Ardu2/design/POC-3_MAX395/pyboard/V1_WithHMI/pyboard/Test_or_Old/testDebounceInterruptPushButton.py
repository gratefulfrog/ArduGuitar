class HWDebouncedPushButton(EnQueueable):
    """
    an interrupt generating pushbutton, using the q to manage actions
    avoiding repeated pushes using a lock and a time delay
    """
    def __init__(self,pinName,q):
        EnQueueable.__init__(self,EnQueueable.PB,q)
        self.extInt = ExtInt(pinName, ExtInt.IRQ_FALLING, Pin.PULL_UP, self.callback)
        self.id = State.pinNameDict[pinName][1]
        self.debugPinName = pinName
        self.locked = False
        self.lastCallBackTime = millis()
        self.debounceDelay = const(100) #millis
        
    def callback(self,unusedLine):
        if self.locked:
            return
        self.locked = True
        now = const(millis())
        if now-self.lastCallBackTime > self.debounceDelay:
            self.lastCallBackTime = now
            self.push(self.id)
        self.locked = False

    def __repr__(self):
        return 'HWDebouncedPushButton:\n  ID:\t%d\n  %s'%(self.id,repr(self.extInt))
