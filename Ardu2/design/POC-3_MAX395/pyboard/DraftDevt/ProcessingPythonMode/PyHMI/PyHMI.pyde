## HMI mockup python version

import Classes
from layout import layout
import FrontEnd

def settings():
  size(int(round(layout.widthReal*Classes.Positionable.scaleFactor)),
       int(round(layout.heightReal*Classes.Positionable.scaleFactor)))

ihm = None

def setup():
    global ihm
    ihm =  FrontEnd.HMIMgr()

def draw():
    background(layout.bg)
    ihm.display()
 