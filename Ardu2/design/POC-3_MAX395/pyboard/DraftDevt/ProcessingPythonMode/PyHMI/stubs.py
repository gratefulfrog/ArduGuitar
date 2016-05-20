# stub functions
import random


#utility active sleep function 
def mSleep(msecs):
    now = millis()
    while millis()-now < msecs:
        None

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
    print(conf.strip() + ' : OK!')
    currentDict['S'] =  conf.strip()
    return True

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


# this is worng and needs to be fixed!
configDict = {(0,0) : {'S' : '(+AB)'},
              (1,0) : {'S' : '(|AB)'},
              (2,0) : {'S' : '(+ABCD)'},
              (3,0) : {'S' : '(|CD)'},
              (4,0) : {'S' : '(+CD)'}}

currentDict = {'Name': 'Full Blast',
               'M' : [5,5],   # vol, tone
               'A' : [5,5], 
               'B' : [5,5], 
               'C' : [5,5], 
               'D' : [5,5], 
               'TR' : [None,5],  # range on [0,5]
               'S' : '(+ABCD)',
               'TREM' : 0,
               'VIB' : 0}

"""
def genIDs(maxi):
    for i in range(maxi):
        (yield i)
IDs = genIDs(25)
"""