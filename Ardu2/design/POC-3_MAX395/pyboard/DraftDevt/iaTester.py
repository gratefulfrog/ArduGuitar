# iaTester.py

import ihmAppTests

## test routines for ihmAppTests

class Loc:
    def __init__(self):
        self.m = ihmAppTests.LCDMgr('A')
    def u(self):
        self.m.updateDisplay()
    def l(self):
        self.m.onLeftButton()
        self.u()
    def r(self):
        self.m.onRightButton()
        self.u()
    

C = Loc()
u=C.u
l=C.l
r=C.r
m=C.m
u()
