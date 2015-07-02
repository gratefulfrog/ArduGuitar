# illuminator.py
# support leds or other pin controlled lights

class Illuminator:
    """ Usage:
    >> pinId = 'X1
    >> i = Illuminator(Pin(pinID, Pin.OUT_PP))
    >> i.value()
    0
    >> i.on()
    >> i.value()
    1
    >> i.off()
    >> i.value()
    0
    -----
    wiring:
    from pin to LED+ 
    from LED- to current limiting resistor
    from current limiting resistor to ground
    """
    def __init__(self,pin):
        """create an instance of a LED connected to the 
        pin provided.
        Pins should be configured as Pin('X1', Pin.OUT_PP)
        """
        self.p = pin
        self.off()
        
    def off(self):
        """ set pin to low
        """
        self.p.low()

    def on(self):
        """ set pin to high
        """
        self.p.high()

    def value(self):
        """ returns 0 or 1 depending on state of pin
        """
        return self.p.value()
        
    def __repr__(self):
        return 'Illuminator:' + \
            '\n\tpin:\t' + str(self.p) +\
            '\n\tvalue:\t' + str(self.p.value())  + '\n'                    
