from pyb import Pin, ADC
import time

def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def normalize(x, in_min, in_max, out_min=-1, out_max=1):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
def expoOutput(input,in_min,in_max,expo, rate):
    norm = normalize(input,in_min,in_max)
    return ((expo*pow(norm,3))+((1-expo)*norm))*rate


class ThumbStick:
    # expo formula
    # ouput =((EXPO*POW(input,3))+((1-EXPO)*input))*RATE
    # where input & output are on  [-1,1]
    
    def __init__(self,xp,yp, expo=0.9):  
         self.XPin = ADC(Pin(xp))
         self.YPin = ADC(Pin(yp))
                          
         self.maxAnalogX = 4095
         self.minAnalogX = 0
         self.maxAnalogY = 4095
         self.minAnalogY = 0
         self.maxOutput = 100
         self.minOutput = -100
         self.expo = expo

         print('Calibrating (0,0)')
         self._calibrate00()
         print('Done!')
         print('move stick continuously to all max and min points')
         self.calibrateMaxMin()
         print('Done!')

    def calibrateMaxMin(self):
        endTime = time.ticks_ms() +  5000 # secs to calibrate
        xMin = xMax = self.X0
        yMin = yMax = self.Y0
        while(endTime > time.ticks_ms()):
            x = self.XPin.read()
            y = self.YPin.read()
            xMin = min(xMin,x)
            xMax = max(xMax,x)
            yMin = min(yMin,y)
            yMax = max(yMax,y)
        self.maxAnalogX = xMax
        self.minAnalogX = xMin
        self.maxAnalogY = yMax
        self.minAnalogY = yMin
            
    def _calibrate00(self):
        xSum = 0
        ySum = 0

        for i in range(100):
            xSum += self.XPin.read()
            ySum += self.YPin.read()

        self.X0 = round(xSum/100.0)
        self.Y0 = round(ySum/100.0)

    def _read(self, x):
        pin = self.XPin
        V0 =  self.X0
        maxAnalog = self.maxAnalogX
        minAnalog = self.minAnalogX
        if not x:
            pin = self.YPin
            V0 =  self.Y0
            maxAnalog = self.maxAnalogY
            minAnalog = self.minAnalogY
            
        val = pin.read()
        #if abs(val - V0) < self.pinExpo:
        #    return(0)
        #return arduino_map(val,V0,maxAnalog,0,self.maxOutput) \
        return expoOutput(val,minAnalog,maxAnalog,self.expo,self.maxOutput) 
        #    if val > self.X0 else \
        #       arduino_map(val,minAnalog,V0,self.minOutput,0) 

    def readX(self):
        return self._read(True)
    def readY(self):
        return self._read(False)
    
  
