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
"""
native times (slightly lower...)
time for LOW output to get PULLED HIGH as input
45
time for a HIGH input to go to LOW output
55
time for a LOW output to go to HIGH output
15
"""

""" result 5 """
def t(c='X8'):
    print ('NO NATIVE: how many pin values can we do in 100 us')
    p = pyb.Pin(c,pyb.Pin.OUT_PP,pull=pyb.Pin.PULL_NONE)
    bit = 1
    p.value(bit)
    count = 0
    u = pyb.micros()
    while pyb.elapsed_micros(u) < 100:
        bit ^= 1
        p.value(bit)
        count+=1
    print(count)

""" result 6 """
@micropython.native 
def tn(c='X8'):
    print ('NATIVE: how many pin values can we do in 100 us')
    p = pyb.Pin(c,pyb.Pin.OUT_PP,pull=pyb.Pin.PULL_NONE)
    bit = 1
    p.value(bit)
    count = 0
    u = pyb.micros()
    while pyb.elapsed_micros(u) < 100:
        bit ^= 1
        p.value(bit)
        count+=1
    print(count)
    
""" result 7 """           
def i():
    print ('how many instructions can we do in 100 us')
    count = 0
    u = pyb.micros()
    while pyb.elapsed_micros(u) < 100:
        count+=1
    print(count)

""" result 9 """           
@micropython.native 
def ni():
    print ('Native: how many instructions can we do in 100 us')
    count = 0
    u = pyb.micros()
    while pyb.elapsed_micros(u) < 100:
        count+=1
    print(count)


    
@micropython.native 
def p(c='X8'):
    """
    time get a pin value
    13
    """
    p = pyb.Pin(c,pyb.Pin.OUT_PP,pull=pyb.Pin.PULL_NONE)
    p.low()
    print(p.value())

    print('time get a pin value')

    u = pyb.micros()
    p.value()
    t = pyb.micros()-u
    print (t)

@micropython.native     
def pt(c='X8'):
    p = pyb.Pin(c,pyb.Pin.OUT_PP,pull=pyb.Pin.PULL_NONE)
    p.low()
    print(p.value())

    print('time for LOW output to get PULLED HIGH as input')

    u = pyb.micros()
    p.init(pyb.Pin.IN,pull=pyb.Pin.PULL_UP)
    while not p.value():
        pass
    t = pyb.micros()-u
    print (t)

    print('time for a HIGH input to go to LOW output')
    u = pyb.micros()
    p = pyb.Pin(c,pyb.Pin.OUT_PP,pull=pyb.Pin.PULL_NONE)
    p.low()
    while p.value():
        pass
    t = pyb.micros()-u
    print (t)
    
    print('time for a LOW output to go to HIGH output')
    u = pyb.micros()
    p.value(1)
    while not p.value():
        pass
    t = pyb.micros()-u
    print (t)

@micropython.native    
def ppt():
    """ 
    Pyboard times:
    Time to wait for not t
    10
    Time to wait for f
    10
    """

    f =False
    t =True

    print('Time to wait for not t')
    u = pyb.micros()
    while not t: 
        None
    t = pyb.micros()-u
    print (t)

    print('Time to wait for f')
    u = pyb.micros()
    while f: 
        None
    t = pyb.micros()-u
    print (t)

@micropython.native     
def pppt():
    """
    time to do absolutely nothing.
    9
    time to execute None.
    8
    time to execute 5x None.
    9
    """
    print('time to do absolutely nothing.')
    u = pyb.micros()
    t = pyb.micros()-u
    print (t)

    print('time to execute None.')
    u = pyb.micros()
    None
    t = pyb.micros()-u
    print (t)

    print('time to execute 5x None.')
    u = pyb.micros()
    None
    None
    None
    None
    None
    t = pyb.micros()-u
    print (t)


@micropython.native
def ct(c='X8'):
    bits = 0
    for i in range(5):
        bits = (bits <<2) |2
    #p = pyb.Pin(c,pyb.Pin.OUT_OD,pull=pyb.Pin.PULL_NONE)
    u = pyb.micros()
    while (bits):
        pyb.udelay(50)
        if(bits & 1):
            p = pyb.Pin(c,pyb.Pin.IN,pull=pyb.Pin.PULL_UP)
        else:
            p = pyb.Pin(c,pyb.Pin.OUT_OD,pull=pyb.Pin.PULL_NONE)
            p.low()
        bits = bits >> 1
        #pyb.udelay(10)
    t= pyb.micros()-u
    #p = pyb.Pin(c,pyb.Pin.IN,pull=pyb.Pin.PULL_UP)
    #while not p.value():
    #    print('o')
    print('elapsed time: ' +str(t))
    

def oc(d='X2',c='X3',b='X4',a='X5'):
    A= pyb.Pin(a,pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)
    B = pyb.Pin(b,pyb.Pin.IN,pull=pyb.Pin.PULL_NONE)
    C = pyb.Pin(c,pyb.Pin.OUT_OD,pull=pyb.Pin.PULL_NONE)
    D = pyb.Pin(d,pyb.Pin.OUT_OD,pull=pyb.Pin.PULL_NONE)
    return(A,B,C,D)


def od(d='X2',c='X3',b='X4',a='X5'):
    A= pyb.Pin(a,pyb.Pin.IN,pull=pyb.Pin.PULL_UP)
    B = pyb.Pin(b,pyb.Pin.IN,pull=pyb.Pin.PULL_UP)
    C = pyb.Pin(c,pyb.Pin.OUT_OD,pull=pyb.Pin.PULL_UP)
    D = pyb.Pin(d,pyb.Pin.OUT_OD,pull=pyb.Pin.PULL_UP)
    return(A,B,C,D)
