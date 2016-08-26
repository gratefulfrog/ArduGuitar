# pathSet.py
# set sys.path to first import from /sd.

import sys
def set():
    """
    extend the path variable by one slot,
    then rotate all the values one slot,
    then set path[0] to '/sd'
    """
    sys.path.append(None)
    for i in range(len(sys.path)-1,0,-1):
        sys.path[i] = sys.path[i-1]
    sys.path[0]='/sd'

set()

