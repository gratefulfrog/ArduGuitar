# trackball.py using the interrupt version

import is1,pyb

# this is the delay between polling at 100% sensitivity
minPollDelay = 10 

def process (deltaX,deltaY):
    """
    put your code here, but remember, None values are possible in case of overflow
    """
    print('dX:\t' + repr(deltaX)+ '\tdY:\t' + repr(deltaY))

def run(sensitivity = 100):
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
