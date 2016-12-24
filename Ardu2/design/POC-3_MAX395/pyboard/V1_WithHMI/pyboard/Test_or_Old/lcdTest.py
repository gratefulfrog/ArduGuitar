"""Implements a character based lcd connected via PCF8574 on i2c."""

from pyb import Pin, delay, millis
from hardware import LcdDisplayI2C
"""
lcdConfDict = {'rs_pin'      : 'X18',
               'enable_pin'  : 'Y7',
               'd4_pin'      : 'Y8',
               'd5_pin'      : 'A15', #board.P3
               'd6_pin'      : 'A14', #board.P4,
               'd7_pin'      : 'A13', #board.P5,
               'num_lines'   : 2,
               'num_columns' : 16}
"""
lcdConfDict = {'i2c_id'      : 1,
                   'i2c_addr'    : 0x20,
                   'num_lines'   : 2,
                   'num_columns' : 16}
    
lcd = LcdDisplayI2C(lcdConfDict)

def testLCD():
    """
    Test function for verifying basic functionality.
    """
    global lcd
    print('Test started!')
    lcd.setLn(0,'Test started!')
    lcd.setLn(1,'Running test...')
    delay(3000)
    count = 0
    try:
        while True:
            lcd.setLn(0,str(millis() // 1000))
            delay(1000)
            count += 1
    except:
        lcd.setLn(1,'Test Ended!')
        print('Test Ended')


