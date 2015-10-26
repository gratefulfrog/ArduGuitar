#is2q.py  2 pin version

"""
wiring: 
- pin X1 is INPUT, PULL NONE, connected to external 1K pullup to 3.3V
- pin X2 is OUT_OD,PULL NONE connected to X1!
results:
PYB: sync filesystems
PYB: soft reboot
MicroPython v1.4.6-89-g556c8a9 on 2015-10-15; PYBv1.0 with STM32F405RG
Type "help()" for more information.
>>> import is2t
>>> is2t.c
Pin(Pin.cpu.A0, mode=Pin.OUT_OD)
>>> is2t.c.value()
0
>>> is2t.c.value(1)
>>> is2t.c.value()
1
>>> #connect x1 to gnd
>>> is2t.c.value()
0
>>> # this is good
>>> # now enable the interrupt
>>> is2t.setInterrupt(is2t.c)
>>> is2t.c
Pin(Pin.cpu.A0, mode=Pin.AF_OD, af=0)
>>> is2t.c.value()
0
>>> # remove gnd from pin
>>> ok
ok
ok
ok

>>> is2t.c.value()
1
>>> # this is ok, now set pin to 0
>>> is2t.c.value(0)
>>> # read pin
>>> is2t.c.value()
1
>>> # this is wrong! pin should be 0!
>>> # connect to GND and read
>>> ok

>>> is2t.c.value()
0
>>> # ok
>>> #check pin config
>>> is2t.c
Pin(Pin.cpu.A0, mode=Pin.AF_OD, af=0)
>>> # from this point, the only way to get 0 on the pin is to connect it to GND, setting value has no effect
""" 


from pyb import Pin,ExtInt

def callback(line):
    print('ok')

mdO = Pin.OUT_OD
mdI = Pin.IN
pL = Pin.PULL_NONE
iM = ExtInt.IRQ_FALLING
   
ci = Pin('X1',mdI,pL)
co = Pin('X2',mdO,pL)

def setInterrupt(p):
    ExtInt(p, iM, pL, callback)


di = Pin('X3',mdI,pL)
do = Pin('X4',mdO,pL)

