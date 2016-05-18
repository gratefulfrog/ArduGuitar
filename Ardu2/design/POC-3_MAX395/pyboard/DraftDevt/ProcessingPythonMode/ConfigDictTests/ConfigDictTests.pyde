# tests of how to manage the current config and be able to update easily

currentDict = {1 : [3,9], 2 : [4, 8]}
ee = [{1 : [33,99], 2 : [44, 98]},
      {1  : [333,999], 2 : [444,898]}]

class testL:
    dict = currentDict
    @staticmethod
    def reset(newDict):
        print('\ntestL Reset')
        for k in testL.dict.keys():
            testL.dict[k]= newDict[k]
    
    # this works, and can be used as the general purpose conf holder
    def __init__(self, (key,ind)):
        self.key = key
        self.ind = ind
        
    def set(self, val):
        testL.dict[self.key][ self.ind] = val

    def get(self):
        return testL.dict[self.key][ self.ind]
    
    def __str__(self):
        return 'testL:' + '\ndict:\t' + str(testL.dict) + '\nkey:\t' + str(self.key)  + '\nind:\t' + str(self.ind) + '\nget():\t' + str(self.get())
                

def lisV():
    global o1
    global o2
    print('\nlisV()')
    
    o1 = testL((1,0))
    o1.set(555)
    
    o2 = testL((2,0))
    o2.set(666)
    

displayed = False
o1= None
o2 =None
def setup():
    lisV()
    print('Click Mouse to run reset!')

def draw():
    global displayed
    if not displayed:
        print(o1)
        print(o2)
        displayed= True

i = 0
def mouseClicked():
    global displayed
    global i
    testL.reset(ee[i])
    i and lisV()
    displayed=False
    i = 0 if i else 1
