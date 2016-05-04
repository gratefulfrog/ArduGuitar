## HMI mockup python version

import Classes

widthReal =  300  # millimeters
heightReal = 220;

def settings():
  size(int(round(widthReal*Classes.Positionable.scaleFactor)),int(round(heightReal*Classes.Positionable.scaleFactor)))
"""
lcVect = [None for i in range(5)]

lcd LCD(140,0)
pb = [PushButton(167 + i*14,30, Actuator()) for i in range (2)]
LedPB[] lpbs = new LedPB[4];


def doLCD():
    lcd.setLn(1,'^')
    lcd.display()

def setup():
    doLeds()
    doLCD()
    global lpbs
  int ind = 0;
  int[] colInd = {4,5,2,1};
  for (int i=0;i<2;i++):
    for (int j = 0;j<2;j++):
    lpbs[ind] = new LedPB(140+j*LedPB.hSpacing, 51+i*LedPB.vSpacing, LEDColors[colInd[ind]]);
    lpbs[ind].display();
    ind++;
    }
  }
   
}

def draw():
  pb[0].display();
  pb[1].display();
  for (int i =0;i<4;i++):
    lpbs[i].display();
  }
}
"""

l =  Classes.LED(100,100,Classes.LED.blue)
ll = Classes.LedLine(15,20)    
lc = Classes.LedCross(40,22)
ld = Classes.LedDisplay(70,40)
def doLeds():
    [(ld.setV(i,i+3), ld.setT(i,i+2)) for i in range(5)]
    ld.TR.set(7)
    ld.display()

def setup():
    doLeds()
    
"""
currentM = millis()
count=0

def draw():
    global currentM
    global count
    if millis() > currentM + 1000: 
        l.toggle()
        currentM = millis()
        count = (count+1)%3
        ll.toggle(count)
    l.display()
    ll.display()
"""