def encode( sender, payload):
    highBits =  sender<<8
    return (highBits | 0xFF & (payload if payload >=0 else 256+payload))

def decode(msg):
    sender = msg>>8
    payload = msg & 0xFF
    print(payload)
    if payload > 127:
        payload = payload-256
    return (sender,payload)

def setup():
    "print(-1&0xFF)
    print (decode(encode(77,11)))
    print (encode(0,-1))
    print (decode(encode(19,-3)))