class C:
    def __init__(self):
        self.x=1

    def show(self, arg):
        print(eval('self.' + arg, globals(),{'self':self}))

