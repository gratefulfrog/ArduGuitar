#ttemp.py

# testing the 11 bit reading of PS/2 protocol

class ps2BitReader:
    ackShift=-1
    stopShift = 0
    parityShift = 1
    startShift = 10
    
    def __init__(self,device=True):
        self.bits=0
        self.bitCount=0
        self.device = device
        self.maxBits = 11
        self.extraShift=0
        if not device: # host sends 12 bits, device only 11
            self.maxBits = 12
            self.extraShift=1
            
    def addBit(self,bit):
        # no error checking
        self.bits |= (bit<<self.bitCount)
        self.bitCount += 1

    def getStop(self):
        return 1 & (self.bits >> (self.stopShift+self.extraShift))
    def getParity(self):
        return 1 & (self.bits >> (self.parityShift+self.extraShift))
    def getStart(self):
        return 1 & (self.bits >> (self.startShift+self.extraShift))
    def getAck(self):
        # no error checking
        return 1 & (self.bits >> (self.ackShift+self.extraShift))
    def getValue(self):
        return 255 & (self.bits >> 2 +self.extraShift)

    def isFull(self):
        return self.bitCount == self.maxBits

    def parityOk(self):
        dataBits= self.getValue()
        count = 0
        while (dataBits):
            if (dataBits & 1):
                count = (count + 1) %2
            dataBits = dataBits >> 1
        return count == self.getParityBit()
    
    def __repr__(self):
        return str(self.bits)



