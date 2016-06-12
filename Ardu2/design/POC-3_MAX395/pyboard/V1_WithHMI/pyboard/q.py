class Q:
    """
    Circular Q of ints
    """
    qLen = 20
    
    def __init__(self):
        self.pptr = 0  # put pointer
        self.gptr = 0  # get pointer
        self.qNbObj=0  # object counter
        self.q = [0xFF for i in range(Q.qLen)]
        self.debuggingPushMsg='push:'
        self.debuggingPopMsg='pop:%s'

    def push(self,e):
        if self.qNbObj == Q.qLen:
            raise Exception('Q Full! ignoring push!')
        else:
            self.q[self.pptr] = e
            self.pptr = (self.pptr+1) % Q.qLen
            self.qNbObj += 1
            print(self.debuggingPushMsg,e)
            
    def pop(self):
        res = None
        if self.qNbObj:
            res = self.q[self.gptr]
            self.gptr = (self.gptr+1) % Q.qLen
            self.qNbObj -=1
            print(self.debuggingPopMsg%hex(res))
        return res

    def __repr__(self):
        res = ''
        for i in range(self.qNbObj):
           res += str(self.q[(self.gptr+i) % Q.qLen]) + ', '
        return res

class EnQueueable:
    """
    This class encapsulates the top 5 bits of an equeue action, for memory
    * we enqueue a 16 bit integer
    * 1st Byte:
    INC ! PB ! CONF ! VOl ! TONE ! X ! Y ! Z
    where the 3 bits XYZ indicate the target of the action defined in the top 5 bits
    * 2nd Byte is a 2s complement signed integer with the value argument
    
    usage:
    q = Q()
    e = EnQueueable((EnQueueable.INC,EnQueueable.VOL),q)
    e.push(lower3bits,secondByte)
    
    """
    top5Bits = [1<<i for i in range(7,2,-1)]
    INC  = 0
    PB   = 1
    CONF = 2
    VOL  = 3
    TONE = 4
    
    def __init__(self,typIndex,q):
        """0 = inc
           1 = pb
           2 = conf
           3 = vol
           4 = tone
        """
        # type is an index to top5Bits
        self.top5 = 0
        if type(typIndex) == tuple:
            for t in typIndex:
                self.top5 |= EnQueueable.top5Bits[t]
        else:
            self.top5 = EnQueueable.top5Bits[typIndex]
        self.q = q
        
    def push(self,lower3,secondByte=0):
        #print('Enqueueable:\t' + hex(self.top5) + '\t' + hex(lower3))
        self.q.push(((self.top5 |lower3)<<8)|(0xFF & (secondByte if secondByte>=0 else 256+secondByte)))
        
