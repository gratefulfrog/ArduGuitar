# connectionTester.py
# used to test the connecton matrix

from dictMgr import connectionsDict
from state import State

def getCons(k):
    """ 
    returns a sorted version of the keys argument
    non-destructive
    """
    args = []
    for tup in k:
        tt = []
        for j in tup:
            tt += [j]
        args +=[tt,]
    args.sort()
    return args


def doConnect(a,lis):
    """
    takes a list of the form [('A',0),('B',0)]
    and flattens it to ['A',0,'B',0]
    then feeds it to the app's connect method.
    """
    args = []
    for tup in lis:
        for j in tup:
            args += [j]
    a.connect(*args)
    a.x()

    
def run(a):
    """
    will execute all the connections in the connectionsDict 
    in cannonical order.
    ---
    usage
    >> a = App()
    >> run (a)
    ...
    """
    for arg in getCons(connectionsDict.keys()):
        doConnect(a,arg)
        print ('\n')
        print(arg)
        if ( 'q' == input('ok? ')):
            break
        

    
