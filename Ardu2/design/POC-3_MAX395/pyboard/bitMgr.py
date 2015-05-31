#!/usr/local/bin/python3.4
# bitMgr.py
# provides functionality to update bit arrays for shifting
 
from state import State
from dictMgr import *

class BitMgr:
    """ This is a serious worker class that provides lots of functionality.
    We will look at the static class variables and method first, then describe
    those of the instance.
    Static Class Variables:
    - cur: index value of the current bit array
    - nex: index value of the future bit array
    both the above work with the instance variable cnConfig which is a vector
    of length 2. each elt of the vector is itself a vector of ints used 
    as 8 bits.
    Next, we have the 3 RegEndPoints tuples:
    - switchRegEndPoints 
    - ivtrRegEndPoints 
    - allRegEndPoints 
    these are used to know where the switch connections are managed and where
    the ivtr bits are managed in view of clearing, updating etc. The usage
    is explained in the instance methods below.
    Next, we have a static method:
    - baseFunc(...)
    This is described in its own documentation, but it is static because it
    does not use any instance members.
    instance creation and usage:
    >>> from state import State
    >>> from bitMgr import BitMgr
    >>> b = BitMgr()
    >>> b.current()
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    >>> b.next()
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    >>> b.update('A',State.Vol, State.l3)
    masking:   # etc.
    >>> b.next()
    [0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0]
    >>> b.x()
    setting:   # etc.
    >>> b.reset(BitMgr.allRegEndPoints)
    """
    cur = 0 # index of the current config
    nex = 1 # index of the underwork, next config
    # end point ranges for reset method
    switchRegEndPoints = (0,State.nbSwitchRegs)
    ivtrRegEndPoints = (State.nbSwitchRegs,State.nbShiftRegs)
    allRegEndPoints = (0,State.nbShiftRegs)

    def baseFunc(onOff,name,att,val):
        """ 
        This helper static method is used to produce the setting and masking
        which are needed for updating the vectors
        Args:
        0: if True, we are making a setting, if not we are turning Off
        1: a coil name, eg. 'A'
        2: one of State.Inverter|State.Vol|State.Tone|State.ToneRange
        3. one of State.lOff| State.l0| ... |State.l5
        return:
        (setting, masking) as a tuple where
        - setting is the result of looking up name,att,val in the vtrDict, 
          or None if onOff is False!
        ie. a pair (Reg,Bit),
        - masking is a list of pairs from the maskingDict
        special case for turning Off, no settings!
        """    
        setting = None
        # if onOff is True, were are making a setting
        if onOff:
            setting = (vtrDict[name][att][val])
        masking = maskingDict[name][att]
        return (setting,masking)

    def __init__(self,nb_shiftRegs=State.nbShiftRegs):
        """
        creates an instace with all bits at zero.
        usage
        >>> b = BitMgr()
        """
        self.cnConfig = ([0 for x in range(BitMgr.allRegEndPoints[0],
                                           BitMgr.allRegEndPoints[1])], 
                         [0 for x in range(BitMgr.allRegEndPoints[0],
                                           BitMgr.allRegEndPoints[1])])

    def reset(self,whatRange, curBool=True,nexBool=True):
        """
        usage:
        b.reset(BitMgr.allRegEndPoints) # resets all bits
        """
        cnRange = []
        if curBool:
            cnRange += [BitMgr.cur]
        if nexBool:
            cnRange += [BitMgr.nex]
        for i in cnRange:
            for j in range(whatRange[0],whatRange[1]):
                self.cnConfig[i][j] = 0

    def current(self):
        """
        returns the current bits vector
        """
        return self.cnConfig[BitMgr.cur]

    def next(self):
        """
        returns the next bits vector
        """
        return self.cnConfig[BitMgr.nex]

    def update(self,name, att, state=State.connectionUpdateOnly):
        """ To call update(...) on name, att, state
        >>> update('A',State.Inverter,State.l2)
        To call update(...) on connections
        >>> update(('A',0),('B',1))
        this method sets up the call to doSettingMasking 
        which makes the member variable assignments
        ---
        Note that there is a procedural difference between updating
        a Vol, Tone,ToneRang, Inverter setting, and updating a connection
        setting.
        In the former case, the non-affecting attributes are maintained. 
        In the latter case, all the connection settings are reset prior to 
        updating. Examples:
        If we had  'A', Vol, l3 already, then we set 'A', Inverter, 1, then
        both the vol and inverter settings are maintained.
        But if we have some connections and we add are starting a new one then
        the previous ones are erased. However, if we have already started
        adding connections, then the previous NEW ones are maintained.
        """
        if state == State.connectionUpdateOnly:
            self.doSettingMasking(connectionsDict[(name,att)],[])
        else:
            # all states can be 'State.lOff', ie None !
            onOff = not state == State.lOff
            (setting, masking) = BitMgr.baseFunc(onOff,
                                                 name,
                                                 att,
                                                 state)
            self.doSettingMasking(setting,masking)
        
    def x(self):
        """
        This is the Execute method for the instance.
        It copies all the values from the NEXT vector to the CURRENT vector
        and then prints both to stdout.
        """
        for i in range(len(self.cnConfig[BitMgr.nex])):
            self.cnConfig[BitMgr.cur][i] = self.cnConfig[BitMgr.nex][i]
        self.printConfigs(None,[])
        
    def doSettingMasking(self,setting,masking):
        """
        This helper method applies the masking, by AND, then
        applies the setting by left shifting a 1 the setting times, then OR 
        it with the other non masked settings.
        The configs are printed to stdout after assignment.
        """
        for (reg,mask) in masking:
            self.cnConfig[BitMgr.nex][reg] &= mask
        if setting:
            self.cnConfig[BitMgr.nex][setting[0]] |= pow(2,setting[1])
        self.printConfigs(setting,masking)

    def printConfigs(self,setting,masking):
        """
        A little helper routing to print setting and masking to stdout for
        user information.
        To print only the config vectors, call:
        >>> b.printConfigs(None, [])
        """
        for (reg,mask) in masking:
            State.printT("masking: ", 
                         ["{0:d}".format(reg), "{0:#b}".format(mask)])
        State.printT('setting: ' + str(setting))
        State.printT(self)

    def __repr__(self):
        s = 'currentConfig:\t' + \
            str(["{0:#b}".format(x) \
                     for x in self.cnConfig[BitMgr.cur]]) + '\n' + \
                     'nextConfig:\t' + \
                     str(["{0:#b}".format(x) \
                              for x in self.cnConfig[BitMgr.nex]])
        return s


