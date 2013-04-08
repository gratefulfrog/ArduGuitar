#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
btSerial.py

 bluetooth doc at http://pybluez.googlecode.com/svn/www/docs-0.7/index.html

 implements the BTSerial Class providing serial comm for 
 Arduino/protocol_01.
 default values are set to work with the linvor and the Asus 1201N
 these may need updating over time
"""

import time,sys
import bluetooth
import config

class btSerialError(Exception):
    # an error to throw in case...
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class BTSerial():
    # this is the Object used for bluetooth com with the Arduino

    def __init__(self,config,comm=True):
        # com argument is to allow execution without a bluetooth connection
        self.conf = config
        setattr(self, config.socketTypeAttributeNameStr, eval(config.socketTypeStr))
        self.btSocket = None
        self.connected = False
        self.comm = comm
        #self.btSocket = bluetooth.BluetoothSocket(self.socketType)
        # is None, meainging blocking by default, self.btSocketw.gettimeout()
        if self.comm:
            self.connect()
            print "Socket not connected, comm..."
        else:
            print "Socket not connected, no comm..."
    
    def connect(self):
        # this is copied from the pybluez examples 
        # it seems to work, and always ends up by connecting.
        # careful adjustment of the sleep times is needed to get optimal resulst
        while(True):
            try:
                self.btSocket = bluetooth.BluetoothSocket(self.socketType)
                self.btSocket.connect(self.conf.sockethwTpl)
                # need to leave some reaction time
                time.sleep(self.conf.replyWaitTime)
                self.connected = True
                self.btSocket.settimeout(self.conf.socketTimeout)
                break;
            except bluetooth.btcommon.BluetoothError as error:
                print "Could not connect: ", error, "; Retrying ..."
                self.btSocket.close()
                self.btSocket = None
                #self.btSocket = bluetooth.BluetoothSocket(self.socketType)
                self.connected = False
                time.sleep(self.conf.reconnectWaitTime)

    def sendAndRecv(self,msg,expectedBytes):
        # send the message on the socket and wait until we receive
        # expectedBytes back, return the bytes received.
        # In multithreading this should be protected by a semaphore to avoid
        # multiple writes in paralllel.
        # exceptions are used to handle various potential comms problems...

        if not self.comm:
            print "BTSerial Send: " + msg + " no comm..."
            print "BTSerial Recv: expecting "+str(expectedBytes)+" bytes, no comm..."
            return 'x' + msg
        else:
            assert self.connected
            print "about to send"
            self.btSocket.sendall(msg)        
            print "sent: " + msg
            time.sleep(self.conf.replyWaitTime)  
            # need to leave some reaction time
            rec =  ""
            try:
                rec =self.btSocket.recv(expectedBytes)
                if len(rec)< expectedBytes:
                  # then something is wrong! raise an error
                  raise btSerialError((msg,rec))
            except bluetooth.btcommon.BluetoothError as err:
                print "Bluetooth error: ", err 
                print "Outgoing: ", msg
                print "Incoming: ", rec
                print "thread exiting..."
                sys.exit()
            except btSerialError as e:
                print "btSerialError: ", ((msg,rec))
                print "Outgoing: ", msg
                print "Incoming: ", rec
                print "thread exiting..."
                sys.exit()
            except Exception as ee:
                # who knows what went wrong
                print "Unexpected error: ", e
                print "Outgoing: ", msg
                print "Incoming: ", rec
                print "thread exiting..."
                sys.exit()
            return rec

def main():
    # just for tests, requires arduino micro with protocol_01
    conf = config.ArduGuitarConf()
    sk = BTSerial(conf.bt) 
    sk.connect() 
    print "Connected"

    while(True):
        s = raw_input("? ")
        sk.sendAndRecv(s, conf.protocol.incomingMsgLen*(len(s)/conf.protocol.outgoingMsgLen))

if __name__ == '__main__':
    main()


