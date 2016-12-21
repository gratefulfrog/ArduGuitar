# tbA.py
#
# trackball quadrature resolution 1,2x,4x algos

import pyb

"""
blue   = 'X18'
yellow = 'X19'
green  = 'X20'
white  = 'X21'
"""
blue   = 'Y10'
yellow = 'Y8'
green  = 'Y9'
white  = 'Y7'


x1_ = pyb.Pin(blue,   pyb.Pin.IN)
x2_ = pyb.Pin(yellow, pyb.Pin.IN)
y1_ = pyb.Pin(green,  pyb.Pin.IN)
y2_ = pyb.Pin(white,  pyb.Pin.IN)

xCount=0
yCount=0

def x11(unused):
    global xCount
    v = 1
    if x2_.value():
        v=-1
    xCount +=v

def y11(unused):
    global yCount
    v = 1
    if y2_.value():
        v=-1
    yCount +=v

def x12(unused):
    global xCount
    v=1
    if x1_.value() and  x2_.value():
        v=-1
    elif not x1_.value() and not x2_.value():
        v = -1
    xCount +=v

def y12(unused):
    global yCount
    v = 1
    if y1_.value() and  y2_.value():
        v=-1
    elif not y1_.value() and not y2_.value():
        v = -1
    yCount +=v

def x14(unused):
    global xCount
    v=1
    if x1_.value() and  x2_.value():
        v=-1
    elif not x1_.value() and not x2_.value():
        v = -1
    xCount +=v

def x24(unused):
    global xCount
    v=-1
    if x1_.value() and  x2_.value():
        v=1
    elif not x1_.value() and not x2_.value():
        v=1
    xCount +=v
    
def y14(unused):
    global yCount
    v = 1
    if y1_.value() and  y2_.value():
        v=-1
    elif not y1_.value() and not y2_.value():
        v = -1
    yCount +=v

def y24(unused):
    global yCount
    v=-1
    if y1_.value() and  y2_.value():
        v=1
    elif not y1_.value() and not y2_.value():
        v=1
    yCount +=v

def getAlgo(xy,ind,res):
    """ returns the handler function given
    xy = 'x' or 'y'
    ind = 1 or for the quandrature sq wave
    res= 1,2,4 for resolutions
    """
    print (xy + str(ind) + str(res))
    return eval(xy + str(ind) + str(res))

def setInts(resolution):
    global intersSet
    intersSet = True
    rf = pyb.ExtInt.IRQ_RISING_FALLING
    if resolution == 1:
        rf = pyb.ExtInt.IRQ_RISING
    pyb.ExtInt(x1_, rf, pyb.Pin.PULL_DOWN, getAlgo('x',1,resolution))
    pyb.ExtInt(y1_, rf, pyb.Pin.PULL_DOWN, getAlgo('y',1,resolution))
    if resolution == 4:
        pyb.ExtInt(x2_, rf, pyb.Pin.PULL_DOWN, getAlgo('x',2,resolution))
        pyb.ExtInt(y2_, rf, pyb.Pin.PULL_DOWN, getAlgo('y',2,resolution))
    
intersSet = False

def run(resolution=1):
    global xCount
    global yCount
    if not intersSet:
        setInts(resolution)
    xCount = yCount = 0
    lxCount=lyCount=0
    printCount=0
    while(True):
        if (lxCount != xCount) or (lyCount != yCount):
            printCount +=1
            print('(',xCount,',',yCount,') :', printCount)
            lyCount=yCount
            lxCount=xCount
