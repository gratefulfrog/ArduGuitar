class MicroValuator:
    """ 
    Reduces incrementation by the factor,
    used to desensitize the trackball
    """
    factor = 0.1  # make 10 steps for one click
    minV   = 0    # inclusive
    maxV   = 5    # inclusive

    def fit2Range(val):
        return max(MicroValuator.minV, min(val, MicroValuator.maxV))

    def __init__(self,idLis):
        """ idLis is a list of identifiers for the pairs that will be microvaluated
        """
        self.pDict = {}
        for id in idLis:
            self.pDict[id] = [0,0]

    def set(self,who,ind,val):
        """ 
        Sets the value but only for existing keys
        and only within the range of values
        """
        if who in self.pDict.keys():
            self.pDict[who][ind] = MicroValuator.fit2Range(val)
        
    def inc(self,who,ind,howMuch):
        """ micro increment dict[who][ind] by factor*howmuch
        """
        if who in self.pDict.keys():
            self.pDict[who][ind] = MicroValuator.fit2Range(self.pDict[who][ind]+howMuch*MicroValuator.factor)

    def valRounded(self, who,ind):
        """
        Do not check for a correct key, so that if a bad key is given, there will be an exception and we can fix it!
        """
        return round(self.pDict[who][ind])

    def __repr__(self):
        return str(self.pDict)
    
