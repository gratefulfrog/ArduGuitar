#!/usr/local/bin/python3.4
# spiMgr.py

"""
The pyboard SPI class gives details:
http://docs.micropython.org/en/latest/library/pyb.SPI.html

the NSS pin is NOT used by the SPI driver and is free for other use.

SPI(1) is on the X position: 
(NSS, SCK, MISO, MOSI) = (X5, X6, X7, X8) = (PA4, PA5, PA6, PA7)

SPI(2) is on the Y position: 
(NSS, SCK, MISO, MOSI) = (Y5, Y6, Y7, Y8) = (PB12, PB13, PB14, PB15)

>>> pyb.freq()
(168000000, 168000000, 42 000 000, 84000000)
(sysclk: frequency of the CPU
 hclk: frequency of the AHB bus, core memory and DMA
 pclk1: frequency of the APB1 bus
 pclk2: frequency of the APB2 bus
)

"""

def char2bit(c):
  return 1 if c == '1' else 0

class ad75019SPIMgr:
  def __init__(self,spiOnX,sPinID):
    import pyb 
    self.spi=pyb.SPI(1 if spiOnX else 2,
                     pyb.SPI.MASTER,
                     prescaler=32 if spiOnX else 16,
                     polarity=0,
                     phase=0,
                     bits=8,
                     firstbit=pyb.SPI.MSB,
                     ti=False, crc=None)
    self.SS = pyb.Pin(sPinID, pyb.Pin.OUT_PP)
    self.SS.high()

  def beginTransaction(self):
    self.SS.high()
        
  def endTransaction(self):
    self.SS.low()
    self.SS.high()

  def sendBytes(self,b):  # send  a single byte or a vector of bytes over SPI
    self.beginTransaction()
    self.spi.send(b)
    self.endTransaction()

  def sendString(self,s):
    """take a string containing only '0' and '1', convert
    it to a byte array and send it.
    The string must be of multiple of 8 in length or it won't fit into bytes!
    """
    buf = bytearray(len(s)//8)
    for si in range(len(s)):
      i= si//8
      buf[i] = (buf[i]<<1)|char2bit(s[si])
    self.beginTransaction()
    self.spi.send(buf)
    self.endTransaction()

