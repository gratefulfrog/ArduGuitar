# clt.py
# class test stuff
# using class members as default values to init; It Works!
#

class cl:
    iVal= 12
    iVec = [0,1,2]


    def __init__(self,i=iVal,v=iVec):
        self.i = i
        self.v = v

    def __repr__(self):
        return 'CL:' + \
            '\n\ti:\t'  + str(self.i) + \
            '\n\tv:\t'  + str(self.v)
    
