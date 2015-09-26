# trackball_0.py
#
# some trackball quadrature tests


import pyb

p = pyb.Pin(pyb.Pin.board.X1, pyb.Pin.IN)

iTime=pyb.millis()

def flagg(unused):
    global iTime
    iTime=pyb.millis()
            
pyb.ExtInt(p, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, flagg)

def run():
    global iTime
    countTime=pyb.millis()
    debounceDelay=1000
    count=0
    lastVal=False
    lastZeroTime=pyb.millis()
    
    while(True):
        if iTime - countTime > debounceDelay:
            if not lastVal:
                print('True,False')
                print(count)
                countTime= pyb.millis()
                count +=1
                lastVal = True
            else:
                lastVal = p.value()
                #print('True,True ', str(count))


        
