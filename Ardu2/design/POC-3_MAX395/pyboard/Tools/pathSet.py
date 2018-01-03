# pathSet.py
# set sys.path to first import from /sd.
# updated 2017 01 02

auto=True

import sys
from pyb import delay


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

def runTest():
    global a
    try:
        import app
        a=app.App()
        print('Running app.App()...')
        delay(1000)
        a.mainLoop()
    except KeyboardInterrupt:
        print('Done.')
        return a

set()
if auto:
    runTest()



