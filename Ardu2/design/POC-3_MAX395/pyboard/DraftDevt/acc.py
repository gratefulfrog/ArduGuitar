# acc.py
# tests of accellerometers
# currently seems to work with the values as they are!

from pyb import Accel, LED, delay, millis

red    = LED(1)
green  = LED(2)
yellow = LED(3)
blue   = LED(4)

def xtest(p=5,m=-5, d= 20, timeOut= 1000):
    """
    this uses the pyboard leds to indicate movement in the x,y,z directions.
    x-axis: the shorter dimension of the board (BLUE led)
    y-axis: the longer  dimension of the board (YELLOW led)
    z-axis: vertical (GREEN led)
    How it works:
    1. define Zones, when the acceleration is greater than a positive threshold
       or less than a negative threshold. These thresholds are the arguments
       'p' and 'm',
    2. the zones are 1 if >= pos threshold, -1 if <= neg threshold, 
       and 0, i.e. the deadband, otherwise.
    3. base values for the acclerations are taken to determine the 'zero'.
    4. a vector of last times a led was changed is maintained for timeouts
    5. the 'd' argument is the delay between accelerometer readings.
    6. the timeOut is the time to wait before turning off a led for which 
       there has been no activity. 
    Loop:
       0. wait for the appropriate time to pass,
       1. if any new value is out of range, skip the iteration
       2. for each axis value, 
          0. find its zone, after subtracting the base val
          1. If we are in a detection zone not the deadband,
             0. if it has changed zones, then:
                toggle led,
                update timeout timer,
                update last zone
          2. if its timeout has expired, then
             turn off the corresponding led 
    """
    a = Accel()
    delay(50)
    global red,green, yellow, blue
    leds = [[blue,0],[yellow,0],[green,0]]
    ledsOff(leds)        
    zp = [0,0,0]
    zc = [0,0,0]
    base= [0,0,0]
    vc= [0,0,0]
    init = False
    while not init:
        delay(5)
        init = readAcc(a,base)
    t = millis()
    lastActionTime = [t,t,t]
    print ('Initialized!')
    while True:
        delay(d)
        if not readAcc(a,vc):  # then read error, skip this iteration
            print ('continuing...')
            continue
        for i in range(3):
            zc[i] = DetectionZone(vc[i]-base[i],p,m)
            if zc[i]: # we are in a detection zone
                if zc[i] != zp[i]:
                    toggle(leds[i])
                    lastActionTime[i] = millis()
                    zp[i] = zc[i]
            if millis()-lastActionTime[i] > timeOut:
                off(leds[i])

def readAcc(ac, valVect,):
    """
    reads ac in 3-axis, 
    if all values are ok, updates valVect & returns True
    if not returns False and does not update
    """
    vc = [ac.x(),ac.y(),ac.z()]
    if any([v>31 or v< -32 for v in vc]):  # error!
        return False
    else:
        for i in range(3):
            valVect[i]=vc[i]
        return True
                
def ledsOff(ls):
    [off(l) for l in ls]

def off(ldPair):
    ldPair[0].off()
    ldPair[1] = 0
    
def DetectionZone(val, posLim, negLim):
    res = 0
    if val >= posLim:
        res = 1
    elif  val <= negLim:
        res = -1
    return res

def toggle(ldPair):
    if ldPair[1]: # it's on, turn off
        ldPair[0].off()
        ldPair[1] = 0
    else:         # it's off, turn on
        ldPair[0].on()
        ldPair[1] = 1

def sign(x):
    if x==0:
        return 1
    else:
        return x/abs(x)

    
