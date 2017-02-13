from pyb import *

x=Accel()
a=ADC('X19')
led = LED(1)

while True:
    led.toggle()
    x.x()
    a.read()
    delay(100)
    
