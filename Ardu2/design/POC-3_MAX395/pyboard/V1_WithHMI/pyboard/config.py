class PyGuitarConf():
    class Vocab():
        configKeys=['Name',               #  0
                'M',   # vol, tone     #  1
                'A',                   #  2
                'B',                   #  3 
                'C',                   #  4
                'D',                   #  5
                'TR',  # range on [0,5]          #  6  
                'S',   # a string like '(|ABc)'  #  7
                'TREM',                #  8
                'VIB',                 #  9
                'AUX0',                # 10
                'AUX1']                # 11
        
        headings= ['HorizontalSelector',  #  0
                'VerticalSelector',    #  1
                configKeys[0],         #  2
                configKeys[1] + 'asterVol',           #  3
                configKeys[1] + 'asterTone',          #  4
                configKeys[2] + 'Vol',                #  5
                configKeys[2] + 'Tone',               #  6
                configKeys[3] + 'Vol',                #  7
                configKeys[3] + 'Tone',               #  8
                configKeys[4] + 'Vol',                #  9
                configKeys[4] + 'Tone',               # 10
                configKeys[5] + 'Vol',                # 11
                configKeys[5] + 'Tone',               # 12
                'ToneRange'] +  configKeys[7:]        # 13
                                        # 14
                                        # 15 
                                        # 16
                                        # 17
                                        # 18

    class LocalConf():
        presetDir     = '/sd/Data'
        dirSeparator  = '/'
        presetFileName = 'presets.csv'
        
    class PresetConf():
        defaultPresetValList= ['(0,0)',
                               [5,5],   # M vol, tone
                               [5,5], 
                               [5,5], 
                               [5,5], 
                               [5,5], 
                               [None,4],  # range on [0,4]
                               '(+ABCD)',
                               0,
                               0, 
                               0,
                               0]
        def __init__(self):
            self.defaultConfDict = {}
            for i in range(len(PyGuitarConf.Vocab.configKeys)):
                 self.defaultConfDict[PyGuitarConf.Vocab.configKeys[i]] = PyGuitarConf.PresetConf.defaultPresetValList[i]
                        
    def __init__(self):
        self.vocab = PyGuitarConf.Vocab()
        self.presetConf = PyGuitarConf.PresetConf()
