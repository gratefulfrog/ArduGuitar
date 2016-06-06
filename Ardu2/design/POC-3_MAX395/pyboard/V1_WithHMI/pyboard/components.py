#!/usr/local/bin/python3.4
# components.py
# provides classes for all physical components of the guitar in user
# readable representatons
# 

from state import State

class CurrentNextable:
    """ this class provides the services for anything that 
    has a current and a next 'state' as in the class State.
    note the way updating works, if the 'add' argument is true
    then the new value will be 'added' as in '+' into the previous
    content of the nex. Depending on the type involved this could
    result in an addtion, or an appened operation...
    usage:
    >>> from components import CurrentNextable
    >>> cn = CurrentNextable()
    >>> cn
    CurrentNextable: 
	current:	None
	next:	None
    >>> cn.update(1)
    >>> cn
    CurrentNextable: 
	current:	None
	next:	1
    >>> cn.update(2)
    >>> cn.cn
    [None, 2]
    >>> cn.x()
    >>> cn.cn
    [2, 2]
    >>> cn.reset()
    >>> cn.cn
    [2, None]
    >>> cn.update([1])
    >>> cn.cn
    [2, [1]]
    >>> cn.update([2],True)
    >>> cn.cn
    [2, [1, 2]]
    """
    # index of the current value
    cur = 0
    # index of the next value
    nex = 1

    def __init__(self):
        """
        instance creation
        """
        self.cn = [State.lOff,State.lOff]
    
    def current(self):
        """
        return the CURRENT value
        """
        return self.cn[self.cur]

    def next(self):
        """
        return the NEXT value
        """
        return self.cn[self.nex]
    
    def reset(self, nextt = True, current = False):
        """
        resets to State.lOff, depending on arguments
        """
        if current:
            self.cn[CurrentNextable.cur] = State.lOff
        if nextt:
            self.cn[CurrentNextable.nex] = State.lOff

    def update(self, new,add=False):
        """
        updates the 'new' value to the next, using addition if
        'add' argument is True.
        If 'add' is False, then simply overwrites.
        """
        if not add or self.cn[self.nex] == None:
            self.cn[self.nex] = new
        else:
            self.cn[self.nex] += new

    def x(self):
        """
        copies NEXT to CURRENT.
        does not change NEXT.
        """
        self.cn[self.cur] = self.cn[self.nex]

    def __repr__(self):
        return 'CurrentNextable: ' + '\n\t'  \
            'current:\t' + str(self.cn[CurrentNextable.cur]) +'\n\t' + \
            'next:\t' + str(self.cn[CurrentNextable.nex]) 

class Connectable:
    """ anything which connects.
    Note that the connection is represented as a list t:
    [poleId, poilPolePair] eg. 0 -> ['B',1].  This is required to avoid
    tuple assignment issues.
    The name of the connected instance is not a member of this class but
    is required in the subclasses.
    the connected2 member variable is a list of 2 CurrentNextable's,
    these are the coils and their poles
    pole0 <-> index 0
    pole1 <-> index 1
    usage:
    >>> from components import Connectable
    >>> c = Connectable()
    >>> c.connect(0,['B',0])
    >>> c
    Connectable:
	reset:	True
	Connected2:
		CurrentNextable: 
		current:	None
		next:	[['B', 0]]
		CurrentNextable: 
		current:	None
		next:	None
    >>> c.connect(0,['C',1])
    >>> c
    Connectable:
	reset:	True
	Connected2:
		CurrentNextable: 
		current:	None
		next:	[['B', 0], ['C', 1]]
		CurrentNextable: 
		current:	None
		next:	None
    >>> c.x()
    >>> c
    Connectable:
	reset:	False
	Connected2:
		CurrentNextable: 
		current:	[['B', 0], ['C', 1]]
		next:	[['B', 0], ['C', 1]]
		CurrentNextable: 
		current:	None
		next:	None
    >>> c.connect(0,['M',0])
    >>> c
    Connectable:
	reset:	True
	Connected2:
		CurrentNextable: 
		current:	[['B', 0], ['C', 1]]
		next:	[['M', 0]]
		CurrentNextable: 
		current:	None
		next:	None
    """
    def __init__(self):
        """
        instance creation, we get a vector of 2 CurrentNextable's
        and 'reset' member variable is True, meaning there has been
        a reset since last connection was added.
        """
        self.connected2 = [CurrentNextable(),CurrentNextable()]
        self.reset = True

    def resetNextConnections(self):
        """
        resets the Next of each of the poles and 
        sets the member variable 'rest' to True
        should not need to be called from outside this class.
        """
        for i in (0,1):
            self.connected2[i].reset()
        self.reset = True

    def connect(self, myPoleId, coilPolePairAsList):
        """
        The connection method is the worker of this class.
        Arguments:
        0: a poleID i.e. 0 or 1
        1: a list of [CoilName,pole] for the other side of the connection
        This works as follows:
        by default we assume that the connection will be appended to any
        existing connections.
        But if the member 'rest' is False, then we need a reset first, and
        will not append.
        Finally, the Connectable member 'update' is called with the arguments
        needed.
        """
        appendNew = True
        if (not self.reset):
            self.resetNextConnections()
            appendNew = False
        self.connected2[myPoleId].update([coilPolePairAsList,], add = appendNew)
    
    def x(self):
        """
        Execute the connections to update the Current values, but only 
        for connections, Do nothing for N one values!
        set member variable 'reset' to False to say that a reset is needed.
        """
        for c in self.connected2:
            if (not c == None):
                c.x() 
        self.reset = False

    def __repr__(self):
        return 'Connectable:\n\t' + \
            'reset:\t' + str(self.reset) + '\n\t' + \
            'Connected2:\n\t\t' + \
            str(self.connected2[0]).replace('\n','\n\t') + '\n\t\t' + \
            str(self.connected2[1]).replace('\n','\n\t')

class VTable(Connectable):    
    """Providing services for anything with a Volume, Tone, and ToneRange.
    The name is needed for connection purposes.
    This is a user facing class where user readable data is maintained.
    member variables are as their names indicate, and for 
    - setFuncs 
     we find a vector of methods that can be called to do updating by indexed
     indirection.
    Instances provide the following services
    - vol(level) # sets the volume level
    - tone(level) # sets the tone level
    - toneRange(level) # sets the tone range
    - resetNext() = zeros the next of each member 
    - x() # calls x() of the members and Super Class.
    """
    def __init__(self,name):
        Connectable.__init__(self)
        self.name = name
        self.vol_ = CurrentNextable()
        self.tone_  = CurrentNextable()
        self.toneRange_  = CurrentNextable()
        # note that setFuncs[0] is set to a method in the 'Invertable' subclass
        self.setFuncs = [None,self.vol,self.tone,self.toneRange]
        
    def vol(self,level):
        self.vol_.update(level)

    def tone(self,level):
        self.tone_.update(level)

    def toneRange(self,level):
        self.toneRange_.update(level)

    def resetNext(self):
        super().resetNextConnections()
        self.vol_.reset()
        self.tone_.reset()
        self.toneRange_.reset()
        
    def x(self):
        self.vol_.x()
        self.tone_.x()
        self.toneRange_.x()
        super().x()

    def __repr__(self):
        return '\nVTable: ' + self.name + '\n\t' + \
            'vol: ' + str(self.vol_) + '\n\t' +\
            'tone: ' + str(self.tone_) + '\n\t' + \
            'toneRange: ' + str(self.toneRange_) + '\n\t' + \
            super().__repr__().replace('\n','\n\t')
            
class Invertable(VTable):    
    """Providing services for anything which can be inverted.
    The name is passed to the superclass!
    This class behaves like its superclass with simply an addional
    method:
    - invert(level)
    - resetNext() = zeros the next of each member 
    and a corresponding element in the setFuncs[] vector.
    """
    def __init__(self,name):
        VTable.__init__(self,name)
        self.setFuncs[0] = self.invert
        self.invert_ = CurrentNextable()

    def invert(self,level):
        self.invert_.update(level)

    def resetNext(self):
        super().resetNext()
        self.invert_.reset()

    def x(self):
        self.invert_.x()
        super().x()

    def __repr__(self):
        return '\nInvertable:\n\t' + \
            'invert: ' + str(self.invert_) + '\n\t' +\
            super().__repr__().replace('\n','\n\t')

class OnOffable():    
    """Providing services for anything which can be turned on and off.
    The name is passed to the superclass!
    This class behaves like its superclass with simply an addional
    method:
    - invert(level)
    - resetNext() = zeros the next of each member 
    and a corresponding element in the setFuncs[] vector.
    """
    def __init__(self):
        self.setFuncs =  [self.switch]
        self.onOff_ = CurrentNextable()

    def switch(self,level):
        self.onOff_.update(level)

    def resetNext(self):
        self.onOff_.reset()

    def x(self):
        self.onOff_.x()

    def __repr__(self):
        return '\nOnOffable:\n\t' + \
            'onOff: ' + str(self.onOff_) + '\n\t'
