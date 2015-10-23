# ttt.py

class tt:
    def staticFunc(x):
        print (x)

    def __init__(self,v):
        self.m =v

    def doit(self):
        tt.staticFunc(self.m)
        print ('called static func')

        
    
