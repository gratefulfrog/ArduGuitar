# stub functions


# pushbutton funcs
def r():
    print('RED')  #id = 0
def y():
    print('YELLOW')  #id = 1
    print('Saving presets to disk...')
def g(): 
    print('GREEN')  #id = 2  Tremolo!
def b():
    print('BLUE')  #id = 3 vibrato !
    
lpbFuncs = [r,y,g,b]

"""
#utility active sleep function 
def mSleep(msecs):
    now = millis()
    while millis()-now < msecs:
        None

def hSelect(p):
    print('Horizontal Selector Func called on pos:\t' + str(p))

def vSelect(p):
    print('Vertical Selector Func called on pos:\t' + str(p))

def hTBFunc(val):
    print('Horizontal Trackball Func called on dX:\t' + str(val))

def vTBFunc(val):
    print('Vertical Trackball Func called on dX:\t' + str(val))

def makeVTFunc(name, volActive=True):
    # second arg to handle unused vol part of ToneRange SpiltPot
    return ((lambda val: pWorkaround(name + ':\tVol:\t' + str(val)) if volActive else lambda unused: None), 
             lambda val: pWorkaround(name + (':\tTone:\t' if volActive else ':\tToneRange:\t') + str(val)))
        
def pWorkaround(v):
    print(v)

def set(attribute, owner, value):
    print('SET:\n\tAttribute:\t' + str(attribute) +'\n\tOwner:\t' + str(owner) +'\n\tValue:\t' + hex(value))
    

def validateConf(conf):
    print(conf + ':\tOK!')
    return True
"""