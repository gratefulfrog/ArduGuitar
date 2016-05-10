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
    print('Horizontal Selector Func called on pos:\t' + str(p))

def vSelect(p):
    print('Vertical Selector Func called on pos:\t' + str(p))



"""
    config def:
    {(h,v): {'S': 'A|B|C', 'M' : (v,t), 'A' : {(v,t), 'B' : {v,t), 'C' : {v,t), 'D' : {v,t), 'R' : tr},
"""
configDict = {(0,0) : {'S' : 'A+B'},
              (1,0) : {'S' : 'A|B'},
              (2,0) : {'S' : 'A+B+C+D'},
              (3,0) : {'S' : 'C|D'},
              (4,0) : {'S' : 'C+D'}}

