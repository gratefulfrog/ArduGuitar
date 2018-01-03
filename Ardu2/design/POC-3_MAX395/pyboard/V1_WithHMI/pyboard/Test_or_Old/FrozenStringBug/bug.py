# bug.py
"""
Usage:
1. Select all the .py files from the root directory!
2. Byte compile them to the frozen part of the firmware and load the firmware to the pyboard.
3. Mound the sd card STAND-ALONE, on the pc
4. Put the Data directory on the sd-card
5. Put the file config_.py from the SD directory on the sd-card
6. Eject the SD card and insert it in the pyboard.
7. connect the pyboard via usb.
8. open a full screen terminal, and run:
   $ screen /dev/ttyACM0
9. at the python prompt, execute the following sequence and obser the results:
>>> import bug
[... messages ...]
>>> sd=bug.getP()  # this creates an instance using only strings from the sd-card as keys to the dictionary
[... messages ...]
>>> frozen=bug.getP(False)  # this creates an instance using strings from the frozen bytecode as keys to the dictionary
[... messages ...]
>>> bug.test(sd)  # see what happens when all strings come from sd-card..
[... messages ...]
dict[p.header[0]]:
 0                   # this means there was no error
>>> bug.test(frozen)  # see what happens when strings from frozen are keys, but other come from sd-card..
[... messages ...]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "bug.py", line 33, in test
KeyError: <value>
>>> 
"""

from Presets import Preset

def getP(sd=True):
    if sd:
        print('returning a Preset instance using config from SD!')
        from config_ import  PyGuitarConf
    else:
        print('returning a Preset instance using config from FLASH!')
        from config import  PyGuitarConf
    c=PyGuitarConf() 
    p=Preset(c)
    return p

def test(p, k=(0,3)):
    dict = p.confDict2RowDict(k,p.presets[k])
    print('dict:\n',dict)
    l = list(dict.keys())
    print('converted to a list:\n', l)
    print('l.index("HorizontalSelector"):\n',l.index("HorizontalSelector"))
    print('l[l.index("HorizontalSelector")]:\n',l[l.index("HorizontalSelector")])
    print('p.header[0]:\n', p.header[0])
    print('p.header[0] == l[l.index("HorizontalSelector")]\n', p.header[0]== l[l.index("HorizontalSelector")])
    print('dict[l[l.index("HorizontalSelector")]]:\n',dict[l[l.index("HorizontalSelector")]])
    print('dict[p.header[0]]:\n',dict[p.header[0]])

"""
>>> import bug
this is csv_ from the sd-card
this is Presets_ the sd-card version, importing csv_ from the sd-card
>>> allSD=bug.getP()
returning a Preset instance using config from SD!
this is config_ from sd-card
creating preset instance from:  /sd/Data/presets.csv
>>> confFrozen=bug.getP(False)
returning a Preset instance using config from FLASH!
creating preset instance from:  /sd/Data/presets.csv
>>> bug.test(allSD)
dict:
 {'CTone': 3, 'ToneRange': 5, 'ATone': 3, 'TREM': 1, 'BVol': 0, 'VIB': 1, 'S': '(|AD)', 'AUX0': 0, 'AUX1': 0, 'AVol': 4, 'CVol': 0, 'BTone': 3, 'MasterVol': 5, 'VerticalSelector': 3, 'HorizontalSelector': 0, 'DVol': 5, 'MasterTone': 3, 'Name': '(0,3)', 'DTone': 3}
converted to a list:
 ['CTone', 'ToneRange', 'ATone', 'TREM', 'BVol', 'VIB', 'S', 'AUX0', 'AUX1', 'AVol', 'CVol', 'BTone', 'MasterVol', 'VerticalSelector', 'HorizontalSelector', 'DVol', 'MasterTone', 'Name', 'DTone']
l.index("HorizontalSelector"):
 14
l[l.index("HorizontalSelector")]:
 HorizontalSelector
p.header[0]:
 HorizontalSelector
p.header[0] == l[l.index("HorizontalSelector")]
 True
dict[l[l.index("HorizontalSelector")]]:
 0
dict[p.header[0]]:
 0
>>> bug.test(confFrozen)
dict:
 {'HorizontalSelector': 0, 'VerticalSelector': 3, 'CTone': 3, 'ToneRange': 5, 'ATone': 3, 'TREM': 1, 'VIB': 1, 'S': '(|AD)', 'BVol': 0, 'AUX0': 0, 'AUX1': 0, 'AVol': 4, 'CVol': 0, 'BTone': 3, 'MasterVol': 5, 'DTone': 3, 'DVol': 5, 'MasterTone': 3, 'Name': '(0,3)'}
converted to a list:
 ['HorizontalSelector', 'VerticalSelector', 'CTone', 'ToneRange', 'ATone', 'TREM', 'VIB', 'S', 'BVol', 'AUX0', 'AUX1', 'AVol', 'CVol', 'BTone', 'MasterVol', 'DTone', 'DVol', 'MasterTone', 'Name']
l.index("HorizontalSelector"):
 0
l[l.index("HorizontalSelector")]:
 HorizontalSelector
p.header[0]:
 HorizontalSelector
p.header[0] == l[l.index("HorizontalSelector")]
 True
dict[l[l.index("HorizontalSelector")]]:
 0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "bug.py", line 33, in test
KeyError: <value>
>>> 
"""

