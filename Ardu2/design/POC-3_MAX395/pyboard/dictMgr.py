#!/usr/local/bin/python3.4
# dictMgr.py

""" Some dictionaries to map user readable symbols into shift reg pins 
and so on...
all the dictionairies are constant and never to be updated programmatically!
"""

from state import *

# this dictionary maps:
# ((fromCoilName,fromPoleID),(toCoilName,toPoleID)) 
# ->
# (registerID,BitID)
# we assume pole 0 == +pole, and pole 1 == -pole
# so if you want to connect say coil A pole 0 to coil B pole 1 you
# would set register 0 bit 1.
# updated 2015 04 08 to confrom to HW.
connectionsDict = {(('A',0),('B',0)) : (3,3),  # ok
                   (('A',0),('B',1)) : (3,2),  # ok
                   (('A',0),('C',0)) : (3,1),  # ok
                   (('A',0),('C',1)) : (3,0),  # ok
                   (('A',0),('D',0)) : (3,5),  # ok
                   (('A',0),('D',1)) : (3,6),  # ok
                   (('A',0),('M',0)) : (3,7),  # ok

                   (('A',1),('B',0)) : (2,0),  # ok
                   (('A',1),('B',1)) : (2,1),  # ok
                   (('A',1),('C',0)) : (2,2),  # ok
                   (('A',1),('C',1)) : (2,3),  # ok
                   (('A',1),('D',0)) : (2,5),  # ok
                   (('A',1),('D',1)) : (2,6),  # ok
                   (('A',1),('M',1)) : (2,7),  # ok
                   
                   (('B',0),('C',0)) : (1,3),  # ok
                   (('B',0),('C',1)) : (1,2),  # ok
                   (('B',0),('D',0)) : (1,1),  # ok
                   (('B',0),('D',1)) : (1,0),  # ok
                   (('B',0),('M',0)) : (1,7),  # ok

                   (('B',1),('C',0)) : (1,5),  # ok
                   (('B',1),('C',1)) : (0,2),  # ok
                   (('B',1),('D',0)) : (0,3),  # ok
                   (('B',1),('D',1)) : (0,1),  # ok
                   (('B',1),('M',1)) : (1,4),  # ok

                   (('C',0),('D',0)) : (0,7),  # ok
                   (('C',0),('D',1)) : (0,0),  # ok
                   (('C',0),('M',0)) : (1,6),  # ok
                   
                   (('C',1),('D',0)) : (3,4),  # ok
                   (('C',1),('D',1)) : (0,6),  # ok
                   (('C',1),('M',1)) : (0,5),  # ok

                   (('D',0),('M',0)) : (2,4),  # ok

                   (('D',1),('M',1)) : (0,4)}  # ok


# this dictionary maps coilName
# Volume, 
# Tone, 
# ToneRange, 
# Inverter information as follows:
#
# CoilName
# ->
# a dictionary of vtri registers and bits
# in this second dictionary the keys:
# State.Vol, State.Tone, State.ToneRange, State.Inverter
# return each a list of tuples that correspond to the levels from
# the State Class
# Note that this enables all of V T R I to have a value or be Off!
# Off means none of the bits are set.
vtrDict =      {'A': {State.Vol:       ((5,2),
                                        (5,3),
                                        (5,4),
                                        (5,5),
                                        (5,6),
                                        (5,7)),
                      State.Tone:      ((4,6),
                                        (4,5),
                                        (4,4),
                                        (5,0),
                                        (5,1)), 
                      State.ToneRange: ((4,7),), # tone on/off
                      State.Inverter:  (((4,0),(4,3)), #  This logic changed with MAX395s
                                        ((4,1),(4,2)))},
                'B': {State.Vol:       ((7,2),
                                        (7,3),
                                        (7,4),
                                        (7,5),
                                        (7,6),
                                        (7,7)),
                      State.Tone:      ((6,6),
                                        (6,5),
                                        (6,4),
                                        (7,0),
                                        (7,1)), 
                      State.ToneRange: ((6,7),), # tone on/off
                      State.Inverter:  (((6,0),(6,3)), #  This logic changed with MAX395s
                                        ((6,1),(6,2)))},

                'C': {State.Vol:       ((9,2),
                                        (9,3),
                                        (9,4),
                                        (9,5),
                                        (9,6),
                                        (9,7)),
                      State.Tone:      ((8,6),
                                        (8,5),
                                        (8,4),
                                        (9,0),
                                        (9,1)), 
                      State.ToneRange: ((8,7),), # tone on/off
                      State.Inverter:  (((8,0),(8,3)), #  This logic changed with MAX395s
                                        ((8,1),(8,2)))},
                'D': {State.Vol:       ((11,2),
                                        (11,3),
                                        (11,4),
                                        (11,5),
                                        (11,6),
                                        (11,7)),
                      State.Tone:      ((10,6),
                                        (10,5),
                                        (10,4),
                                        (11,0),
                                        (11,1)), 
                      State.ToneRange: ((10,7),), # tone on/off
                      State.Inverter:  (((10,0),(10,3)), #  This logic changed with MAX395s
                                        ((10,1),(10,2)))},
                'M': {State.Vol:       ((12,7),
                                        (12,6),
                                        (12,5),
                                        (12,4),
                                        (12,3),
                                        (12,2)),
                      State.Tone:      ((13,5),
                                        (13,6),
                                        (13,7),
                                        (12,0),
                                        (12,1)),
                      State.ToneRange: ((13,4),
                                        (13,3),
                                        (13,2),
                                        (13,1),
                                        (13,0))}}
# this dictionary maps coilName
# Volume, 
# Tone, 
# ToneRange, 
# Inverter 
# to provide the masking needed when updating the corresponding field.
# by masking I mean When you set the volume of coil 'A' to say 2, first
# you must ensure that all the other volume bits of coil 'A' are set to
# zero.
# you do this by performing an AND with all the reg,bits pairs that are returned
# after a lookup of ['A'][State.Vol]
# maskingDict lookups are:
# maskingDict[CoilName][State.Vol|State.Tone|State.ToneRange| State.Inverter]
# but note that coil 'M' has no State.Inverter entry and if so indexed
# will return an error
# updated 2015 04 08 to conform to HW updates

maskingDict = {'A' : {State.Vol         : (( 5,0B00000011),),
                      State.Tone        : (( 4,0B10001111),( 5,0B11111100)),
                      State.ToneRange   : (( 4,0B01111111),),
                      State.Inverter    : (( 4,0B11110000),)},    # ok      
               'B' : {State.Vol         : (( 7,0B00000011),),
                      State.Tone        : (( 6,0B10001111),( 7,0B11111100)),
                      State.ToneRange   : (( 6,0B01111111),),
                      State.Inverter    : (( 6,0B11110000),)},    # ok      
               'C' : {State.Vol         : (( 9,0B00000011),),
                      State.Tone        : (( 8,0B10001111),( 9,0B11111100)),
                      State.ToneRange   : (( 8,0B01111111),),
                      State.Inverter    : (( 8,0B11110000),)},    # ok      
               'D' : {State.Vol         : ((11,0B00000011),),
                      State.Tone        : ((10,0B10001111),( 11,0B11111100)),
                      State.ToneRange   : ((10,0B01111111),),
                      State.Inverter    : ((10,0B11110000),)},    # ok      
               'M' : {State.Vol         : ((12,0B00000011),),
                      State.Tone        : ((12,0B11111100), (13,0B00011111)),
                      State.ToneRange   : ((13,0B11100000),)}}   # ok
