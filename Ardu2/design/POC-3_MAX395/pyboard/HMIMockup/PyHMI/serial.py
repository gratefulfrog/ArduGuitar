add_library("serial")

import os,sys,time

from processing.serial import Serial as PSerial

class Serial(object):
    """
    A wrapper around processing.serial.Serial to provide a
    PySerial.Serial like interface to a serial port. 
    """
    def __init__(self, port, baudrate=9600, *args, **kwargs):
        self._pserial = PSerial(this, port, baudrate)
        self.port = port
        self.baudrate = baudrate
        self._is_open = True
        self.timeout = (1000 if not kwargs else kwargs['interCharTimeout'])
        print('Connected to %s at %d baud.'%(port,baudrate))

    def _data_to_str(self, data):
        # pyserial read() returns strings 
        return "".join([chr(i) for i in data])

    def read(self, size=1):
        bytes_read = []
        start_time = time.time() 

        while len(bytes_read) < size:
            if self.inWaiting() > 0:
                val = self._pserial.read()

                if val != -1:
                    bytes_read.append(val)

            if time.time() - start_time > self.timeout:
                break

        return self._data_to_str(bytes_read)

    def write(self, s):
        for c in s:
            self._pserial.write(c)

        return len(s)

    def inWaiting(self):
        return self._pserial.available()

    def flush(self):
        return self._pserial.clear()

    def flushInput(self):
        return self._pserial.clear() 

    def open(self):
        if not self._is_open:
            self._pserial = PSerial(this, self.port, self.baudrate)

    def close(self):
        self._is_open = False
        return self._pserial.stop()

    def isOpen(self):
        return self._is_open

class SerialException(Exception):
    pass