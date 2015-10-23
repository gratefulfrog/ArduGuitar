#vs2mouse.py
# to test the Storm ps/2 trackball
# non class version

from vs2 import init, read, write
from pyb import udelay,delay

def mInit():
    """
    set up the vs2 module
    """
    init()
    delay(20) # this seems to be needed
    _mInit(read,write,udelay)

def run():
    """
    init the module,
    then run an infinite loop, polling the ps/2 trackball, and displaying the results
    """
    mInit()
    delay(20)
    loop(read,write,delay)

@micropython.viper    
def _mInit(read,write,ud):
    """
    send RESET
    read 3 times
    send REMOTE MODE
    wait one clock cycle
    """
    # send the RESET byte 0XFF
    write(0XFF)
    # read the 3 bytes replied
    r1 = read()   # ack byte   0xFA
    r2 = read()   # BAT        0xAA
    r3 = read()   # device ID  0x00

    # display the replies
    print('ACK (0xFA)\t',hex(r1),'\tBAT (0xAA)',hex(r2),'\tID (0x0)',hex(r3))

    # send the REMOTE MODE command, this means that the device will wait for a poll, then reply;
    # it will not initiate communication on its own
    write(0xF0)  # remote mode
    r3 = read()  # ack 0xFA
    # display the ACK
    print('ACK (0xFA)\t',hex(r3))

    # wait, I'm not sure why??
    ud(100) #microseconds

    
@micropython.viper    
def loop(read,write,ddelay):
    """
    arguments seem to be needed to pass functions????
    In an infinite loop:
    - poll the device for data
    - if the data is different from the last displayed data, then display it
      The device replies to the poll with 4 bytes: ACK, STATUS, deltaX, deltaY, all values since last poll
    - wait for 20 ms
    """
    # variables to hold current and previous values
    mstat = 0x7fffffff
    mx    = 0x7fffffff
    my    = 0x7fffffff
    lstat = 0x7fffffff
    lx    = 0x7fffffff
    ly    = 0x7fffffff
    
    while True:
        write(0XEB)  # poll for data
        read()  # ack byte 0xFA
        mstat = read()   # status byte 
        mx = read()   # delta X
        my = read()   # delta Y

        # if something is new, then display it,
        if (mstat != lstat) or (mx != lx) or (my != ly):
            display(mstat,mx,my)
            lstat = mstat
            lx = mx
            ly = my
        ddelay(20)  # milliseconds
        

def display(stat:int,x:int,y:int):
    """
    a little helper function to format the results read from the poll of the device
    """
    # these are the potential values carried by the status byte
    statVec = ["Left",
               "Right",
               "Middle",
               "None",
               "-X",
               "-Y",
               "X Overflow",
               "Y Overflow"]
    # the values will be appended to this variable 
    status  = '\t'
    
    for i in range(8):
        if stat & (1<<i):
            status += ',' + statVec[i] if status != '\t' else statVec[i]
            #if i<7:
            #    status += ','
    # now convert unsigned bytes to negative values if status byte says so 
    if stat & (1<<4):
        x -= 256
    if stat &(1<<5):
        y -= 256

    # display the results
    print('X:\t',x,'\tY:\t',y,status)
        
    
