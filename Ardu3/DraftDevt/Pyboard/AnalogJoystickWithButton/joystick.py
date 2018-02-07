from pyb import Pin, ExtInt, ADC
import time

def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

class JoyStick:
    def __init__(self,xp,yp, pbp, pbFunc):  # last arg is a pointer to the interrupt handler
         self.XPin = ADC(Pin(xp))
         self.YPin = ADC(Pin(yp))
         self.PBPin = Pin(pbp, Pin.IN, Pin.PULL_UP)
                          
         self.maxAnalog = 4095
         self.minAnalog = 0
         self.maxOutput = 100
         self.minOutput = -100
         self.pinExpo = 25

         self.onPB = pbFunc
         self.changeDelta   = 400   # ms
         self.lastChangeTime = 0    # ms

         self._calibrateXY()

    def _calibrateXY(self):
        xSum = 0
        ySum = 0

        for i in range(100):
            xSum += self.XPin.read()
            ySum += self.YPin.read()

        self.X0 = round(xSum/100.0)
        self.Y0 = round(ySum/100.0)

    def checkPB(self):
        now = time.ticks_ms()
        if now-self.lastChangeTime > self.changeDelta:
            if not self.PBPin.value():
                self.onPB()
                self.lastChangeTime = now
                
        

    def _read(self, x):
        pin = self.XPin
        V0 =  self.X0
        if not x:
            pin = self.YPin
            V0 =  self.Y0
            
        val = pin.read()
        if abs(val - V0) < self.pinExpo:
            return(0)
        return arduino_map(val,V0,self.maxAnalog,0,self.maxOutput) \
            if val > self.X0 else \
               arduino_map(val,self.minAnalog,V0,self.minOutput,0) 

    def readX(self):
        return self._read(True)
    def readY(self):
        return self._read(False)
    
  
