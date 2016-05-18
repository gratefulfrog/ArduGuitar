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
    print('RED')  #id = 0
    print(str(currentDict))
def y():
    print('YELLOW')  #id = 1
def g(): 
    print('GREEN')  #id = 2  Tremolo!
    currentDict['TREM'] = 0 if currentDict['TREM'] else 1
    
def b():
    print('BLUE')  #id = 3 vibrato !
    currentDict['VIB'] = 0 if currentDict['VIB'] else 1
    

lpbFuncs = [r,y,g,b]

def validateConf(conf):
    #if random.randint(0,1):
        print(conf + ' : OK!')
        currentDict['S'] =  conf
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
    return ((lambda val: pWorkaround(name + ':\tVol:\t' + str(val)) if volActive else lambda unused: None), 
             lambda val: pWorkaround(name + (':\tTone:\t' if volActive else ':\tToneRange:\t') + str(val)))
        
def pWorkaround(v):
    print(v)


def pb(ind, lcdmgrInstance):
    if (ind <5):
        print (ind)
    else:
        print(ind)


def set(attribute, owner, value):
    print('SET:\n\tAttribute:\t' + str(attribute) +'\n\tOwner:\t' + str(owner) +'\n\tValue:\t' + hex(value))

configDict = {(0,0) : {'S' : '(+AB)'},
              (1,0) : {'S' : '(|AB)'},
              (2,0) : {'S' : '(+ABCD)'},
              (3,0) : {'S' : '(|CD)'},
              (4,0) : {'S' : '(+CD)'}}

currentDict = {'M' : [0,0],   # vol, tone
               'A' : [0,0], 
               'B' : [0,0], 
               'C' : [0,0], 
               'D' : [0,0], 
               'TR' : [None,0],  # range on [0,5]
               'S' : '(|(+AB)(+CD))',
               'TREM' : 0,
               'VIB' : 0}


