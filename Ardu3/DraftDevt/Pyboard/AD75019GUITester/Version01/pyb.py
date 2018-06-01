#!/usr/local/bin/python3.4
# pyb.py for Off-pyboard testing
# here we find pyboard simulation classes for Off-board testing

#import time

class LED:
    def __init__(self,name):
        self.name = name
        self.state = 0
        
    def on(self):
        self.state = 1
    def off(self):
        self.state=0
"""
LED = [led(1),
       led(2),
       led(3),
       led(4)]
"""
def delay(dela):
    d=dela*10000
    while(d):
        d -=1

def udelay(dela):
    delay(dela)
    
count = 0
def millis():
    global count
    count+=1
    return count
       
class SPI():
    """simulation SPI class provides basic SPI simulation
    - definitions
    - instance creation
    - send operation
    - repr
    usage:
    >>> from pyb import SPI
    >>> s = SPI(1,SPI.MASTER)
    >>> print(s)
    SPI:
	BoardSide:	1
	MasterOrSlave:	Master
    >>> s.send(0)
    send:	0b0
    >>> s.send(1)
    send:	0b1
    >>> s.send(2)
    send:	0b10
    """
    MASTER = 'Master'
    SLAVE = 'Slave'
    LSB   = 'LSB'
    MSB   = 'MSB'

    def __init__(self,side,MasterOrSlave,prescaler=256,
                 polarity=0,phase=0,bits=8,firstbit=MSB,ti=0,crc=None):
        self.side      = side
        self.MoS       = MasterOrSlave
        self.prescaler = prescaler
        self.polarity  = polarity

    def send(self,bits):
        #print(bits)
        print(''.join('{:02x}'.format(x) for x in bits))
        #for b in bits:
        #    print("Simulated: send:\t{0:#b}".format(b))
        
    def __repr__(self):
        return 'SPI:' + \
            '\n\tBoardSide:\t' + str(self.side) + \
            '\n\tMasterOrSlave:\t' + str(self.MoS) +\
            '\n\tprescaler:\t' + str(self.prescaler) +\
            '\n\tpolarity:\t' + str(self.polarity)

class Pin():
    """simulation Pin class provides basic pin simulation
    - definitions
    - instance creation
    - high() low()  operations
    - repr
    usage:
    >>> from pyb import Pin
    >>> p = Pin('X5',Pin.OUT_PP)
    >>> print(p)
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	0
    >>> p.high()
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	1
	set: HIGH
    >>> p.low()
    Pin:
	LatchPin:	X5
	PinOut:	OUT_PP
	Value:	0
	set: LOW
    """
    OUT_PP = 'OUT_PP'
    IN = 'IN'
    PULL_DOWN = 'PULL_DOWN'
    PULL_UP = 'PULL_UP'
    

    def __init__(self, latch, mode=None, pull = None):
        self.latchPin = latch
        self.pinOut = mode
        self.puLL = pull
        self.val = 0

    def init(self,*ags):
        pass

    def high(self):
        self.val = 1
        #print(str(self) + '\n\tset: HIGH')

    def low(self):
        self.val = 0
        #print (str(self) + '\n\tset: LOW')

    def value(self,*args):
        return self.val

    def __repr__(self):
        return 'Pin:' + \
            '\n\tLatchPin:\t' + str(self.latchPin) + \
            '\n\tPinOut:\t' + str(self.pinOut) + \
            '\n\tValue:\t' + str(self.val) 

class pwmAble:
    def __inti__(self):
        self.perc = 0

    def pulse_width_percent(self,percent):
                self.perc = percent

    def __repr__(self):
        return 'pwmAble: ' +'\n\t' + str(self.perc)
    
class Timer:
    PWM  = 0
    def __init__(self,pp,freq):
        self.pin = pp
        self.freq = freq

    def channel (self,ch,kind,pin):
        r = pwmAble()
        return r

    def __repr__(self):
        return 'A Timer!'

class ADC:
    def __init__(self,pp):
        self.pin = pp

    def read(self):
        print('input value for ADC on pin ' + self.pin +': ' ,end='')
        return int(input())
        
    def __repr__(self):
        return 'An ADC on pin: ' + self.pin

class Accel():
    def __init__(self):
        self.what = 'Accel'
    def __repr__(self):
        return 'Accel'

    
class ExtInt:
    IRQ_FALLING = 'IRQ_FALLING'
    IRQ_RISING = 'IRQ_RISING'

    def __init__(self,pinName,irq,pull, callback):
        self.pinName = pinName
        self.irq = irq
        self.pull = pull
        self.callback = callback
        
    def __repr__(self):
        return 'An ExtInt:\n  Pin:\t%s\n  Irq:\t%s\n  Pull:\t%s\n'% (self.pinName,self.irq,self.pull)
    

class USB_VCP:
    def __init__(self):
        self.something = 0
    def any(self):
        return True
    def write(self, arg):
        print('Wrote to usb : ' + arg)
    def read(self):
        return '|'
    
