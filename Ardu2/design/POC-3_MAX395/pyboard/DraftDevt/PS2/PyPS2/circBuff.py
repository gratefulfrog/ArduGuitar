# circBuff.py
# implementation of a circular buffer to support concurrent reading
# and writing

buffSize = 5

class circBuff:
    class overflow(Exception):
        def __init__(self):
            pass
        def __repr__(self):
            return 'Overflow Exception!'
    class underflow(Exception):
        def __init__(self):
            pass
        def __repr__(self):
            return 'Underflow Exception!'
        
    def __init__(self,size=buffSize):
        self.buff    = [None for i in range(size)]
        self.nextIn  = 0
        self.nextOut = 0
        self.nbElts  = 0
        self.size    = size

    @micropython.native    
    def incNext(self,ingoing=True):
        if ingoing:
            self.nextIn = (self.nextIn +1)%self.size
        else:
            self.nextOut = (self.nextOut +1)%self.size

    @micropython.native    
    def put(self, elt,overwrite=False):
        """
        if overwrite is true, then the buffer will potentially
        overwrite elements that have not been read.
        Warning:the outpointer will not necessarily point to the oldest elt!
        """
        if not overwrite and self.nbElts == self.size:
            raise self.overflow()
        else:
            self.buff[self.nextIn]=elt
            self.incNext()
            self.nbElts =min(self.size,self.nbElts+1)

    @micropython.native    
    def get(self,remove=True):
        """
        if remove is False, the item is not removed, but it is returned.
        """
        if not self.nbElts:
            raise self.underflow()
        else:
            res = self.buff[self.nextOut]
            self.incNext(False)
            if remove:
                self.nbElts -=1
            return res
        
    def __repr__(self):
        res =  'size:\t' + str(self.size)
        res += '\nNb Elts:\t' +str(self.nbElts)
        res += '\nNext In:\t' +str(self.nextIn)
        res += '\nNext Out:\t' +str(self.nextOut)
        res += '\n' + repr(self.buff)
        return res
    
        
