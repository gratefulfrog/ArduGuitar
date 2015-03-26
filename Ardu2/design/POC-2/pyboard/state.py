#!/usr/local/bin/python3.4
# state.py 

class State:
	# SPI state for pyboard setup
	# define the latching pin
	spiLatchPinName = 'X5'
	# say which side of the pyboard are we using
	spiOnX = True

	off = None
	l0  = 0
	l1  = 1
	l2  = 2
	l3  = 3
	l4  = 4
	l5  = 5
	
	Inverter  = -1
	Vol	  = -2
	Tone	  = -3
	ToneRange = -4
	
	coils = ['A','B','C','D','M']
	poles = []
	
	def __init__(self):
		for c in State.coils:
			State.poles += [(c,0),]
			State.poles += [(c,1),]
