#!/usr/local/bin/python3.4
# dictMgr.py

""" Some dictionaries to map user readable symbols into shift reg pins 
and so on...
all the dictionairies are constant and never to be updated programmatically!
"""

from state import *

# shunt configuration (pin, timer, channel, frequency)
shuntConfDict = {'p':'Y1',
                 't':8,
                 'c':1,
                 'f':50000}

# this dictionary maps:
# ((fromCoilName,fromPoleID),(toCoilName,toPoleID)) 
# ->
# (registerID,BitID)
# we assume pole 0 == +pole, and pole 1 == -pole
# so if you want to connect say coil A pole 0 to coil B pole 1 you
# would set register 0 bit 1.
# updated 2015 04 08 to confrom to HW.
# updated 2016 06 06 to integrate HMI LED display

connectionsDict = {(('A',0),('B',0)) : (8,3),  # ok
                   (('A',0),('B',1)) : (8,2),  # ok
                   (('A',0),('C',0)) : (8,1),  # ok
                   (('A',0),('C',1)) : (8,0),  # ok
                   (('A',0),('D',0)) : (8,5),  # ok
                   (('A',0),('D',1)) : (8,6),  # ok
                   (('A',0),('M',0)) : (8,7),  # ok

                   (('A',1),('B',0)) : (7,0),  # ok
                   (('A',1),('B',1)) : (7,1),  # ok
                   (('A',1),('C',0)) : (7,2),  # ok
                   (('A',1),('C',1)) : (7,3),  # ok
                   (('A',1),('D',0)) : (7,5),  # ok
                   (('A',1),('D',1)) : (7,6),  # ok
                   (('A',1),('M',1)) : (7,7),  # ok
                   
                   (('B',0),('C',0)) : (6,3),  # ok
                   (('B',0),('C',1)) : (6,2),  # ok
                   (('B',0),('D',0)) : (6,1),  # ok
                   (('B',0),('D',1)) : (6,0),  # ok
                   (('B',0),('M',0)) : (6,7),  # ok

                   (('B',1),('C',0)) : (6,5),  # ok
                   (('B',1),('C',1)) : (5,2),  # ok
                   (('B',1),('D',0)) : (5,3),  # ok
                   (('B',1),('D',1)) : (5,1),  # ok
                   (('B',1),('M',1)) : (6,4),  # ok

                   (('C',0),('D',0)) : (5,7),  # ok
                   (('C',0),('D',1)) : (5,0),  # ok
                   (('C',0),('M',0)) : (6,6),  # ok
                   
                   (('C',1),('D',0)) : (8,4),  # ok
                   (('C',1),('D',1)) : (5,6),  # ok
                   (('C',1),('M',1)) : (5,5),  # ok

                   (('D',0),('M',0)) : (7,4),  # ok

                   (('D',1),('M',1)) : (5,4)}  # ok


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
vtrDict =      {'A': {State.Vol:       (((10,2),),
                                        ((10,3),(4,7)),
                                        ((10,4),(4,6)),
                                        ((10,5),(4,6),(4,7)),
                                        ((10,6),(4,5)),
                                        ((10,7),(4,5),(4,7))),
                      State.Tone:      ((( 9,6),(4,4)),
                                        (( 9,5),(4,3)),
                                        (( 9,4),(4,3),(4,4)),
                                        ((10,0),(4,2)),
                                        ((10,1),(4,2),(4,4))), 
                      State.ToneRange: (( 9,7),), # tone on/off
                      State.Inverter:  (((9,0),(9,3)), #  This logic changed with MAX395s
                                        ((9,1),(9,2)))},  # HMI OK
                'B': {State.Vol:       (((12,2),),
                                        ((12,3),(4,1)),
                                        ((12,4),(4,0)),
                                        ((12,5),(4,0),(4,1)),
                                        ((12,6),(3,7)),
                                        ((12,7),(3,7),(4,1))),
                      State.Tone:      (((11,6),(3,6)),
                                        ((11,5),(3,5)),
                                        ((11,4),(3,5),(3,6)),
                                        ((12,0),(3,4)),
                                        ((12,1),(3,4),(3,6))),
                      State.ToneRange: ((11,7),), # tone on/off
                      State.Inverter:  (((11,0),(11,3)), #  This logic changed with MAX395s
                                        ((11,1),(11,2)))},  # HMI OK
                'C': {State.Vol:       (((14,2),),
                                        ((14,3),(3,3)),
                                        ((14,4),(3,2)),
                                        ((14,5),(3,2),(3,3)),
                                        ((14,6),(3,1)),
                                        ((14,7),(3,1),(3,3))),
                      State.Tone:      (((13,6),(3,0)),
                                        ((13,5),(2,7)),
                                        ((13,4),(2,7),(3,0)),
                                        ((14,0),(2,6)),
                                        ((14,1),(2,6),(3,0))),
                      State.ToneRange: ((13,7),), # tone on/off
                      State.Inverter:  (((13,0),(13,3)), #  This logic changed with MAX395s
                                        ((13,1),(13,2)))},  # HMI OK
                'D': {State.Vol:       (((16,2),),
                                        ((16,3),(2,5)),
                                        ((16,4),(2,4)),
                                        ((16,5),(2,4),(2,5)),
                                        ((16,6),(2,3)),
                                        ((16,7),(2,3),(2,5))),
                      State.Tone:      (((15,6),(2,2)),
                                        ((15,5),(2,1)),
                                        ((15,4),(2,1),(2,2)),
                                        ((16,0),(2,0)),
                                        ((16,1),(2,0),(2,2))),
                      State.ToneRange: ((15,7),), # tone on/off
                      State.Inverter:  (((15,0),(15,3)), #  This logic changed with MAX395s
                                        ((15,1),(15,2)))},  # HMI OK
                'M': {State.Vol:       (((17,2),),
                                        ((17,3),(1,7)),
                                        ((17,4),(1,6)),
                                        ((17,5),(1,6),(1,7)),
                                        ((17,6),(1,5)),
                                        ((17,7),(1,5),(1,7))),
                      State.Tone:      (((18,5),(1,4)),
                                        ((18,6),(1,3)),
                                        ((18,7),(1,3),(1,4)),
                                        ((17,0),(1,2)),
                                        ((17,1),(1,2),(1,4))),
                      State.ToneRange: (((18,4),(1,1)),
                                        ((18,3),(1,0)),
                                        ((18,2),(1,0),(1,1)),
                                        ((18,1),(0,7)),
                                        ((18,0),(0,7),(1,1)))},  # HMI OK
                'PB':{State.Yellow:    ((0,4),),
                      State.Red:       ((0,3),),
                      State.Tremolo:   ((0,6),),
                      State.Vibrato:   ((0,5),)},   # HMI OK
                'UNUSED':{State.l0:    ((0,2),),
                          State.l1:    ((0,1),),
                          State.l2:    ((0,0),)}}   # HMI OK


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
# update 2016 06 06 to integrate HI LED display

maskingDict = {'A' : {State.Vol         : (( 10,0B00000011), (  4,0B00011111)),
                      State.Tone        : ((  9,0B10001111), ( 10,0B11111100),( 4,0B11100011)),
                      State.ToneRange   : ((  9,0B01111111),),
                      State.Inverter    : ((  9,0B11110000),)},    # ok OK   
               'B' : {State.Vol         : (( 12,0B00000011), (  4,0B11111100),( 3,0B01111111)),
                      State.Tone        : (( 11,0B10001111), ( 12,0B11111100),( 3,0B10001111)),
                      State.ToneRange   : (( 11,0B01111111),),
                      State.Inverter    : (( 11,0B11110000),)},    # ok OK     
               'C' : {State.Vol         : (( 14,0B00000011), (  3,0B11110001)),
                      State.Tone        : (( 13,0B10001111), ( 14,0B11111100),( 3,0B11111110),( 2,0B00111111)),
                      State.ToneRange   : (( 13,0B01111111),),
                      State.Inverter    : (( 13,0B11110000),)},    # ok OK 
               'D' : {State.Vol         : (( 16,0B00000011), (  3,0B11000111)),
                      State.Tone        : (( 15,0B10001111), ( 16,0B11111100),( 2,0B11111000)),
                      State.ToneRange   : (( 15,0B01111111),),
                      State.Inverter    : (( 15,0B11110000),)},    # ok OK
               'M' : {State.Vol         : (( 17,0B00000011), ( 1,0B00011111)),
                      State.Tone        : (( 17,0B11111100), (18,0B00011111),( 1,0B11100011)),
                      State.ToneRange   : (( 18,0B11100000), ( 1,0B11111100),( 0,0B01111111))},
               'PB': {State.Yellow      : ((  0,0B11101111),),
                      State.Red         : ((  0,0B11110111),),
                      State.Tremolo     : ((  0,0B10111111),),
                      State.Vibrato     : ((  0,0B11011111),)}}   # ok OK
