# this is where I put all the preset configs

"""
Each config is a dictionary of this form:
currentDict = {'Name': 'EasyMusic',
               'M' : [0,0],   # vol, tone
               'A' : [0,0], 
               'B' : [0,0], 
               'C' : [0,0], 
               'D' : [0,0], 
               'TR' : [None,0],  # range on [0,5]
               'S' : '(|(+A(|BC)D)',
               'TREM' : 0,
               'VIB' : 0}
"""
# configs is a dictionary with key (hs,vs) where hs is horizontal selector pos, and vs is vertical selector pos
Configs  = {(0,0): fullNeckSeries,
            (1,0): fullB,
            (2,0): fullNeckBridgeParallel,
            (3,0): fullC,
            (4,0): fullBridgeSeries,
            (0,1): fullNeckParalllel,
            (1,1): fullA,
            (2,1): fullNeckBridgeSeries,
            (3,1): fullD,
            (4,1): fullBridgeSeries,
            (0,2): NeckWoman,
            (1,2): ADSeriesWoman,
            (2,2): ABCDSeriesWoman,
            (3,2): BCSeriesWoman,
            (4,2): BridgeWoman,
            (0,3): fullOn,
            (1,3): fullOn,
            (2,3): fullOn,
            (3,3): fullOn,
            (4,3): fullOn,
            (0,4): fullOn,
            (1,4): fullOn,
            (2,4): fullOn,
            (3,4): fullOn,
            (4,4): fullOn}
                