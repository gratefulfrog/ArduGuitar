# whoFuncs.py
# test to see if we can have static class member as list of methods
# answer is yes, but the methods must be defined before the static
# member variables.
# it works
"""
$ micropython 
Micro Python  on 2015-05-11; linux version
>>> from whoFuncs import *
>>> t=T()
>>> t.apfun(T.whoFuncs[0])
<T object at 797af300>
f1
>>> t.apfun(T.whoFuncs[1])
<T object at 797af300>
f2
>>> t.apfun(T.whoFuncs[2])
<T object at 797af300>
f3 
>>> t.apfun(T.whoFuncs[3])
Thing.g
"""
import thing

class T:

    # some random methods
    def f1(self):
        print(self)
        print('f1')
    def f2(self):
        print(self)
        print('f2')
    def f3(self):
        print(self)
        print('f3')

    # a static class variable containing the methods
    whoFuncs = (f1,f2,f3,thing.Thing.g)

    def __init__(self):
        self.thing = thing.Thing()
    
    def f1(self):
        print('f1')
    def f2(self):
        print('f2')
    def f3(self):
        print('f3')

    # the instance method where the instance method is applied via
    # derefence from the constant class variable 
    def apfun(self,f):
        f(self)
        
