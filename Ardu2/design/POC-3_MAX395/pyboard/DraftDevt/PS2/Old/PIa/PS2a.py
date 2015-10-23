# PS2a.py, again...

import pyb

class PS2:
    def gohi(p):
        p.init(mode=pyb.Pin.IN,pull=pyb.Pin.PULL_UP);
    def golo(p):
        p.init(mode=pyb.Pin.OUT_OD,pull=pyb.Pin.PULL_NONE)
        p.value(0)

    def __init__(self,clockName,dataName):
        self.clock = pyb.Pin(clockName,mode=pyb.Pin.IN,pull=pyb.Pin.PULL_UP);
        self.data = pyb.Pin(dataName,mode=pyb.Pin.IN,pull=pyb.Pin.PULL_UP);
        PS2.gohi(self.clock)
        PS2.gohi(self.data)

    def write(self,bits):
        data = bits & 255
        parity = 1
        
        PS2.gohi(self.data)
        PS2.gohi(self.clock)
        pyb.udelay(300)
        PS2.golo(self.clock)
        pyb.udelay(120)
        PS2.golo(self.data)
        #pyb.udelay(10)
        PS2.gohi(self.clock)       # start bit = 0

        # now wait for device to take control of clock!
        #us = pyb.micros()
        while self.clock.value():
            None
        #print('clock high for %d us'% (pyb.micros()-us))
        for i in range(8):
            # clock is now low, we can send a bit!
            #pyb.udelay(5)  # wait for the falling edge to pass
            if data & 0x01:
                PS2.gohi(self.data) # or set value to 1 ??
                #self.data.value(1)
            else:
                PS2.golo(self.data)
            # updata parity
            parity = parity ^ (data & 0x01)
            data = (data >> 1)
            # wait a clock cycle before next iteration
            #us = pyb.micros()
            #while not self.clock.value():
            #    None
            #print('clock low for %d us'% (pyb.micros()-us))
            #us = pyb.micros()
            while self.clock.value():
                pass
            #print('clock high for %d us'% (pyb.micros()-us))
        #now send the parity bit
        if parity:
            PS2.gohi(self.data) # or set value to 1 ??
            #self.data.value(1)
        else:
            PS2.golo(self.data)
                
        # wait a clock cycle before stop bit
        while not self.clock.value():
            None
        while self.clock.value():
            None

        # stop bit
        PS2.gohi(self.data)
        #self.data.value(1)
        #pyb.udelay(50)
        while self.data:
            pass
        while self.clock.value():
            None
        # mode switch
        while (not self.clock.value()) or (not self.data.value()):
            pass
        #hold up incoming data
        PS2.golo(self.clock)

    def read(self):
        # ignores parity

        data = 0  # will contain result of reading
        bit = 1
        # start clock
        PS2.gohi(self.clock)
        PS2.gohi(self.data)
        pyb.udelay(50)
        
        while self.clock.value():
            pass
        # read on low bit, but start bit is always zero, so skip it
        while not self.clock.value():
            pass
        for i in range(8):
            # now we are set up to read the payload bits
            # wait for clock to be low, then read a bit
            while self.clock.value():
                pass
            #pyb.udelay(10)  # wait for the falling edge to pass
            if self.data.value():
                data |= bit
                #print('incoming HIGH bit')
            # shift data,
            bit = (bit << 1)
            # wait for clock to be high
            while not self.clock.value():
                pass

        # eat and ignore parity bit
        while self.clock.value():
            None
        while not self.clock.value():
            None
        # eat and ignore stop bit
        while self.clock.value():
            None
        while not self.clock.value():
            None

        # hold incoming data
        PS2.golo(self.clock)

        return data
    
