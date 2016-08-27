# outils.py
# provides various utility classes and functions
# * RMap: maps values from one range to another
# * floor function
# * ceiling function

def floor (n,d):
    """ floor of the experssion n/d
    """
    return n//d

def ceiling (n,d):
    """ ceiling of the experssion n/d
    """
    res = n//d 
    return res if not (n/d - res) else res +1

def ljust(s,width,padchar=' '):
    """  Needed becaue micropython does not implement str.ljust
    takes a string s, and puts width padhcar's after it to make the total lenght of 
    st + padding equal to width. The original string is returned if width <= len(s)
    """
    l = len(s)
    if width<= l:
        return s
    return s + padchar*(width-l)

        
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
        self.tEnd  = toRange[1]
        if makeInt:
            self.typ = lambda x:round(x)
        else:
            self.typ = lambda x:x
        

    def v(self,val):
        """
        return the result of mapping val from the from range 
        to the target range. 
        Will only return values on [toRange[0],tRange[1]], ie. clamping!
        """
        return self.typ(min(self.tEnd,
                            max(self.tZero,
                                self.ratio*(val-self.fZero) + self.tZero)))
    
