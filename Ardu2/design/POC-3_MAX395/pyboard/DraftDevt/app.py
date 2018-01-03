# app.py
# tests to see if the sd card file overrides the FLASH file

import sys

def setPath():
    sys.path.append(None)
    for i in range(len(sys.path)-1,1,-1):
        sys.path[i] = sys.path[i-1]
    sys.path[0]='/sd'


class App():
    """
    This class is just a temp test that does nothing.
    On instanciation, it prints its name.
    """
    
    def __init__(self):
        """
        Instance creation;
        print name.
        """
        print(self)

    def __repr__(self):
        return "I'm an instance of " + self.__class__.__name__ + "!!!"
