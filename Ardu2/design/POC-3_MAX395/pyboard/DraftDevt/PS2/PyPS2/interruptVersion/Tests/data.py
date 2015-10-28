"""
>>> is1.lastAction
'r'
>>> is1.co()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'Pin' object is not callable
>>> is1.cv()
1
>>> is1.dv()
1
>>> is1.inData
[0, 
0, 1, 0, 1, 
1, 1, 1, 1, 
1, 1,
 0, 
0, 0, 0, 1, 
0, 0, 0, 0, 
0, 1,
 0, 
0, 1, 0, 0, 
0, 0, 0, 0, 
0, 1,
 0, 
0, 1, 0, 0, 
0, 1, None, None, 
None, None]

data overflow...

so I did some overflow tests by setting the sensitivity to 1...
- overflow values process correctly....

"""

"""
removed the leading init() call
andfound this:
>>> is1.lastAction
'r'
>>> is1.outData
[1, 1, 0, 1, 
 0, 1, 1, 1, 
 1, 1]
EB = poll
ok so far...
>>> is1.inData
[0, 
0, 1, 0, 1, 
1, 1, 1, 1, 
1, 1, 
ACK is ok!
0, 
0, 0, 0, 1, 
1, 1, 0, 1, 
B8 
8 is ok!  
but B???
None, None, 
 None, None, None, None, None, None, None, None, None, None, None, 
 None, None, None, None, None, None, None, None, None, None, None]

>>> is1.bitsExpected
44
>>> is1.inBitCount
20
>>> is1.cv()
1
>>> is1.dv()
1
so both clock and data are released...
why did it stop reading in the middle????
Explain this!
maybe an electrical problem???

doubtful
"""

"""
>>> is1.cv()
1
>>> is1.dv()
1
>>> is1.outData
[1, 1, 0, 1, 0, 1, 1, 1, 1, 1]
That's EB, poll!
>>> is1.bitsExpected
44
that's correct!
>>> is1.inBitCount
40
this failed!
>>> is1.inData
[1, 
0, 0, 0, 0, 
1, 0, 0, 0, 
0, 0, 
1, 
This should have been 0xFA !!! all wrong!

0, 0, 0, 0, 
0, 0, 0, 0, 
0, 1, 
1, 
0, 0, 0, 0, 
0, 0, 0, 0, 
0, 1, 
1, 
1, 1, 1, 1, 
1, 1, None, None, 
None, None]



"""
