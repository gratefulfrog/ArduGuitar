# acc.py
# tests of accellerometers

from pyb import Accel, LED, delay

red    = LED(1)
green  = LED(2)
yellow = LED(3)
blue   = LED(4)


def test(min=5):
    a = Accel()
    while True:
        print (a.filtered_xyz())
        print(a.tilt())
        print(a.x())
        print(a.y())
        print(a.z())
        delay(200)

def rock(s = 10):
    a = Accel()
    delay(50)
    count = [0,0,0]
    v= [a.x(),a.y(),a.z()]
    while True:
        x = a.x()
        y = a.y()
        z = a.z()
        xd = abs(x-v[0]) > s
        yd = abs(y-v[1]) > s
        zd = abs(z-v[2]) > s
        v[0]=x
        v[1]=y
        v[2]=z
        if  xd and yd:
            print("x y: " +str(count[0]))
            count[0] +=1
        if  xd and zd:
            print("x z: " +str(count[1]))
            count[1] +=1
        if  zd and yd:
            print("y z: " +str(count[2]))
            count[2] +=1
        delay(50)
    
def fvn():
    a=Accel()
    delay(50)
    while True:
        f = a.filtered_xyz()
        x = a.x()
        y = a.y()
        z = a.z()
        t = a.tilt()
        print ('filtered: ' + str(f))
        print ('raw:      (' + str(x) + ',' + str(y) + ',' + str(z) + ')')
        print('tilt:      '  + str(t))
        print('----------------')
        delay(1000)
        
    
