# configs.py
# config file contains preset configurations

NeckBridgeParallelFullVolMaxTone = [
    # connect neck HB to Output with coils in series
    "connect('A',0,'M',0)",  
    "connect('A',1,'B',0)",
    "connect('B',1,'M',1)",
    # connect bridge HB to Output with coils in series
    "connect('C',0,'M',0)",
    "connect('C',1,'D',0)",
    "connect('D',1,'M',1)",
    # set all coils to straight, not inverted
    "set('A',Inverter,0)",
    "set('B',Inverter,0)",
    "set('C',Inverter,0)",
    "set('D',Inverter,0)",
    # set all Vols to 5
    "set('A',Vol,5)",
    "set('B',Vol,5)",
    "set('C',Vol,5)",
    "set('D',Vol,5)",
    "set('M',Vol,5)",
    # set all Tone to Off
    "set('A',Tone,Off)",
    "set('B',Tone,Off)",
    "set('C',Tone,Off)",
    "set('D',Tone,Off)",
    "set('M',Tone,Off)",
    # set all ToneRange to Off
    "set('A',ToneRange,Off)",
    "set('B',ToneRange,Off)",
    "set('C',ToneRange,Off)",
    "set('D',ToneRange,Off)",
    "set('M',ToneRange,Off)"]

AllSeriesFullVolMaxTone = [
    # connect neck HB to Output 
    "connect('A',0,'M',0)",  
    # set all coils in series
    "connect('A',1,'B',0)",
    "connect('B',1,'C',0)",
    "connect('C',1,'D',0)",
    # set end coil to output ground
    "connect('D',1,'M',1)",
    # set all coils to straight, not inverted
    "set('A',Inverter,0)",
    "set('B',Inverter,0)",
    "set('C',Inverter,0)",
    "set('D',Inverter,0)",
    # set all Vols to 5
    "set('A',Vol,5)",
    "set('B',Vol,5)",
    "set('C',Vol,5)",
    "set('D',Vol,5)",
    "set('M',Vol,5)",
    # set all Tone to Off
    "set('A',Tone,Off)",
    "set('B',Tone,Off)",
    "set('C',Tone,Off)",
    "set('D',Tone,Off)",
    "set('M',Tone,Off)",
    # set all ToneRange to Off
    "set('A',ToneRange,Off)",
    "set('B',ToneRange,Off)",
    "set('C',ToneRange,Off)",
    "set('D',ToneRange,Off)",
    "set('M',ToneRange,Off)"]

DOnlyFullVolMaxTone = [
    # connect bridge coil D to Output
    "connect('D',0,'M',0)",  
    "connect('D',1,'M',1)",
    # set all coils to straight, not inverted
    "set('A',Inverter,0)",
    "set('B',Inverter,0)",
    "set('C',Inverter,0)",
    "set('D',Inverter,0)",
    # set all Vols to 5
    "set('A',Vol,5)",
    "set('B',Vol,5)",
    "set('C',Vol,5)",
    "set('D',Vol,5)",
    "set('M',Vol,5)",
    # set all Tone to Off
    "set('A',Tone,Off)",
    "set('B',Tone,Off)",
    "set('C',Tone,Off)",
    "set('D',Tone,Off)",
    "set('M',Tone,Off)",
    # set all ToneRange to Off
    "set('A',ToneRange,Off)",
    "set('B',ToneRange,Off)",
    "set('C',ToneRange,Off)",
    "set('D',ToneRange,Off)",
    "set('M',ToneRange,Off)"]

COnlyFullVolMaxTone = [
    # connect bridge coil C to Output
    "connect('C',0,'M',0)",  
    "connect('C',1,'M',1)",
    # set all coils to straight, not inverted
    "set('A',Inverter,0)",
    "set('B',Inverter,0)",
    "set('C',Inverter,0)",
    "set('D',Inverter,0)",
    # set all Vols to 5
    "set('A',Vol,5)",
    "set('B',Vol,5)",
    "set('C',Vol,5)",
    "set('D',Vol,5)",
    "set('M',Vol,5)",
    # set all Tone to Off
    "set('A',Tone,Off)",
    "set('B',Tone,Off)",
    "set('C',Tone,Off)",
    "set('D',Tone,Off)",
    "set('M',Tone,Off)",
    # set all ToneRange to Off
    "set('A',ToneRange,Off)",
    "set('B',ToneRange,Off)",
    "set('C',ToneRange,Off)",
    "set('D',ToneRange,Off)",
    "set('M',ToneRange,Off)"]

BOnlyFullVolMaxTone = [
    # connect neck coil B to Output
    "connect('B',0,'M',0)",  
    "connect('B',1,'M',1)",
    # set all coils to straight, not inverted
    "set('A',Inverter,0)",
    "set('B',Inverter,0)",
    "set('C',Inverter,0)",
    "set('D',Inverter,0)",
    # set all Vols to 5
    "set('A',Vol,5)",
    "set('B',Vol,5)",
    "set('C',Vol,5)",
    "set('D',Vol,5)",
    "set('M',Vol,5)",
    # set all Tone to Off
    "set('A',Tone,Off)",
    "set('B',Tone,Off)",
    "set('C',Tone,Off)",
    "set('D',Tone,Off)",
    "set('M',Tone,Off)",
    # set all ToneRange to Off
    "set('A',ToneRange,Off)",
    "set('B',ToneRange,Off)",
    "set('C',ToneRange,Off)",
    "set('D',ToneRange,Off)",
    "set('M',ToneRange,Off)"]

AOnlyFullVolMaxTone = [
    # connect neck coil A to Output
    "connect('A',0,'M',0)",  
    "connect('A',1,'M',1)",
    # set all coils to straight, not inverted
    "set('A',Inverter,0)",
    "set('B',Inverter,0)",
    "set('C',Inverter,0)",
    "set('D',Inverter,0)",
    # set all Vols to 5
    "set('A',Vol,5)",
    "set('B',Vol,5)",
    "set('C',Vol,5)",
    "set('D',Vol,5)",
    "set('M',Vol,5)",
    # set all Tone to Off
    "set('A',Tone,Off)",
    "set('B',Tone,Off)",
    "set('C',Tone,Off)",
    "set('D',Tone,Off)",
    "set('M',Tone,Off)",
    # set all ToneRange to Off
    "set('A',ToneRange,Off)",
    "set('B',ToneRange,Off)",
    "set('C',ToneRange,Off)",
    "set('D',ToneRange,Off)",
    "set('M',ToneRange,Off)"]

bridgeBucker = [
    # connect bridge C+ to Output+
    "connect('C',0,'M',0)",  
    # connect bridge C- to D+
    "connect('C',1,'D',0)",
    # connect bridge D- to Output-
    "connect('D',1,'M',1)",
    # set all coils to straight, not inverted
    "set('A',Inverter,0)",
    "set('B',Inverter,0)",
    "set('C',Inverter,0)",
    "set('D',Inverter,0)",
    # set all Vols to 5
    "set('A',Vol,5)",
    "set('B',Vol,5)",
    "set('C',Vol,5)",
    "set('D',Vol,5)",
    "set('M',Vol,5)",
    # set all Tone to Off
    "set('A',Tone,Off)",
    "set('B',Tone,Off)",
    "set('C',Tone,Off)",
    "set('D',Tone,Off)",
    "set('M',Tone,Off)",
    # set all ToneRange to Off
    "set('A',ToneRange,Off)",
    "set('B',ToneRange,Off)",
    "set('C',ToneRange,Off)",
    "set('D',ToneRange,Off)",
    "set('M',ToneRange,Off)"]

neckBucker = [
    # connect neck A+ to Output+
    "connect('A',0,'M',0)",  
    # connect neck A- to B+
    "connect('A',1,'B',0)",
    # connect neck B- to Output-
    "connect('B',1,'M',1)",
    # set all coils to straight, not inverted
    "set('A',Inverter,0)",
    "set('B',Inverter,0)",
    "set('C',Inverter,0)",
    "set('D',Inverter,0)",
    # set all Vols to 5
    "set('A',Vol,5)",
    "set('B',Vol,5)",
    "set('C',Vol,5)",
    "set('D',Vol,5)",
    "set('M',Vol,5)",
    # set all Tone to Off
    "set('A',Tone,Off)",
    "set('B',Tone,Off)",
    "set('C',Tone,Off)",
    "set('D',Tone,Off)",
    "set('M',Tone,Off)",
    # set all ToneRange to Off
    "set('A',ToneRange,Off)",
    "set('B',ToneRange,Off)",
    "set('C',ToneRange,Off)",
    "set('D',ToneRange,Off)",
    "set('M',ToneRange,Off)"]


neckBuckerPhased = [
    # connect neck A+ to Output+
    "connect('A',0,'M',0)",  
    # connect neck A- to B+
    "connect('A',1,'B',0)",
    # connect neck B- to Output-
    "connect('B',1,'M',1)",
    #  invert coil B, only
    "set('A',Inverter,0)",
    "set('B',Inverter,1)",
    "set('C',Inverter,0)",
    "set('D',Inverter,0)",
    # set all Vols to 5
    "set('A',Vol,5)",
    "set('B',Vol,5)",
    "set('C',Vol,5)",
    "set('D',Vol,5)",
    "set('M',Vol,5)",
    # set all Tone to Off
    "set('A',Tone,Off)",
    "set('B',Tone,Off)",
    "set('C',Tone,Off)",
    "set('D',Tone,Off)",
    "set('M',Tone,Off)",
    # set all ToneRange to Off
    "set('A',ToneRange,Off)",
    "set('B',ToneRange,Off)",
    "set('C',ToneRange,Off)",
    "set('D',ToneRange,Off)",
    "set('M',ToneRange,Off)"]

configDict = {'nb1': NeckBridgeParallelFullVolMaxTone,
              'as1' : AllSeriesFullVolMaxTone,
              'd':  DOnlyFullVolMaxTone,
              'c' : COnlyFullVolMaxTone,
              'b' : BOnlyFullVolMaxTone,
              'a' : AOnlyFullVolMaxTone,
              'bridge' : bridgeBucker,
              'neck' : neckBucker,
              'nbp'  : neckBuckerPhased}

def mapReplace(appName, config):
    """
    Sets up the list of strings for a call to eval()
    by adding the name with a dot:
    e.g. a.set(...
    then adding 'State.' and 'State.l' as needed
    """
    newConfig =[]
    for c in config:
        c = appName +'.' + c
        c = c.replace('Inverter','State.Inverter')
        c = c.replace('Vol','State.Vol')
        c = c.replace('Tone','State.Tone')
        if c.find('set') > -1:
            c = c.replace('Off','State.lOff')
            c = c.replace('0','State.l0')
            c = c.replace('1','State.l1')
            c = c.replace('2','State.l2')
            c = c.replace('3','State.l3')
            c = c.replace('4','State.l4')
            c = c.replace('5','State.l5')
        newConfig += [c]
    return newConfig

