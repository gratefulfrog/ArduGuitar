# interpreter.py
# interprets ps2 device messages
# provides somre routines to make the messages human readable and or processable
"""
Usage:
User level calls:
1. i11s(bits, res=[]):
   This is the top level call to interpret the bits read from the ps/2 device.
   The bits are stripped of start and end, then sent to the i9 function to get 
   interpreted.
   the return is a list of the results of the i9 interpretation
2. deviceResponse(tup):
   Returns the string version of the command in the tuple, uses the global dictionary 'd'
   to find it.
3. interpretPollPayload(tups):
   Takes the 3 last tuples from the interpretation of the reply to a poll and 
   returns the tuple (deltaA, deltaY) where the values are signed and may be
   None if an overlfow was detected by the device.

Internal calls:
1. i9(m):
   Takes the 9 bits from the 11 bit frame stripped, calculates the numerical value and checks
   the negative parity.
   Returns a 3-tuple (hex-string, decimal, parityOk)

Globals:
1. d
   A dictionary, keyed on numerical values, with values as strings corresponding to the 
   possible device response.
2. h
   A dictionary of possible host commands, currently commented out, for documentation use
   only.
"""

d = {0xFA: 'ACK',
     0xAA: 'BAT',
     0xFE: 'RESEND',
     0xFC: 'ERROR',
     0x00: 'ID'}
"""
this dictionary is unused, it contains all the host commands.
h = {0xFF : 'Reset',
     # The mouse responds to this command with "acknowledge" (0xFA) then enters reset mode.

     0xFE : 'Resend',
     # The host sends this command whenever it receives invalid data from the mouse.
     # The mouse responds by resending the last packet it sent to the host. If the mouse
     # responds to the "Resend" command with another invalid packet, the host may either
     # issue another "Resend" command, issue an "Error" (0xFC) command, cycle the
     # mouse's power supply to reset the mouse, or it may inhibit communication
     # (by bringing the clock line low). This command is not buffered, which means
     # "Resend" will never be sent in response to the "Resend" command.

     0xF6 : 'Set Defaults',
     # The mouse responds with "acknowledge" (0xFA) then loads the following values:
     # Sampling rate = 100,
     # resolution = 4 counts/mm,
     # Scaling = 1:1,
     # data reporting = disabled.
     # The mouse then resets its movement counters and enters stream mode.

     0xF5 : 'Disable Data Reporting',
     # The mouse responds with "acknowledge" (0xFA) then disables
     # data reporting and resets its movement counters. This only
     # affects data reporting in stream mode and does not disable
     # sampling. Disabled stream mode functions the same as remote mode.

     0xF4 : 'Enable Data Reporting', # The mouse responds with "acknowledge" (0xFA)
     # then enables data reporting and resets its movement counters. This command
     # may be issued while the mouse is in remote mode, but it will only
     # affect data reporting in stream mode.

     0xF3 : 'Set Sample Rate', # The mouse responds with "acknowledge" (0xFA)
     # then reads one more byte from the host. The mouse saves this byte as the
     # new sample rate. After receiving the sample rate, the mouse again responds
     # with "acknowledge" (0xFA) and resets its movement counters. Valid sample
     # rates are 10, 20, 40, 60, 80, 100, and 200 samples/sec.

     0xF2 : 'Get Device ID',
     # The mouse responds with "acknowledge" (0xFA) followed by its device
     # ID (0x00 for the standard PS/2 mouse). The mouse should also reset its movement counters.

     0xF0 : 'Set Remote Mode',
     # The mouse responds with "acknowledge" (0xFA) then resets its
     # movement counters and enters remote mode.

     0xEE : 'Set Wrap Mode', # The mouse responds with "acknowledge" (0xFA)
     # then resets its movement counters and enters wrap mode.

     0xEC : 'Reset Wrap Mode', # The mouse responds with "acknowledge" (0xFA)
     # then resets its movement counters and enters the mode it was in
     # prior to wrap mode : (stream mode or remote mode).

     0xEB : 'Read Data', # The mouse responds with "acknowledge" (0xFA) then
     # sends a movement data packet. This is the only way to read data
     # in remote mode. After the data packet has successfully been sent,
     # the mouse resets its movement counters.

     0xEA : 'Set Stream Mode', # The mouse responds with "acknowledge" (0xFA)
     # then resets its movement counters and enters stream mode.

     0xE9 : 'Status Request',
     # The mouse responds with "acknowledge" (0xFA) then sends
     # a 3-byte status packet (then resets its movement counters):  

     0xE8 :'Set Resolution',
     # The mouse responds with "acknowledge" (0xFA) then reads one byte
     # from the host and again responds with "acknowledge" (0xFA) then
     # resets its movement counters. The byte read from the host determines the resolution

     0xE7 :'Set Scaling 2:1',
     # The mouse responds with "acknowledge" (0xFA) then enables 2:1 scaling.

     0xE6 : 'Set Scaling 1:1'
     # The mouse responds with "acknowledge" (0xFA) then enables 1:1 scaling. 
     }
"""
    
def i9(m):
    """
    return tuple:  ( hex(value), decimal value, True if parity ok )
    argument should be a 9 elt list:
    1st 8 elts are the bits of a byte least significant first,
    the last is the odd parity bit
    """
    by = m[0:8]
    py = m[8]
    p=1
    s=0
    for i in range(8):
        s+=by[i]<<i
        p^=by[i]
    return(hex(s),s,p==py)
 
def i11s(ms,res=[]):
    """ interpret a list of bits, 11 by 11 coming from a ps/2
    device, bits are low order first
    start bit
    a byte of payload
    odd parity bit
    stop bit
    the start and stop bits are ignored in this interpretation
    returns a list of i9 results
    """
    if not ms:
        return res
    else:
        return i11s(ms[11:],res + [i9(ms[1:10])])

def deviceResponse(tup):
    """ lookup the value in dictionary
    """
    return d[tup[1]]

def interpretPollPayload(tups):
    """
    tups are the infobyte, x, y
    return [x,y] where x,y could be None if overlow
    """
    mask = 0b0101
    ntups = [t[1] for t in tups]
    info = ntups[0] >> 4
    func = lambda i,b: b if not i else None if i>> 1 else b-256
    res = []
    for indx in range(2):
        res += [func(info >> indx & mask, ntups[indx+1])]
    return res


"""
def negate(tup):
    ''' replies with a negated 2-tuple:
    (hex(s2complement(v))), s2complement(v))
    '''
    val = 256-tup[1]
    return (hex(val),val)

# testdata
m = [0] + [1 for i in range(10)]
m += m

# test poll reply should give [13,-2]
pp = [0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1,
     #0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1,
      0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, # bad  y 
      0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 
      0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1]

dd = [0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1,
      0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1,
      0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1,
      0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1]
"""
