#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
config.py
a class with all the configuration params for all the ArduGuitar
NOTE: use of innerclasses to separate the sub-configurations
NOTE: use strings for to eliminate module dependency, postfix them with Str
      so that they can be deferenced by setattr(self, att, eval(nameStr))
"""

import sys

class LocalConf():
    # these values may need updating on your system
    class BTSerialConf():
        sockethwTpl = ('00:12:11:19:08:54', 1) # (host, channel) tuple for linvor
        #sockethwTpl = ('00:06:66:60:46:1A', 1) # (host, channel) tuple for BlueSMIRF

    class PresetConf():
        presetDir = "data/usr/"

    class GuiConf():
        dirSeparator = '/'
        fileExtensionSeparator = '.'
        appDataDir = "data/app/"   

    def __init__(self,args=None):
        # create an instance by creating instances of inner classes
        self.btSerialConf = self.BTSerialConf()
        self.presetConf = self.PresetConf()
        self.guiConf= self.GuiConf()

class ArduGuitarVocab():
    # keys are used anywhere needed
    nameKey = 'name'
    volKey = 'vol'   
    toneKey = 'tone' 
    neckKey = 'neck'
    middleKey = 'middle'
    bridgeKey = 'bridge'
    bridgeNorthKey = 'bridgeNorth'
    bridgeBothKey  = 'bridgeBoth'
    splitKey = 'split'
    keyLis = [nameKey,
              volKey,
              toneKey,
              neckKey,
              middleKey,
              bridgeKey,
              splitKey]
    guiKeyLis = [neckKey,
                 middleKey,
                 bridgeNorthKey,
                 bridgeBothKey]
    presetDefaultNameKey = 'Default'

    
class ArduGuitarConf():
    class BTSerialConf():
        # serial conf
        # note this is a STRING and needs evaluation when the BTSerialConf class is instanciated
        socketTypeAttributeNameStr = 'socketType'
        # note this is a STRING and needs evaluation when the BTSerialConf class is instanciated
        socketTypeStr = 'bluetooth.RFCOMM' 
        # seconds time to wait to let the Arduino reply, before checking the socket
        replyWaitTime = 0.4 # seconds
        # time to wait before reconnect attempts
        reconnectWaitTime = 2 # seconds
        # how long we'll wait for a reply on a connected socekt befor giving up and declaring
        # the socket as dead
        socketTimeout = 1 # seconds
        def __init__(self,localConf,args=None):
            # localConf is an instance of the inner class BTSerialConf
            self.sockethwTpl = localConf.sockethwTpl
            # args are param,value pairs provided at init time
            if args:
                i = iter(args)
                for c in range(len(args)/2):
                    setattr(self, i.next(),i.next())
                    print "BTSerialConf Initialized"

    class ProtocolConf():
        # protocol conf
        outgoingMsgLen = 5
        incomingMsgLen = outgoingMsgLen + 1
        errorPrefix = 'e'
        okPrefixes = 'adx'
        heartbeatMsg = '99999'
        def __init__(self,args=None):
            # args are param,value pairs provided at init time
            if args:
                i = iter(args)
                for c in range(len(args)/2):
                    setattr(self, i.next(),i.next())
                    print "ProtocolConf Initialized"

    class HalConf():
        # HAL conf
        # volume control pins are: 
        # [pin between pickup-input-bus & pot-out, pin between pot-out & ground]
        volPins = [9,10,12]   
        tonePin = 11
        onOff2ValDict = {True:255,False:0}
        # this is the factor used to convert Gui scale vol and tone on [0,11]
        # to Arduino scale on [0,5]
        vtDiviser = None #
        11.0/5.0  #  note that the numerator must be the value of
        # Model.guiVTMax, and the denominator Model.arduinoVTMax
        # vol levels: [0,1,2,3,4,5]
        volPWM  = [[0,12,14,18,27,255],
                   #  volPWM[0]-> volPins[0]
                   [255,30,20,15,13,0],
                   #  volPWM[1]-> volPins[1]
                   [0,0,0,0,0,255]]  # experimental 3rd vactrol for max volume
                   #  volPWM[2]-> volPins[2]
        # tone levels: [0,1,2,3,4,5]
        tonePWM = [255,90,46,27,17,0]  #,17,27,46,90,255]
        def __init__(self,vocab,args=None):
            self.pickup2PinDict = {vocab.neckKey:2, 
                                   vocab.middleKey:3,
                                   vocab.bridgeKey:4,
                                   vocab.splitKey:5}
            # args are param,value pairs provided at init time
            if args:
                i = iter(args)
                for c in range(len(args)/2):
                    setattr(self, i.next(),i.next())
                    print "HALConf Initialized"

    class PresetConf():
        # preset conf
        defaultPresetValsLis = [11,11,False,False,True,False]
        defaultPresets = {}

        def __init__(self,vocab,localConf,args=None):
            # localConf is an instance of inner Class  PresetConf
            # at init, create a default preset dict and fill it just in case!
            self.presetDir = localConf.presetDir
            self.presetFileName = self.presetDir + "presets.csv"
            
            pDict = {}
            keys = vocab.keyLis[1:]
            #print keys
            for i in range(len(self.defaultPresetValsLis)):
                pDict[keys[i]] = self.defaultPresetValsLis[i]
            self.defaultPresets[vocab.presetDefaultNameKey] = pDict

            # args are param,value pairs provided at init time
            if args !=None:
                i = iter(args)
                for c in range(len(args)/2):
                    setattr(self, i.next(),i.next())
                    print "PresetConf Initialized"

    class ModelConf():
        # model conf
        guiCurrentSettings = {}
        #guiVTMax = 10
        guiVTMax = 11
        arduinoVTMax = 5
        heartbeatTimer = 10  #seconds
        def __init__(self,vocab,args=None):
            # args are param,value pairs provided at init time
            if args != None:
                i = iter(args)
                for c in range(len(args)/2):
                    setattr(self, i.next(),i.next())
                    print "ModelConf Initialized"

    class GuiConf():
        # GUI window conf
        windowTitle = 'ArduGuitar'

        # PRESET gui Parameters
        writeCurrentPresetTip = 'Write Current Preset'
        writeCurrentPresetShrtCut = 'Ctrl+w'
        createNewPresetTip = 'Create New Preset'
        createNewPresetShrtCut = 'Ctrl+n'
        deleteCurrentPresetTip = 'Delete Current Preset'
        deleteCurrentPresetShrtCut = 'Ctrl+d'
        savePresetFileTip = 'Save Preset File'
        savePresetFileShrtCut = 'Ctrl+s'
        openPresetFileTip = 'Open Preset File'
        openPresetFileShrtCut = 'Ctrl+o'
        newPresetName = 'New-%s'
        # the new-Counter is used to ensure that preset names are unique
        newCounter = 0        

        # toolbar stuff
        toolbarName = 'Tools'

        # file ops stuff
        saveFileWindowTitle = 'Save Preset File'
        openFileWindowTitle = 'Open Preset File'
        baseImageFileShort = 'AndroidPhone000NoPresets.png'
        imageFilesShort = ["AndroidPhone000NeckSelector.png",
                           "AndroidPhone000MiddleSelector.png",
                           "AndroidPhone000BridgeNorthSelector.png",
                           "AndroidPhone000BridgeBothSelectors.png"]
        iconFilesShort = [ "go-jump-3-16x16.png",
                           "format-text-strikethrough-2-16x16.png",
                           "list-add-3-16x16.png", 
                           "list-remove-3-16x16.png",
                           "document-save-3-16x16.png",
                           "document-open-5-16x16.png"]
        # these are x and y coordinate values for various thins
        xL = 90   # Left edge of clicking area
        xNM = 192 # line separating Neck and Middle pickups
        xMBN =  290 # line separating Middle and Bridge North pickups
        xBN = 350   # line separating Bridge North and Bridge south, ie Bridge both, pickups
        xR = 415  # Right edge of clicking area
        tbY = 4   # upper left Y coord for pixmap drawing
        vtX = 95  # X coord for vol tone label
        vtY = 44+tbY  # Y coord for vol tone label
        lW = xR-xBN  #  preset listbox width
        lH = 250     #   preset listbox height
        # note this is a STRING and needs evaluation 
        # when the GuiConf class is instanciated
        listFontStr = "QtGui.QFont('Sans',5, QtGui.QFont.Light)"
        styleStr = "* { color : white; }"
        listStyleStr = "background:transparent;"
        iconSizeStr = "QtCore.QSize(10,10)"
        qPenColorStr = "QtCore.Qt.white"
        qPenThickness=  2
        qPenTypeStr = "QtCore.Qt.SolidLine"
        winParams  = (100,100,578,315)  # app window [x,y,width, height]
        presetFileLabelY = winParams[3] - 35 
        textMask = "vol:    %d\ntone: %d"   # used to display vol and tone 
        singleClickTime = 0.2    # max time is seconds for a click to be single click instead of a hold
        dragSensitivityMultiplier = 0.5   # used to amplify the drag 
        dragMinDiviser = 6.0              # used to determin if a small drag counts or not

        def __init__(self,vocab,localConf,args=None):
            #localConf is an instance of the inner class LocalConf.GuiConf
            # create and populate the image file dictionary 
            self.dirSeparator = localConf.dirSeparator
            self.fileExtensionSeparator = localConf.fileExtensionSeparator
            self.appDataDir = localConf.appDataDir
            self.baseImageFile = self.appDataDir + self.baseImageFileShort
            self.imageFiles =  [self.appDataDir + f \
                                    for f in self.imageFilesShort] 
            self.iconFiles = [self.appDataDir + f for f in self.iconFilesShort]

            self.imageFileDict = {}
            for i in range(len(vocab.guiKeyLis)):
                self.imageFileDict[vocab.guiKeyLis[i]] = self.imageFiles[i]
            # args are param,value pairs provided at init time
            if args != None:
                i = iter(args)
                for c in range(len(args)/2):
                    setattr(self, i.next(),i.next())
                    print "GuiConf Initialized"


    def __init__(self,args=None):
        # create an instance by creating instances of inner classes and vocab
        localConf = LocalConf()
        self.vocab = ArduGuitarVocab()
        self.bt = self.BTSerialConf(localConf.btSerialConf)
        self.protocol = self.ProtocolConf()
        self.hal = self.HalConf(self.vocab)
        self.preset = self.PresetConf(self.vocab,localConf.presetConf)
        self.model = self.ModelConf(self.vocab)
        self.gui = self.GuiConf(self.vocab,localConf.guiConf)
        self.hal.vtDiviser = float(self.model.guiVTMax)/ \
            float(self.model.arduinoVTMax)

        # args are param,value pairs provided at init time
        if args:
            i = iter(args)
            for c in range(len(args)/2):
                setattr(self, i.next(),i.next())
                print "Config Initialized"
        if args:
            i = iter(args)
            for c in range(len(args)/2):
                print args[c*2] + " = " + getattr(self, i.next(),i.next())

def main():
    if len(sys.argv)>1:
        if len(sys.argv[1:])%2 != 0:
            print "Usage:" 
            print "... $ config.py" 
            print "... $ config.py attribute value attribute value -- must be eveven number of arguments!" 
        else:
            myConf = ArduGuitarConf(sys.argv[1:])
    else:
        myConf = ArduGuitarConf()

if __name__ == '__main__':
    main()
