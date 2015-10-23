# ps2b.py
# version using things learned on the forum thread:
# http://forum.micropython.org/viewtopic.php?f=2&t=990

import pyb,stm
from pyb import Pin


# version not using hard wired tricks!
class ps2:
    
    def __init__(self, clockPinName, dataPinName):
        self.clock = Pin(clockPinName, Pin.OUT_OD, Pin.PULL_UP)
        self.data  = Pin(dataPinName,  Pin.OUT_OD, Pin.PULL_UP)
        self.ckv = self.clock.value
        self.dav = self.data.value
        
    def reset(self):
        self.send(0xFF)
        res = (self.read(), self.read(),self.read())
        self.inhibitedState()
        return res

    def setRemote(self):
        self.send(0xF0)
        res  = (self.read(),)
        self.inhibitedState()
        return res

    def getData(self):
        self.send(0xEB)
        res = (self.read(),self.read(),self.read(),self.read())
        self.inhibitedState()
        return res

    @micropython.viper
    def clockRelease(self, bits:int=1):
        self.ckv(bits)

    @micropython.viper
    def clockLow(self, bits:int=0):
        self.dav(bits)

    @micropython.viper
    def dataRelease(self, bits:int=1):
        self.dav(bits)

    @micropython.viper
    def datakLow(self, bits:int=0):
        self.dav(bits)
    
    def idleState(self): 
        self.dataRelease()
        self.clockRelease()

    def inhibitedState(self): 
        self.dataRelease()
        self.clockLow()
    
    def request2SendState(self):
        self.inhibitedState()
        pyb.udelay(150)
        self.dataLow()
        self.clockRlease()

    @micropython.viper
    def send(self, bits:int):
        parity = 1
        self.request2SendState()
        for i in range(8):
            while self.ckv():
                pass
            bit = (bits >> i) & 1
            parity = ~parity if bit else parity
            self.dav(bit)
            while not self.ckv():
                pass
        while self.ckv():
            pass
        self.dav(parity)
        while not self.ckv():
            pass
        while self.ckv():
            pass
        self.dav(1)  # stop bit
        while not self.ckv():
            pass

    @micropython.viper
    def read(self):
        bits:int = 0
        parity = 1
        # let the ZERO start bit go by
        while not self.ckv():
            pass
        for i in range(8):
            # wait for low clock
            while self.ckv():
                pass
            # read a bit
            bit = self.dav()
            bits |= (bit << i)
            parity = ~parity if bit else parity
            while not self.ckv():
                pass
        # now we have read bits and computed parity
        # read the parity bit:
        while self.ckv():
            pass
        parityBit = self.dav()
        while not self.ckv():
            pass
        while self.ckv():
            pass
        # let stop bit go by
        while not self.ckv():
            pass
        return (parity=parityBit, bits)
        
            
