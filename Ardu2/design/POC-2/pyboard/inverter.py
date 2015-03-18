#!/usr/bin/python3

from state import State

def testF(x):
    print('testF called with: ' + str(x))

class Inverter:
    def __init__(self, setFunc, initialState=State.Inverter.off):
        self.setFunc = setFunc
        self.state = initialState
        self.setFunc(initialState)

    def setState(self, state):
        """update internal state and call stateFunc on it
        """
        self.state = state
        self.setFunc(state)

    def __repr__(self):
        return 'Inverter:\n\tstate: ' + \
            str(self.state) + '\n\tsetFunc: ' + str(self.setFunc)
    
