class Mapper:
    """ create an instance that has one member function, which
    takes a number as arg and returns the value mapped from
    the 'frm' range to the 'to' range given as tuples/lists to the
    constructor.
    Usage:
    >>>import mapper
    >>> m = mapper.Mapper((0,10),(0,20))
    >>> m.map(2)
    4.0
    >>> m.map(0)
    0.0
    >>> m.map(10)
    20.0
    >>> m.map(100)
    200.0
    >>> m.map(-10)
    -20.0
    >>> x=m.map(-10)
    >>> x
    -20.0
    """
    def __init__(self,frm,to):
        self.map = lambda y: frm[0]+ (y-frm[0])*(to[1]-to[0])/(frm[1]-frm[0])
