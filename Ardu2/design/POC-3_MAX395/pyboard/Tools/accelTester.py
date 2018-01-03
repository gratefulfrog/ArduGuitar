#accelTester.py
# examination of interactions between the pyb.Accel instance and ExtInts on pins X9 and X10!

"""
Results:
#1. if we instantiate the Accel before creating the interrupts (after Ctrl-D soft reboot):
>>> from accelTester import *
>>> (i,a) = accFirst()  # instantiate the Accel, then the ExtInts!
>>> a
<Accel>
>>> a.x() # readings are always 4, for all axes
4
>>> a.y()
4
>>> a.z()
4
>>> 
#2. if we  create the ExtInts, then instatiate the Accel (after Ctrl-D soft reboot):
>>> from accelTester import *
>>> (i,a)=intsFirst() # loads of interrupts are fired!
7
6
6
7
6
7
7
6
6
7
6
7
6
7
7
6
7
7
>>> a.x() # again, interrrupts are fired, but at the end, the result is returned!
7
6
6
7
6
7
6
7
6
6
7
6
6
7
6
-19
>>> a.y() # again, interrrupts are fired, but at the end, the result is returned!
7
6
6
7
6
7
6
7
7
6
6
7
6
6
7
6
-3
>>> a.z() # again, interrrupts are fired, but at the end, the result is returned!
7
6
6
7
6
7
6
7
7
6
6
7
6
6
7
6
-7
>>>

"""



from pyb import ExtInt,Pin,Accel,delay

pinLineVec = (('X1',0),
              ('X2',1),
              ('X3',2),
              ('X4',3),
              ('X5',4),
              ('X6',5),
              ('X9',6),  # X9 causes the issue, X7 does not
              ('X10',7), # X10 causes the issue, X8 does not
              ('Y3',8),
              ('Y4',9),
              ('Y9',10),
              ('Y10',11),
              ('Y5',12),
              ('Y6',13),
              ('Y7',14),
              ('Y8',15))


def callback(line):
    print(line)

def intsFirst():
    ints = [ExtInt(p[0],ExtInt.IRQ_FALLING,Pin.PULL_UP,callback) for p in pinLineVec]
    a=Accel()
    delay(2000)
    return (ints,a)

def accFirst():
    a=Accel()
    ints = [ExtInt(p[0],ExtInt.IRQ_FALLING,Pin.PULL_UP,callback) for p in pinLineVec]
    delay(2000)
    return (ints,a)

              
