# adc.py

from pyb import ADC

class VoltageDividerPot:

    def __init__(self,pin,rm=None):
        """
        instance creation, args:
        * pin is a pyb.Pin object as per: pyb.Pin('X1', pyb.Pin.ANALOG)
        * an optional RMap instance to provide a reading in the proper range
        """
        self.a = ADC(pin)
        if rm:
            self.v = lambda x: rm.v(x)
        else:
            self.v = lambda x:x

    def update(self):
        """
        returns the current reading as per config
        """
        return self.v(self.a.read())
            
