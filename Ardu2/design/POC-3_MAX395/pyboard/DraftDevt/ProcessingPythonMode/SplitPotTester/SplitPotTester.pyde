import Classes
import stubs

widthReal =  300  # millimeters 
heightReal = 220;
bg = 40

def settings():
  size(int(round(widthReal*Classes.Positionable.scaleFactor)),
       int(round(heightReal*Classes.Positionable.scaleFactor)))

spa=None
sp=None
def setup():
    global spa
    global sp
    #sp = Classes.SplitPot(30,100,'Goop',(None,None))#[stubs.makeVTFunc(name) for name in ['Goop']])
    spa= Classes.SplitPotArray(0,100,[stubs.makeVTFunc(name) for name in Classes.SplitPotArray.names])  #(stubs.onNewVol,stubs.onNewTone) for i in range(6)])
    
def draw():
    background(40)
    spa.display()
    #sp.display()