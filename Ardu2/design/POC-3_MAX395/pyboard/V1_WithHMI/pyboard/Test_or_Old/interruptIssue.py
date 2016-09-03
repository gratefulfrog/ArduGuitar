#interruptIssue.py

# there may be an issue of interrupts being sent from pins not configured?

"""
Pin Y1 is on interrupt line 6
Pin X9 is also on line 6

If I configure a interrupt on X9, then set Y1, will that set off the interrupt?

The answer is NO IT WILL NOT!!! Thankfully!

"""

from pyb import ExtInt, Pin, delay

class TC:
    def callback(self,unusedLine):
        print('Callback from pin:\t',self.iPin)

    def __init__(self,ipin='X9',vpin='Y1'):
        self.extInt = ExtInt(ipin, ExtInt.IRQ_FALLING, Pin.PULL_UP, self.callback)
        self.iPin = ipin
        self.vPin = vpin
        self.vPP = Pin(vpin,mode=Pin.OUT_PP, pull=Pin.PULL_UP)
        
    def test(self):
        while True:
            print('setting: ' + self.vPin + ' LOW')
            self.vPP.low()
            delay(500)
            print('setting: ' + self.vPin + ' HIGH')
            self.vPP.high()
            delay(500)
            
        

