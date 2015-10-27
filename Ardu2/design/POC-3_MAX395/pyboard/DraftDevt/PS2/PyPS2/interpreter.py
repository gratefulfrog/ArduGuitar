# interpreter.py
# interprets ps2 device messages

d = {0xFF:'ACK',
     0xFA: 'BAT',
     0xFE: 'RESEND',
     0xFC: 'ERROR'}

def i9(m):
    """
    return the (hex(value), decimal value,True if parity ok)
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
    """
    if not ms:
        return res
    else:
        return i11s(ms[11:],res + [i9(ms[1:10])])

def negate(tup):
    """ relies with a negated 2-tuple:
    (hex(s2complement(v))), s2complement(v))
    """
    val = 256-tup[1]
    return (hex(val),val)

def deviceResponse(tup):
    """ lookup the value in dictionary
    """
    return d[tup[1]]



# testdata
m = [0] + [1 for i in range(10)]
m += m
