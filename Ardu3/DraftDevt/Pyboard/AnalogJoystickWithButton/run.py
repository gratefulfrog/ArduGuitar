from app import App

from pyb import LED

def doit():
    XPin = 'X11'   # x axis pin - ADC required
    YPin = 'X12'   # y axis pin - ADC required
    PPin = 'X10'   # pushbutton pin - external interrupt required
    led = LED(2)   # green LED
    for i in range(1,5):
        LED(i).off()
        
    app = App(XPin,YPin,PPin,led)

    try:
        app.loop()
    except KeyboardInterrupt:
        print('exiting...')
        return
    except Exception as e:
        print (e)

        
