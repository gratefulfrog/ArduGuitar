#is2test.py

import is2

def test0(nb=1,parity = 1):
    for j in range(nb):
        # OxFF is the string
        bits = [0] + [1 for i in range(10)]
        bits[9] = parity
        #print(bits)

        for bit in bits:
            is2.rBuffer[is2.rIndex] = bit
            is2.rIndex = (is2.rIndex + 1)%is2.rBuffSize
        is2.nbBits2Process +=11
        #print(is2.nbBits2Process)
    return is2.bitList2ByteList()


"""
reset = [0xFF,3,0xFA,0xAA,0x0] # ACK, BAT, ID
remoteMode = [0xF0,1,0xFA] # ACK
poll = [0xEB,4,0xFA]  # ACK plus 3 data bits
"""



def test1(com):
    is2.sendCommandGetResponse(com)


def test2():
    is2.init()
    is2.reading=False
    is2.hostSetClockLow = False
    buf = [0 for i in range(11)]
    is2.sendCommand(buf)
