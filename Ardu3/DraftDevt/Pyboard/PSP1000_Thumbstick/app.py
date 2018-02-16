import time
from thumbstick import ThumbStick

class App:
    
    def __init__(self,xp,yp,expo=None):
        self.displayDelta  = 200  # ms
        self.js=None
        try:
            self.js = ThumbStick(xp,yp,expo) if expo else ThumbStick(xp,yp) 
            print('Starting up...')
        except Exception as e:
            print(e)
            print('ThumbStick creation failed!')
            
    def loop(self):
        lastDisplayTime = time.ticks_ms()
        while True:
            now = time.ticks_ms()
            if now - lastDisplayTime > self.displayDelta:
                lastDisplayTime = now
                line = 'X: ' + str(round(self.js.readX())) + '  Y: ' + str(round(self.js.readY()))
                print(line)


        
        

