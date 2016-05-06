# stub functions
import random


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
    if random.randint(0,1):
        print(conf + ' : OK!')
        return True
    else:
        print(conf + ' : NOT OK!')
        return False

def hSelect(p):
    print('Horizontal Sector: ' + str(p))

def vSelect(p):
    print('Vertical Sector: ' + str(p))


"""
    config def:
    {(h,v): {'S': 'A|B|C', 'M' : (v,t), 'A' : {v,t), 'B' : {v,t), 'C' : {v,t), 'D' : {v,t), 'R' : tr},
"""