# tb1.py
#
# trackball quadrature resolution 2x algo


import pyb

blue = 'X18'
yellow = 'X19'
green = 'X20'
white = 'X21'


x1_ = pyb.Pin(blue, pyb.Pin.IN)
x2_ = pyb.Pin(yellow, pyb.Pin.IN)
y1_ = pyb.Pin(green, pyb.Pin.IN)
y2_ = pyb.Pin(white, pyb.Pin.IN)


xCount=0
yCount=0

def x1(unused):
    global xCount
    v=1
    if x1_.value() and  x2_.value():
        v=-1
    elif not x1_.value() and not x2_.value():
        v = -1
    xCount +=v

def y1(unused):
    global yCount
    v = 1
    if y1_.value() and  y2_.value():
        v=-1
    elif not y1_.value() and not y2_.value():
        v = -1
    yCount +=v

pyb.ExtInt(x1_, pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_DOWN, x1)
pyb.ExtInt(y1_, pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_DOWN, y1)

def run():
    global xCount
    global yCount
    xCount = yCount = 0
    lxCount=lyCount=0
    while(True):
        if (lxCount != xCount) or (lyCount != yCount):
            print('(',xCount,',',yCount,')')
            lyCount=yCount
            lxCount=xCount
            
