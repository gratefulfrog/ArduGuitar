#!/usr/local/bin/python3.4
# server_01.py

"""
This reproduces the Arduino functionality from Arduino_v01.ino
this requires updated boot.py
----
# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import pyb
pyb.main('main.py') # main script to run after this one
pyb.usb_mode('CDC+MSC') # act as a serial and a storage device
#pyb.usb_mode('CDC+HID') # act as a serial device and a mouse
-----

"""

import pyb,spiMgr

SPI_ON_X = True

""" unused
def val2String(val,strLen):
    res = ''
    for i in range(strLen):
        v = (val & (1<<(strLen-1-i)))
        res+= ('1' if v else '0')
    return res
"""

def charFromSer(ser):
    return chr(ser.read(1)[0])

class App:
    def __init__(self,SPI_ON_X):
        self.spi = spiMgr.ad75019SPIMgr(SPI_ON_X,
                                        ('X5' if SPI_ON_X  else 'Y5'))

        #self.baudrate      = 115200
        self.loopPauseTime = 200 # millisecs

        self.contactChar = '|' #bytes('|' ,'utf8')
        self.pollChar    = 'p' #bytes('p' ,'utf8')
        self.executeChar = 'x' #bytes('x' ,'utf8')

        # states
        self.uninitState   = 1
        self.contactState  = 2
        self.pollState     = 3
        self.executeState  = 4

        # unused self.bitVecNBBytes = 32
        self.nbPins        = 16
        self.nbBits        = 256
        self.execIncomingLength = self.nbPins + self.nbBits
          
        # incoming message processing
        self.incomingBits = '0' * self.nbBits

        self.replyReady = False
    
        self.serial=pyb.USB_VCP() 

        self.setState(self.uninitState)
        self.establishContact()
        self.setState(self.contactState)
        self.loop()

    def setState(self,state):
        leds= range(1,5)
        [pyb.LED(i).off() for i in leds]
        self.currentState = state
        pyb.LED(state).on()
        
    def establishContact(self):
        found = False
        while not found:
            while not self.serial.any():
                self.serial.write(self.contactChar)
                pyb.delay(self.loopPauseTime)
            read = charFromSer(self.serial)
            if read == self.contactChar:
                found = True

    def loop(self):
        while True:
            if self.serial.any():
                self.processIncoming()
            if self.replyReady:
                self.sendReply()
                self.replyReady = False
    
    def processIncoming(self):
        incomingChar = charFromSer(self.serial)
        if (self.currentState == self.contactState or
            self.currentState == self.pollState):
            if incomingChar == self.pollChar:
                self.setState(self.pollState)
                pyb.delay(100)  # only to be able to see the led flash! remove in operational code
                self.replyReady = True
                self.setState(self.contactState)
            elif incomingChar == self.executeChar:
                self.incomingBits = ''
                self.setState(self.executeState)
        elif self.currentState == self.executeState:
            self.incomingBits += incomingChar
            if len(self.incomingBits) == self.execIncomingLength:
                #self.execIncoming()
                self.replyReady = True
                self.setState(self.contactState)

    def execIncoming(self):
        self.setConnections()

    def setConnections(self):
        self.spi.sendString(self.incomingBits)

    def sendReply(self):
        reply= '0' * self.nbPins 
        reply += self.incomingBits
        self.serial.write(reply)
        

