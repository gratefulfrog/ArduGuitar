# pt.py pin timing tester!

import pyb

""" 
Arduino times
time for a LOW OUTPUT to get pulled HIGH as INPUT
16
time for a High input to go to LOW output
16
time for a LOW output to go to HIGH OUTPUT
16

Pyboard times:
time for LOW output to get PULLED HIGH as input
51
time for a HIGH input to go to LOW output
63
time for a LOW output to go to HIGH output
20
"""


def pt(c='X3'):
    p = pyb.Pin(c,pyb.Pin.OUT_PP,pull=pyb.Pin.PULL_NONE)
    p.value(0)

    print('time for LOW output to get PULLED HIGH as input')
    #print ('\nValue: ' + str(p.value()))    
    u = pyb.micros()
    p.init(pyb.Pin.IN,pull=pyb.Pin.PULL_UP)
    while not p.value():
        None
    t = pyb.micros()-u
    print (t)

    print('time for a HIGH input to go to LOW output')
    #print ('\nValue: ' + str(p.value()))
    u = pyb.micros()
    p = pyb.Pin(c,pyb.Pin.OUT_PP,pull=pyb.Pin.PULL_NONE)
    p.value(0)
    while p.value():
        None
    t = pyb.micros()-u
    print (t)

    print('time for a LOW output to go to HIGH output')
    #print ('\nValue: ' + str(p.value()))
    u = pyb.micros()
    p.value(0)
    while p.value():
        None
    t = pyb.micros()-u
    print (t)

