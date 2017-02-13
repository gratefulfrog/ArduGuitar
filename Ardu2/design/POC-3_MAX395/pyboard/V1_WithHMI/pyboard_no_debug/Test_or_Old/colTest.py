import array, pyb

"""
This demonstrates the non-interrupt safeness of the circular Q.

The problem occurs when multiple interrupts occur during the execution of the callback and thus the call to push.

For example suppose a push is executing:
1. if self.qNbObj == Q.qLen:     # passes this...
2. else:                         # passes this...
3.      self.q[self.pptr] = e    # passes this..
4. INTERRUPTED, generating a new call to push before the ppter is incremented!!! thus pushing to the same place!

Voila why it doesn't work!
"""

class Q:
    """
    Circular Q of ints
    """
    qLen = 500
    
    def __init__(self):
        self.pptr = 0  # put pointer
        self.gptr = 0  # get pointer
        self.qNbObj=0  # object counter
        self.q = array.array('I',[0xFFFF for i in range(Q.qLen)])

    def push(self,e):
        if self.qNbObj == Q.qLen:
            #print('************************** Q Full! ignoring push! *******************************')
            raise Exception('Q Full! ignoring push!')
        else:
            self.q[self.pptr] = e
            self.pptr = (self.pptr+1) % Q.qLen
            self.qNbObj += 1
            
    def pop(self):
        res = None
        if self.qNbObj:
            res = self.q[self.gptr]
            self.gptr = (self.gptr+1) % Q.qLen
            self.qNbObj -=1
        return res

    def __repr__(self):
        res = ''
        for i in range(self.qNbObj):
           res += str(self.q[(self.gptr+i) % Q.qLen]) + ', '
        return res


class Collider:
    def __init__(self,qq):
        self.q = qq
        self.tim1 = pyb.Timer(4, freq=100,callback=self.callback)
        self.tim2 = pyb.Timer(5, freq=101,callback=self.callback)
        self.tim3 = pyb.Timer(6, freq=99,callback=self.callback)
        self.tim4 = pyb.Timer(7, freq=98,callback=self.callback)
        
        
    def callback(self, unused):
        self.q.push(self.q.pptr)


class App:
    def __init__(self,qq):
        self.collider = Collider(qq)
        self.q = qq

    def run(self):
        nb = 20
        lastRead = [-1 for i in range(nb)]
        i=0
        count = 0
        while True:
            res = self.q.pop()
            if res != None:
                if res in lastRead:
                    print ('Error: read: ',res, 'prev: ', lastRead)
                    break;
                else:
                    lastRead[i] = res
                    i = (i+1)% nb
                    print ('ok: ', count)
                    count += 1
                            

def dot():
    q=Q()
    a=App(q)
    a.run()
    
