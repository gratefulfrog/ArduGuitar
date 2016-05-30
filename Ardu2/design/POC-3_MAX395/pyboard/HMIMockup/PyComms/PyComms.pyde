
from PyboardMgr import PyboardMgr 

# for the Pyguitar project
seq1 = ['from app import App',
        'from state import State',
        'a=App()',
        'a.showConfig()',
        "a.set('A',State.Vol,State.l5)",
        "a.set('A',State.Inverter,State.l0)",
        "a.connect('A',0,'B',1)",
        'a.x()',
        "a.loadConfig('nbp')",
        'a.showConfig()'
        ]
seqTest = ['from testClass import TestClass',
        't=TestClass()',
        't.sayHello()'
        ]

def setup():
    p = PyboardMgr()
    print(p.send(seqTest))
    #print(p.doBlink())
    exit()