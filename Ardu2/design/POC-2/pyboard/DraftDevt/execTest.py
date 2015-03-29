# execTest.py

class C:
    def __init__(self):
        self.x=1

    def exe(self,*args):
        print (args)

    def show(self):
        return exec('self.x')
