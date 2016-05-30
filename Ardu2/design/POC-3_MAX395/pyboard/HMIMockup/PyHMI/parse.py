# parse.py
# python version of lisp code

"""
parsing coil-node expressions

a coil Z has 2 endpoints: Z+ and Z-

a Node is of the form:
[LP, lM, ListOfPairs]
where 
* LP is a list of coil end points connected to OUT+
* LM is connected to OUT-
* ListOfPairs is of the form [[a,b],[x,y]..]
* where
** each pair is a pair of connections, eg. ['A+','B-']...

Let's say that the connections data structure is a list of lists:
[list-out+ list-out- list-of-lists-of-internal-connections]
[[out+] [out-] [[internal connection] [internal connection] ...]]

then we need to get the pair-wise connections of the form:
[[A+  out+] [a-  b+] [... etc]

thus we need some high level functions to define the circuit
and a function to get all the necessary connections

Define a Parallel connection
pp(coil1 &optional coil2 coil3 coil4)
paralllel connection of all the coils given

Define a Series connection
ss(coil1 coil2 &optional coil3 coil4)
series connection of all the coils given

both the above functions return a connection list which is the argument
needed to get the pair-wise list of connected terminals

Get the pair-wise connected terminals
connection-list (ss ('c1' 'c2' pp ('c3' 'c4')))
-> [["C1+" "out+"] ["C3-" "out-"] ["C4-" "out-"] ["C3+" "C4+"] ["C2-" "C3+"]
    ["C2-" "C4+"] ["C1-" "C2+"]]

all the others are helper functions
"""

from functools import reduce

def n (nd,ind):
    """
    this little helper function takes a node and an index and returns the 
    element that is required:
    0: out+
    1: out-
    2: internals
    """
    if nd:
        rep = nd
        if type(nd) == str:
            rep = [[nd+'+'],[nd+'-'],[]]
        return rep[ind]
    else:
        return  []
    
  
def nPlus (nd):
    """
    return the out+ of the node
    """
    return n(nd, 0)

def nMinus(nd):
    """
    return the out- of the node
    """
    return n(nd, 1)
    
def nStar(nd):
    """
    return the internals of the node
    """
    return n(nd, 2)

def connect (coilA,coilB):
    """
    a and b are lists, this concatenates them
    just syntactic sugar, returns a list of a+b
    """
    return coilA + coilB

def mapConnect(lis, res=[]):
    if len(lis)==1:
        return res
    else:
        return mapConnect(lis[1:],[[lis[0],elt] for elt in lis[1:]] + res)

    
###################
### TOP LEVEL CALLS
###################

def p(n1 , n2 = []):
    """
    parallel connect nd1 nd2 means:
    out+ = the out+ of nd1 and nd2 connected together
    out- = the out- of nd1 and nd2 connected together
    whatever previous internal connections there were are maintained
    """
    return [connect (nPlus(n1), nPlus(n2)),
            connect (nMinus (n1), nMinus (n2)),
            nStar (n1) + nStar(n2)]

def s (n1, n2):
  """
  series connect nd1 nd2 means:
  out+ = the out+ of nd1 
  out- = the out- of nd2 
  internals = add a connection from out- of nd1 to out+ of nd2 to
  whatever previous internal connections there were."
  """
  return [nPlus (n1),
          nMinus (n2),
	  [connect (nMinus (n1), nPlus (n2))] + nStar (n1) + nStar (n2)]

def pp (n1, *otherNodes):
    """"
    returns a list of n parallel connected nodes where n>0
    """
    #print(n1)
    #print(otherNodes)
    return p(n1) if not otherNodes else reduce(p, [n1] + list(otherNodes))

def ss(n1, n2, *otherNodes):
    """
    returns a list of n series connected nodes where n > 1
    """
    #print(n1,n2)
    #print(otherNodes)
    return s(n1,n2) if not otherNodes else  reduce(s, [n1,n2] + list(otherNodes))

def connectionList (cLis):
    return [[elt, 'OUT+'] for elt in cLis[0]] + \
           [[elt, 'OUT-'] for elt in cLis[1]] + \
           ([] if not cLis[2] else reduce(lambda x,y: x+y,[mapConnect(x) for x in cLis[2]]))
