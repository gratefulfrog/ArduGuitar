class C:
    def __init__(self):
        self.x=0

    def one(self):
        self.x = 1

    def zero(self):
        self.x = 0

class D(C):
    funcs = (C.one,C.zero)

    def __init__(self):
        C.__init__(self)

    def toggle(self):
        type(self).funcs[self.x](self)
    
