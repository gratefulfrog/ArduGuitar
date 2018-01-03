# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import pyb
#pyb.main('main.py') # main script to run after this one
#pyb.usb_mode('CDC+MSC') # act as a serial and a storage device
#pyb.usb_mode('CDC+HID') # act as a serial device and a mouse
pyb.LED(3).on()
pyb.delay(2000)
pyb.LED(4).on()
pyb.LED(3).off()
sw = pyb.Switch()
if sw():
    pyb.usb_mode('CDC+MSC')
    pyb.main('debug_app.py')
else:
    pyb.usb_mode('CDC+HID')
    pyb.main('normal_app.py')
pyb.LED(4).off()
