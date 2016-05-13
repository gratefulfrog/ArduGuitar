# stub functions
import random


#utility active sleep function 
def mSleep(msecs):
    now = millis()
    while millis()-now < msecs:
        None

def genIDs(maxi):
    for i in range(maxi):
        (yield i)
IDs = genIDs(25)

# pushbutton funcs
def r():
    print('RED')
def y():
    print('YELLOW')
def g(): 
    print('GREEN')
def b():
    print('BLUE')

lpbFuncs = [r,y,g,b]

def validateConf(conf):
    #if random.randint(0,1):
        print(conf + ' : OK!')
        return True
    #else:
    #    print(conf + ' : NOT OK!')
    #    return False

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
    return ((lambda val: pWorkaround(name + ':\tVol:\t' + str(val)) if volActive else lambda un: None), 
            lambda val: pWorkaround(name + (':\tTone:\t' if volActive else ':\tToneRange:\t') + str(val)))
        
def pWorkaround(v):
    print(v)

"""
    config def:
    {(h,v): {'S': 'A|B|C', 'M' : (v,t), 'A' : {(v,t), 'B' : {v,t), 'C' : {v,t), 'D' : {v,t), 'R' : tr},
"""
configDict = {(0,0) : {'S' : '(+AB)'},
              (1,0) : {'S' : '(|AB)'},
              (2,0) : {'S' : '(+ABCD)'},
              (3,0) : {'S' : '(|CD)'},
              (4,0) : {'S' : '(+CD)'}}