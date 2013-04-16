#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
model.py 
needs to manage everything:
 - Gui
 - Preset
 - Hal
   - protocol 
     -btSerial
"""
# this is for testing without the Bluetooth connection
useBluetooth = False


import sys,time
import threading
from Queue import *
from PySide import QtGui

import config
import preset
import hal
import gui

class HalThread(threading.Thread):
    def __init__(self, arduGuitarConf, comm, q):
        super(HalThread,self).__init__()
        self.dictQ = q
        self.setDaemon(True)
        self.hal = hal.Hal(arduGuitarConf,comm) 

    def run(self):
        print ("HalThread running.")
        while(True):
            dictItem = self.dictQ.get()
            self.hal.update(dictItem)
            self.dictQ.task_done()

class Model():
    def __init__(self,arduGuitarConf,comm=True): 
        # com argument is to allow execution without a bluetooth connection
        # first, create a semaphore for threading protection
        #self.lk = thread.allocate_lock()
        self.q = Queue()
        self.halThread = HalThread(arduGuitarConf,comm,self.q) 
        self.halThread.start()

        # create the dictionary for the current settings:
        # vol, tone, pickups, split
        self.currentSettings = {}
        # get the conf
        self.conf = arduGuitarConf        

        # get the presets
        self.preset = preset.Preset(self.conf)
        
        # Create an instance of the QApllication and the GUI App class
        app = QtGui.QApplication(sys.argv)
        # App instanciation is split in 2 parts, due to need for
        # a Preset instance
        self.gui = gui.App(self,arduGuitarConf) 
        
        self.loadPreset(self.preset.presets.keys()[0])
        
        # here we finish the init of the GUI
        self.gui.finishInit()

        # use a try block to insure that clean up takes place on exit
        try:
            sys.exit(app.exec_())
        finally:
            #  save presets to file.
            #self.halThread.stop()
            self.preset.toFile()

    #########################
    ###### Preset Mgt #######
    def savePresets(self,fname):
        self.preset.toFile(fname)

    def  loadPresetFile(self,fname):
        #load a preset file
        self.currentSettings = {}
        self.preset = preset.Preset(self.conf,fname)
        print "model.loadPresetFile(" +fname+"):"
        print "presets are: " + str(self.preset.presets)
        self.loadPreset(self.preset.presets.keys()[0])
        # now put them in the Gui
        self.gui.populateList()

    def loadPreset(self,pName):
        print "model.loadPreset(" + pName + ")"
        if not pName in self.preset.presets.keys():
            print "model.loadPreset tried to load a bad preset name: " + pName
        else:
            # update everything that needs updating due to new preset
            self.update(self.preset.presets[pName])
    
    def renamePreset(self,old,new):
        # just delegate this to the Preset class
        self.preset.rename(old,new)

    def updatePreset(self,name):
        # settings can be modifed at any time, but they are not saved
        # to the current preset until this call.
        # this is where we write the currenSettings to the current preset
        for k in self.currentSettings.keys():
            #print " update: " + k
            #print "to: " + str(self.currentSettings[k])
            (self.preset.presets[name])[k] = \
                self.currentSettings[k]
    
    def addPreset(self,name):
        #print name, self.currentSettings
        self.preset.add(name,self.currentSettings)

    def deletePreset(self,name):
        #print "model deleting current preset: " + name #self.currentNameKey
        self.preset.remove(name)
        self.loadPreset(self.preset.presets.keys()[0])
    
    ###############################
    ###### Volume and Tone  #######

    def updateVT(self,v,t):
        # first refresh display to avoid lag
        self.gui.updateVTLabel(v,t)
        # then call the updater for the hardware
        self.update({self.conf.vocab.volKey:v,
                     self.conf.vocab.toneKey:t})

    ###########################
    ###### Pickup Mgt.  #######

    def allOnOff(self):
        # process all aspects of a toggle all On/Off
        pNameLis = [self.conf.vocab.neckKey,
                    self.conf.vocab.middleKey,
                    self.conf.vocab.bridgeKey]
        newSettings = {}
        # if any are On, ie True, then we turn all off
        turnAllOff = any([self.currentSettings[k] for k in pNameLis])
        # turn them all on/off as appropriate
        for k in pNameLis:
            newSettings[k] = not turnAllOff
        # don't forget that the split is off no matter what
        newSettings[self.conf.vocab.splitKey] = False
        self.update(newSettings)

    def toggle(self,guiKey):
        # invert the setting of the item pointed by 'guiKey'
        newSettingsDict = {}
        # if there's no splitting, then just invert it
        if not self.splittable(guiKey):
            newSettingsDict[guiKey] = not self.currentSettings[guiKey]
        else:
            # treat the various cases of splitting
            self.toggleSplit(guiKey,newSettingsDict)
        self.update(newSettingsDict)

    def splittable(self,guiKey):
        # currently only the bridge* keys refer to a splittable pickup
        return guiKey in [self.conf.vocab.bridgeNorthKey,
                          self.conf.vocab.bridgeBothKey]

    def toggleSplit(self,guiKey,newSettingsDict):
        # handle split logic based on gui input
        # 
        #   if not bridge:   
        #      bridge <- True            -- always turn bridge on
        #      split  <- guiKey==bridgeNorthKey  -- north means split
        #   elif split:  -- ie bridge & split
        #      split  <- False -- always
        #      bridge <- guiKey != bridgeNorthKey
        #   else:     -- ie. bridge & not split 
        #       bridge <- guiKey = bridgeNorthKey
        #       split <- guiKey = bridgeNorthKey

        if not self.currentSettings[self.conf.vocab.bridgeKey]:
            newSettingsDict[self.conf.vocab.bridgeKey] = True
            newSettingsDict[self.conf.vocab.splitKey] = \
                guiKey == self.conf.vocab.bridgeNorthKey
        elif self.currentSettings[self.conf.vocab.splitKey]:
            newSettingsDict[self.conf.vocab.splitKey] = False
            newSettingsDict[self.conf.vocab.bridgeKey] = \
                guiKey != self.conf.vocab.bridgeNorthKey
        else: 
            newSettingsDict[self.conf.vocab.bridgeKey] = \
                newSettingsDict[self.conf.vocab.splitKey] = \
                guiKey == self.conf.vocab.bridgeNorthKey

    ###########################
    ###### Update Mgt.  #######
    def update(self,newSettingsDict):
        # this method handles the updating of the current settings
        # and initiates harware updating.
        # newSettingsDict contains all the settings that need updating
        # create a temporary clean dictionary, to be sure to not
        # cause side-effects.Copy all the new settings into it.
        tempD = {}
        for k in newSettingsDict.keys():
            tempD[k] = newSettingsDict[k]
        # first check to see what's really new and get rid of anything
        # that was already correctly set. This is to minimize communication
        # with the hardware layer.
        for key in tempD.keys():
            if (not key in self.currentSettings.keys()) or \
                    self.currentSettings[key]!=tempD[key]: 
                # if it's a change then update in current settings
                self.currentSettings[key]=tempD[key] 
            else:
                # if it's not a change then remove it from the work to do
                del tempD[key] 
        # at this point tempD contains the minimum set of elements 
        # requiring update on hardware
        if len(tempD)>0:
            # first refresh gui !
            self.updateGui()
            # if there are any settings left to process, then enqueue
            # them so the HalThread can process them!
            self.q.put_nowait(tempD)  
            print ('put on queue' + str(tempD))


    def updateGui(self):
        # this is where we update the gui
        # first update the volume and tone display
        self.gui.updateVTLabel(self.currentSettings[self.conf.vocab.volKey],
                               self.currentSettings[self.conf.vocab.toneKey])
        # then make a dictionary for the pickup display settings
        boolDict = {}
        boolDict[self.conf.vocab.neckKey] = \
            self.currentSettings[self.conf.vocab.neckKey]
        boolDict[self.conf.vocab.middleKey] = \
            self.currentSettings[self.conf.vocab.middleKey]

        if  self.currentSettings[self.conf.vocab.bridgeKey]:
            boolDict[self.conf.vocab.bridgeNorthKey] = \
                self.currentSettings[self.conf.vocab.splitKey]
            boolDict[self.conf.vocab.bridgeBothKey] = \
                not self.currentSettings[self.conf.vocab.splitKey]
        else:
            boolDict[self.conf.vocab.bridgeNorthKey] = \
                boolDict[self.conf.vocab.bridgeBothKey] = False
        self.gui.updatePickupDisplay(boolDict)
        self.gui.update()

def main():
    conf = config.ArduGuitarConf()
    if len(sys.argv)>1:
        m = Model(conf,eval(sys.argv[1]))
    else:
        m = Model(conf,useBluetooth) 

if __name__ == '__main__':
    main()
