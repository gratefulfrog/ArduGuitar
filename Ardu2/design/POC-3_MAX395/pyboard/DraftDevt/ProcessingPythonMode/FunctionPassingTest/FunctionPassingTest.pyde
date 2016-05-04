# a demo of passing a method as an argument in python-processing - IT WORKS!!!

class CC:
    def __init__(self,x):
        self.id = x
        
    def x(self):
        print('my id: ' + str(self.id))

class DD:
    def __init__(self,x):
        self.func = x
        
    def x(self):
        self.func()
        
littleC = CC(12)
littleD = DD(littleC.x)
    
def setup():
    size(200,300)
    
def draw():
    littleD.x()
    littleC.id = littleC.id+1
    