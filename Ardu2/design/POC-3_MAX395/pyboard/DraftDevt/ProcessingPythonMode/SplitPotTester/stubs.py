def makeVTFunc(name):
    return (lambda val: pWorkaround(name + ':\tVol:\t' + str(val)), 
            lambda val: pWorkaround(name + ':\tTone:\t' + str(val)))
        
def pWorkaround(v):
    print(v)