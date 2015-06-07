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
connectionsDict = {(('A',0),('B',0)) : (0,0),
                   (('A',0),('B',1)) : (0,1),
                   (('A',0),('C',0)) : (0,2),
                   (('A',0),('C',1)) : (0,3),
                   (('A',0),('D',0)) : (0,4),
                   (('A',0),('D',1)) : (0,5),
                   (('A',0),('M',0)) : (0,6),

                   (('A',1),('B',0)) : (0,7),
                   (('A',1),('B',1)) : (1,0),
                   (('A',1),('C',0)) : (1,1),
                   (('A',1),('C',1)) : (1,2),
                   (('A',1),('D',0)) : (1,3),
                   (('A',1),('D',1)) : (1,4),
                   (('A',1),('M',1)) : (1,5),
                   
                   (('B',0),('C',0)) : (1,6),
                   (('B',0),('C',1)) : (1,7),
                   (('B',0),('D',0)) : (2,0),
                   (('B',0),('D',1)) : (2,1),
                   (('B',0),('M',0)) : (2,2),

                   (('B',1),('C',0)) : (2,3),
                   (('B',1),('C',1)) : (2,4),
                   (('B',1),('D',0)) : (2,5),
                   (('B',1),('D',1)) : (2,6),
                   (('B',1),('M',1)) : (2,7),

                   (('C',0),('D',0)) : (3,0),
                   (('C',0),('D',1)) : (3,1),
                   (('C',0),('M',0)) : (3,2),
                   
                   (('C',1),('D',0)) : (3,3),
                   (('C',1),('D',1)) : (3,4),
                   (('C',1),('M',1)) : (3,5),

                   (('D',0),('M',0)) : (3,6),

                   (('D',1),('M',1)) : (3,7)}


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
vtrDict =      {'A': {State.Vol:       ((4,0),
                                        (4,1),
                                        (4,2),
                                        (4,3),
                                        (4,4),
                                        (4,5)),
                      State.Tone:      ((4,6),
                                        (4,7),
                                        (5,0),
                                        (5,1),
                                        (5,2)), 
                      State.ToneRange: ((5,3),), # tone on/off
                      State.Inverter:  ((5,4),
                                        (5,5))},
                'B': {State.Vol:       ((5,6),
                                        (5,7),
                                        (6,0),
                                        (6,1),
                                        (6,2),
                                        (6,3)),
                      State.Tone:      ((6,4),
                                        (6,5),
                                        (6,6),
                                        (6,7),
                                        (7,0)),
                      State.ToneRange: ((7,1),), # tone on/off
                      State.Inverter:  ((7,2),
                                        (7,3))},
                'C': {State.Vol:       ((7,4),
                                        (7,5),
                                        (7,6),
                                        (7,7),
                                        (8,0),
                                        (8,1)),
                      State.Tone:      ((8,2),
                                        (8,3),
                                        (8,4),
                                        (8,5),
                                        (8,6)),
                      State.ToneRange: ((8,7),), # tone on/off
                      State.Inverter:  ((9,0),
                                        (9,1))},
                'D': {State.Vol:       ((9,2),
                                        (9,3),
                                        (9,4),
                                        (9,5),
                                        (9,6),
                                        (9,7)),
                      State.Tone:      ((10,0),
                                        (10,1),
                                        (10,2),
                                        (10,3),
                                        (10,4)),
                      State.ToneRange: ((10,5),), # tone on/off
                      State.Inverter:  ((10,6),
                                        (10,7))},
                'M': {State.Vol:       ((11,0),
                                        (11,1),
                                        (11,2),
                                        (11,3),
                                        (11,4),
                                        (11,5)),
                      State.Tone:      ((11,6),
                                        (11,7),
                                        (12,0),
                                        (12,1),
                                        (12,2)),
                      State.ToneRange: ((12,3),
                                        (12,4),
                                        (12,5),
                                        (12,6),
                                        (12,7))}}
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

maskingDict = {'A' : {State.Vol         : (( 4,0B11000000),),
                      State.Tone        : (( 4,0B00111111),( 5,0B11111000)),
                      State.ToneRange   : (( 5,0B11110111),),
                      State.Inverter    : (( 5,0B11001111),)},    # ok
               'B' : {State.Vol         : (( 5,0B00111111), ( 6,0B11110000)),
                      State.Tone        : (( 6,0B00001111), ( 7,0B11111110)),
                      State.ToneRange   : (( 7,0B11111101),),
                      State.Inverter    : (( 7,0B11110011),)},    # ok
               'C' : {State.Vol         : (( 7,0B00001111), ( 8,0B11111100)),
                      State.Tone        : (( 8,0B10000011),),
                      State.ToneRange   : (( 8,0B01111111),),
                      State.Inverter    : (( 9,0B11111100),)},    # ok
               'D' : {State.Vol         : (( 9,0B00000011),),
                      State.Tone        : ((10,0B11100000),),
                      State.ToneRange   : ((10,0B11011111),), 
                      State.Inverter    : ((10,0B00111111),)},   # ok
               'M' : {State.Vol         : ((11,0B11000000),),
                      State.Tone        : ((11,0B00111111), (12,0B11111000)),
                      State.ToneRange   : ((12,0B00000111),)}}   # ok
