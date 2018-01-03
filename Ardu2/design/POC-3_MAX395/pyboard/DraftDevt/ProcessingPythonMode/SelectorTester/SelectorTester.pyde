import Classes,stubs

widthReal =  300  # millimeters
heightReal = 220;
bg = 40

def settings():
  size(int(round(widthReal*Classes.Positionable.scaleFactor)),
       int(round(heightReal*Classes.Positionable.scaleFactor)))

sh = Classes.Selector(185, 52,Classes.Selector.white,True,stubs.hSelect)
sv = Classes.Selector(220, 41,Classes.Selector.black,False,stubs.vSelect)

    
def draw():
    background(bg)
    sh.display()
    sv.display()
    
