# trackball.py using the ps/2 protocol interrupt version is1.py
# This module demos the capture of trackball moveme t
# at the time of release, it stil freezes and the pyboard RED LED comes on
# occaisionally for unknow reasons, sorry.
#
# usage:
"""
>>> import trackball
>>> trackball.run()
dX:     1       dY:     1
dX:     -1      dY:     3
dX:     -9      dY:     5
...
"""
# user paramters to run:
# run (s)
# where s is the percentage sensitivity of 100%, min 1 max 100.
# higher s gives lower dX dY values since the polling frequency is higher,
# but it will load the pyboard cpu

import is1,pyb

# this is the delay between polling at 100% sensitivity
minPollDelay = 10 

def process (deltaX,deltaY):
    """
    put your code here, but remember, None values are possible in case of overflow
    """
    print('dX:\t' + repr(deltaX)+ '\tdY:\t' + repr(deltaY))

def run(sensitivity = 100):
    """
    does the init steps and then loops on poll calls
    """
    if not sensitivity or sensitivity >100:
        print('Sensitivity is a percent and must be on [100,1]')
        return
    
    s = round(minPollDelay * 100/ sensitivity)
    
    # init the is1 module
    is1.i()
    
    # reset the trackball
    is1.r()
          # set trackball to remote, i.e. polling mode
    is1.m()
    while True:
          # recover x,y offsets
        (x,y) = is1.p()
        # if there has been some movement, process it
        if x or y :
            process(x,y)
            lx=x
            ly=y
        # give some time to do other stuff!
        pyb.delay(s)
