# rmap.py
# provides the RMap class which maps values from one range to another

class RMap:
    def __init__(self,fromRange, toRange, makeInt=False):
        """ 
        create an instance,
        will raise an error if the from Range is of Zero length.
        usage:
        >>> m = RMap([0,100],[0,10], True) # will return ints
        >>> m.v(8)
        1
        >>> n = RMap([0,100],[0,10]) # will return floats
        >>> n.v(8)
        0.8
        """
        self.ratio = (toRange[1]-toRange[0])/(fromRange[1]-fromRange[0])
        self.fZero = fromRange[0]
        self.tZero = toRange[0]
        if makeInt:
            self.typ = lambda x:round(x)
        else:
            self.typ = lambda x:x
        

    def v(self,val):
        """
        return the result of mapping val from the from range 
        to the target range.
        """
        return self.typ(self.ratio*(val-self.fZero) + self.tZero)
    
