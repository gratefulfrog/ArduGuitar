# PS2.py
# a class to support PS2 protocol objects, like a PS/2 trackball

import pyb

class PS2:
    def __init__(self, clockPinName,dataPinName):
        self.clockPin = pyb.Pin(clockPinName, pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)
        self.dataPin  = pyb.Pin(dataPinName,pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)
        self.clockGoHi()
        self.dataGoHi()
        
    def clockGoHi(self): #goHi
        """ set the clock to INPUT mode with PULL_UP
        """
        self.clockPin.init(pyb.Pin.IN,pull=pyb.Pin.PULL_UP)

    def clockGoLo(self):  #goLo
        """ set the clock pin to OUTPUT mode, then set it at LOW
        """
        self.clockPin.init(pyb.Pin.OUT_PP,pull=pyb.Pin.PULL_NONE)
        self.clockPin.value(0)

    def dataGoHi(self): # goHi
        """ set the data to INPUT mode with PULL_UP
        """
        self.dataPin.init(pyb.Pin.IN,pull=pyb.Pin.PULL_UP)

    def dataGoLo(self): #goLo
        """ set the data pin to OUTPUT mode, then set it at LOW
        """
        self.dataPin.init(pyb.Pin.OUT_PP,pull=pyb.Pin.PULL_NONE)  # NONE
        self.dataPin.value(0)

    """
    unused for the moment
    def clockOutputHi(self.p): #new from me
        # set the clock pin to OUTPUT mode, then set it at LOW
        self.clockPin.init(pyb.Pin.OUT_PP,pull=pyb.Pin.PULL_NONE)
        self.clockPin.value(1)

    def dataOutputHi(self): # new from me
        # should this be OUTPUT mode PP? with value(1)??
        self.dataPin.init(pyb.Pin.OUT_PP,pull=pyb.Pin.PULL_NONE)
        self.dataPin.value(1)
    """

        
    def write(self,data):
        """ data is one byte to be written to the ps/2 device
        it is taken as a number in the argument...
        """
        def waitClockLoHi():
            print ('in clockloHi waitng for a HI...')
            while (not self.clockPin.value()):
                None
            print('Clock is HI')
            while (self.clockPin.value()):
                None
            print('Clock is LOW')
        print('in write, data is: ', str(data))
        self.dataGoHi()
        self.clockGoHi()
        pyb.udelay(300)
        self.clockGoLo()
        pyb.udelay(300)
        self.dataGoLo()
        pyb.udelay(10)
        self.clockGoHi()  # this is the start bit??? how can that be?
        #self.clockGoLo()  # ???? try ...

        print('in write, about to wait for clock to go low...')
        # wait for device to take control of clock
        while (self.clockPin.value()):
            None
        print('in write, about to write..')
        # now we can send data!
        parityBit = 0
        
        for i in range(8):  # iterate over bits in byte, Low order bit first
            print ('in the write bit loop..')
            val = data & 0x01 # then it's a one, 
            if (val):
                self.dataGoHi()
            else:
                self.dataGoLo()
            pyb.udelay(20)
            waitClockLoHi()
            #parity bit
            parityBit ^= val
            # shift to next data bit
            data = (data >> 1)

        # now send parity bit
        if (parityBit):
            self.dataGoHi()
        else:
            self.dataGoLo()
        print('wrote parity bit, about to wait on clock low/high')
        waitClockLoHi()
            
        # stop bit
        self.dataGoHi()
        pyb.udelay(50)
        # wait for clock to go lo?
        while (self.clockPin.value()):
            None
        print ('Clock is HI, now waiting on the big OR')
        # mode switch???
        while( (not self.clockPin.value()) or
               (not self.dataPin.value())):
            None

        # block incoming data?
        self.clockGoLo()

    def read(self):
        def waitClockHiLo():
            while (self.clockPin.value()):
                None
            while (not self.clockPin.value()):
                None
        
        data = 0
        bit = 0x1

        self.clockGoHi()
        self.dataGoHi()
        pyb.udelay(50)
        while (self.clockPin.value()):
            None
        print('in read, Clock is low..')
        pyb.udelay(5)  # why is this?
        while (not self.clockPin.value()):
            None  # this eats the start bit???
        print('in read, Clock is now HI...')
        # Now read in a byte
        for i in range(8):
            while (self.clockPin.value()):
                None
                print ('in read, waiting for clock to go low for the data...')
                if (self.dataPin.value()):
                    data |=bit
                print ('in read, read a bit, waiting for clock to go hi...')
                while (not self.clockPin.value()):
                    None
                print ('in read, read a bit, clock is hi...')
                bit = (bit << 1)
        # eat parity bit
        waitClockHiLo()
        # eat stop bit
        waitClockHiLo()

        # hold incoming data
        self.clockGoLo()

        return data
