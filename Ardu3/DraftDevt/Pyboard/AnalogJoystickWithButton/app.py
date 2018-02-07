import time
from joystick import JoyStick

class App:
    
    def __init__(self,xp,yp,pp,ld):
        self.displayDelta  = 200  # ms
        self.led = ld
        self.led.off()
        try:
            self.js = JoyStick(xp,yp,pp, self.onButton)
            print('Starting up...')
        except Exception as e:
            print(e)
            print('JoyStick creation failed!')

    def onButton(self):
        self.led.toggle()
        print('\nPush Button!\n')
            
    def loop(self):
        lastDisplayTime = time.ticks_ms()
        while True:
            self.js.checkPB()
            now = time.ticks_ms()
            if now - lastDisplayTime > self.displayDelta:
                lastDisplayTime = now
                line = 'X: ' + str(self.js.readX()) + '  Y: ' + str(self.js.readY())
                print(line)


        
        

