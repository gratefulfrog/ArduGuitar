#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
protocol.py 
"""

import sys
import config
import btSerial


class Protocol():

    def __init__(self,arduGuitarConf,comm=True):
        # com argument is to allow execution without a bluetooth connection
        # get a BluetoothSerial object instance
        # and check to be sure it's alive
        self.conf = arduGuitarConf.protocol
        self.bt = btSerial.BTSerial(arduGuitarConf.bt,comm)
        self.heartbeatCheck()

    def heartbeatCheck(self):
        # it would be nice to raise an exception in case of timeout
        # but I don't see how to do it for the moment...
        # anyway, this will be re-written when it goes to Android
        self.sendAndRecv(self.conf.heartbeatMsg)
        print "Pulse..."

    def sendAndRecv(self,msg):
        # send the message on the socket if it is right lenght and socket
        # is connected
        # receive the reply, and report any error
        assert len(msg)%self.conf.outgoingMsgLen == 0
        
        rec = self.bt.sendAndRecv(msg,self.
                                  conf.
                                  incomingMsgLen*(len(msg)/self.
                                                  conf.
                                                  outgoingMsgLen))
        if (self.conf.errorPrefix in rec) or  (msg != filter(lambda x: 
                                                             x not in self.conf.okPrefixes,
                                                             rec)):
            raise btSerial.btSerialError(msg + "," + rec)

    def send(self,pinValTupleLis):
        """ 
        pinValTupleLis of the form [(pin,val)...]
        send a single msg with all the values along to the connection.
        """
        #print pinValTupleLis
        outMsg = ""
        for tup in pinValTupleLis:                
            outMsg += str(tup[0]).zfill(2) + str(tup[1]).zfill(3) 
        self.sendAndRecv(outMsg)
        
def main():
    conf = config.ArduGuitarConf()
    pr = Protocol(conf) 
    while(True):
        s = raw_input("tuple list ? ")
        tl = eval(s)
        pr.send(tl)



if __name__ == '__main__':
    main()
