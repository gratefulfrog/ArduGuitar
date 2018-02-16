from app import App
from pyb import LED

def doit(expo=None):
    XPin = 'X1'   # x axis pin - ADC required
    YPin = 'X2'   # y axis pin - ADC required
    for i in range(1,5):
        LED(i).off()
        
    app = App(XPin,YPin,expo) if expo else App(XPin,YPin)

    try:
        app.loop()
    except KeyboardInterrupt:
        print('exiting...')
        return
    except Exception as e:
        print (e)

        
