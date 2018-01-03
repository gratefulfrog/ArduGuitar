## HMI mockup python version

import Classes
from config import PyGuitarConf
import FrontEnd


def settings():
  size(int(round(PyGuitarConf.Layout.widthReal*Classes.Positionable.scaleFactor)),
       int(round(PyGuitarConf.Layout.heightReal*Classes.Positionable.scaleFactor)))

ihm = None

def setup():
    global ihm
    global conf
    ihm =  FrontEnd.HMIMgr()

def draw():
    background(PyGuitarConf.Layout.bg)
    ihm.display()