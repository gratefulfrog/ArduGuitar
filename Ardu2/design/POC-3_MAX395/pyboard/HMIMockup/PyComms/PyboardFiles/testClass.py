class TestClass():
    def __init__(self,name='me'):
        self.name=name

    def sayHello(self):
        print ('Hello, my name is %s!'%self.name)
        return 'all ok!'
