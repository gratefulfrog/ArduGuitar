#HMItest.py
# some test config for the HMI readboards

"""
pin   color
LCD:
X18  4     brown
X19  6     green
X20  11    yellow
X21  12    blue
X22  13    white
X1   14    orange

LCD Pushbuttons:
X3 Left  orange
X4 Right brown

SPI:
X6 SHCP  blue   (Clock SCK X6)
X5 STCP  orange (latch NSS X5)
X8 DS    yellow  (DI MOSI X8)

Illuminated Pusbuttons
Y12   yellow
X2   orange  (seems like Y11 is broken???)
Y10   blue
Y9    green
------------------------
Usage:
Tests are all integrated into the pushbutton tester!
LCD displays the text, not the sends, as per stdout.

>>> pbTest()
('send:\t0b1000',)
('send:\t0b0',)
('send:\t0b0',)
('send:\t0b0',)
('send:\t0b0',)
yellow pressed!
('send:\t0b1100',)
('send:\t0b0',)
('send:\t0b0',)
('send:\t0b0',)
('send:\t0b0',)
red pressed!
('send:\t0b1110',)
('send:\t0b0',)
('send:\t0b0',)
('send:\t0b0',)
('send:\t0b0',)
blue pressed!
('send:\t0b1111',)
('send:\t0b0',)
('send:\t0b0',)
('send:\t0b0',)
('send:\t0b0',)
green pressed!
('send:\t0b11111111',)
('send:\t0b11111111',)
('send:\t0b11111111',)
('send:\t0b11111111',)
('send:\t0b11111111',)
left pressed!
All ON !!
('send:\t0b0',)
('send:\t0b0',)
('send:\t0b0',)
('send:\t0b0',)
('send:\t0b0',)
right pressed!
All off ...
('send:\t0b11111111',)
('send:\t0b11111111',)
('send:\t0b11111111',)
('send:\t0b11111111',)
('send:\t0b11111111',)
left pressed!
All ON !!
('send:\t0b11111110',)
('send:\t0b11111111',)
('send:\t0b11111111',)
('send:\t0b11111111',)
('send:\t0b11111111',)
green pressed!
"""

from spiMgr import SPIMgr
from debouncePushbutton import DebouncePushbutton
from pyb import Pin, delay, millis
from pyb_gpio_lcd import GpioLcd



############################################################
############### Shift Reg SPI Tests
############################################################

nbShiftRegs = 5
allOn = [255 for i in range(nbShiftRegs)]
allOff = [0 for i in range(nbShiftRegs)]

ledStatus = [0 for i in range(nbShiftRegs)]


yellow = [0,2]
red    = [0,3]
blue   = [0,4]
green  = [0,5]
left = 1
right = 0

sMgr = SPIMgr(True, 'X5')

def testSPI(array=[]):
    global ledStatus
    for i in range(len(array)):
        ledStatus[i] = array[i]
    sMgr.update(ledStatus)

def toggle(elt, array):
    """ phsyical change to array arg
    """
    bit = 1<<elt[1]
    array[elt[0]] ^=bit
    testSPI(array)
    

############################################################
############### Pushbutton tests
############################################################

yellowB = DebouncePushbutton(Pin('Y12',Pin.IN,Pin.PULL_UP),
                             lambda : func('yellow'))

# is pin Y11 defective?
redB = DebouncePushbutton(Pin('X2',Pin.IN,Pin.PULL_UP),
                             lambda : func('red'))
blueB = DebouncePushbutton(Pin('Y10',Pin.IN,Pin.PULL_UP),
                             lambda : func('blue'))
greenB = DebouncePushbutton(Pin('Y9',Pin.IN,Pin.PULL_UP),
                             lambda : func('green'))
leftB = DebouncePushbutton(Pin('X3',Pin.IN,Pin.PULL_UP),
                             lambda : func('left'))
rightB = DebouncePushbutton(Pin('X4',Pin.IN,Pin.PULL_UP),
                            lambda : func('right'))

def pbTest():
    try:
        LCDsend('Start Test!\nAll off ...')
        testSPI(allOff)
        while True:
            for pb in [yellowB, redB, blueB, greenB, leftB, rightB]:
                pb.update()
    except:
        LCDsend('Test ended!\nAll off ...')
        testSPI(allOff)

def func(pb):
    mp = {'yellow' : yellow,
          'red': red,
          'blue' : blue,
          'green' : green,
          'left' : left,
          'right' : right}
    if type(mp[pb])==list :
        LCDsend(pb + ' pressed!')
        toggle(mp[pb],ledStatus)
    elif mp[pb]:
        """
        LCDsend(pb + ' pressed!\nAll ON !!')
        testSPI(allOn)
        """
        LCDsend(pb + ' pressed!\nCycling !!')
        cycleAll()
    else:
        LCDsend(pb + ' pressed!\nAll off ...')
        testSPI(allOff)

def cycleAll():
    vals = [0 for i in range(nbShiftRegs)]
    for i in range(nbShiftRegs):
        for j in range(8):
            vals[i] |= 1<<j
            testSPI(vals)
            delay(100)

############################################################
############### LCD tests
############################################################

lcd = GpioLcd(rs_pin=Pin.board.X18,
              enable_pin=Pin.board.X19,
              d4_pin=Pin.board.X20,
              d5_pin=Pin.board.X21,
              d6_pin=Pin.board.X22,
              d7_pin=Pin.board.X1,
              num_lines=2, num_columns=16)

def LCDsend(msg):
    lcd.clear()  # if not, message scrolls from last cursor point
    lcd.putstr(msg)
    print(msg)

def testLCD():
    """Test function for verifying basic functionality."""
    print("Running testLCD")
    lcd.putstr("It Works!\nSecond Line")
    delay(3000)
    lcd.backlight_off()
    lcd.clear()
    count = 0
    while count<20:
        lcd.move_to(0, 0)
        lcd.putstr(str(millis() // 1000))
        delay(1000)
        count += 1
    return lcd


