#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This is the python/pyside version of the GUI for Linux
"""

import sys, time
from scipy.interpolate import interp1d
from PySide import QtGui, QtCore
from PySide.QtGui import *

class NamedListItem(QListWidgetItem):
    # this class is used for the presets listbox, we need to keep track of the 
    # preset's name in addition to the WidgetItem text attribute
    name = ''
    def  __init__(self,pName):
        super(NamedListItem, self).__init__()
        self.setText(pName)
        self.name = pName
        # this allows us to know the old name in case of text edit

class App(QtGui.QMainWindow):
    # this is the QT application main window
    def __init__(self,model,arduGuitarConf):    
        super(App, self).__init__()
        
        self.initUI(model,arduGuitarConf)
        
    def initUI(self,model,arduGuitarConf):      
        self.model = model
        self.conf = arduGuitarConf
        
        # this is the base image for the window
        self.pm = QtGui.QPixmap(self.conf.gui.baseImageFile)
        # this is a dictionary of image overlays to indicate
        # pickups being active or not
        self.pmm = {}
        for k in self.conf.gui.imageFileDict.keys():
            self.pmm[k] = QtGui.QPixmap('')

        # set all fonts style
        self.setStyleSheet(self.conf.gui.styleStr)
        
        # create the vol and tone display in a label
        self.labelVT = QtGui.QLabel(self)
        self.labelVT.move(self.conf.gui.vtX,self.conf.gui.vtY)

        # create the preset file name display in label
        self.presetFileLabel = QtGui.QLabel(self)
        self.presetFileLabel.move(self.conf.gui.vtX,self.conf.gui.presetFileLabelY)


    def finishInit(self):
        self.setUpPresets()
        
        # turn off 'context-menu on right click'
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        
        self.setGeometry(self.conf.gui.winParams[0],
                         self.conf.gui.winParams[1],
                         self.conf.gui.winParams[2],
                         self.conf.gui.winParams[3])
        self.setWindowTitle(self.conf.gui.windowTitle)
        self.show()
    
    def setUpPresets(self):
        # create the label where the current preset name will be displayed
        self.presetLbl = QtGui.QLabel(self)

        # create and configure the preset listbox
        self.list = QListWidget(self)
        self.list.setFont(eval(self.conf.gui.listFontStr))
        
        self.list.setGeometry(self.conf.gui.xR,
                              self.conf.gui.vtY, 
                              self.conf.gui.lW,
                              self.conf.gui.lH)
        self.list.currentItemChanged[QListWidgetItem, 
                                     QListWidgetItem].connect(self.onSelected)
        self.list.itemChanged[QListWidgetItem].connect(self.onItemChanged)
        self.list.setCurrentItem(self.list.item(0))
        
        self.list.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.list.setStyleSheet(self.conf.gui.listStyleStr)
        self.list.setFrameStyle(QFrame.NoFrame)

        # create toolbar elements and configure toolbar
        writeCurrentPresetAction = QtGui.QAction(QtGui.QIcon(self.conf.gui.iconFiles[0]), 
                                                 self.conf.gui.writeCurrentPresetTip, 
                                                 self)
        writeCurrentPresetAction.setShortcut(self.conf.gui.writeCurrentPresetShrtCut)
        writeCurrentPresetAction.triggered.connect(self.writeCurrentPreset)

        createNewPresetAction = QtGui.QAction(QtGui.QIcon(self.conf.gui.iconFiles[2]),
                                              self.conf.gui.createNewPresetTip, 
                                              self)
        createNewPresetAction.setShortcut(self.conf.gui.createNewPresetShrtCut)
        createNewPresetAction.triggered.connect(self.createNewPreset)

        deleteCurrentPresetAction = QtGui.QAction(QtGui.QIcon(self.conf.gui.iconFiles[3]),
                                                  self.conf.gui.deleteCurrentPresetTip,
                                                  self)
        deleteCurrentPresetAction.setShortcut(self.conf.gui.deleteCurrentPresetShrtCut)
        deleteCurrentPresetAction.triggered.connect(self.deleteCurrentPreset)

        savePresetFileAction = QtGui.QAction(QtGui.QIcon(self.conf.gui.iconFiles[4]),
                                             self.conf.gui.savePresetFileTip,
                                             self)
        savePresetFileAction.setShortcut(self.conf.gui.savePresetFileShrtCut)
        savePresetFileAction.triggered.connect(self.savePresetFile)

        openPresetFileAction = QtGui.QAction(QtGui.QIcon(self.conf.gui.iconFiles[5]),
                                             self.conf.gui.openPresetFileTip,
                                             self)
        openPresetFileAction.setShortcut(self.conf.gui.openPresetFileShrtCut)
        openPresetFileAction.triggered.connect(self.openPresetFile)

        self.toolbar = self.addToolBar(self.conf.gui.toolbarName)
        self.toolbar.addAction(writeCurrentPresetAction)

        self.toolbar.addAction(createNewPresetAction)
        self.toolbar.addAction(deleteCurrentPresetAction)
        self.toolbar.addAction(savePresetFileAction)
        self.toolbar.addAction(openPresetFileAction)
        self.toolbar.setIconSize(eval(self.conf.gui.iconSizeStr))
        self.toolbar.setAllowedAreas(QtCore.Qt.RightToolBarArea)

        # populate the preset list box
        self.populateList()
        # update the preset file label
        self.updatePresetFileLabel()

    def updatePresetFileLabel(self):
        # call this when the nameof the  preset file changes, 
        # ie. on a save to file or load of file
        # just display the base name without extension
        # ie if file is 'toto.csv' then just display 'toto'
        path = self.model.preset.filePath
        fullFileName = path.rsplit(self.conf.gui.dirSeparator,1)[1]
        labelText = fullFileName.rsplit(self.conf.gui.fileExtensionSeparator,1)[0]
        self.presetFileLabel.setText(labelText)
        self.presetFileLabel.adjustSize() 

    def populateList(self):
        # first clean out all the old elements of the listbox
        #while self.list.count()>0:
        #    self.list.takeItem(0)
        self.list.clear()
        # then put in the new ones, making each editable
        for name in self.model.preset.presets.keys():
            item = NamedListItem(name)
            #print name
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.list.addItem(item)
        # finally update the current preset label
        self.updatePresetLbl(self.list.item(0).text())

    def updatePresetLbl(self,new):
        # set the text, adjust size, and re-center the preset name label
        self.presetLbl.setText(new)
        self.presetLbl.adjustSize()  
        xl = (self.conf.gui.xNM + self.conf.gui.xMBN)/2.0  - self.presetLbl.width()/2.0
        self.presetLbl.move(xl,self.conf.gui.vtY)

    def onSelected(self, new, old):
        # this is called when a new preset is selected in the listbox
        #if new in self.model.preset.presets.keys():
        if new: # in self.model.preset.presets.keys():
            print "list selection: " + new.text()
            self.model.loadPreset(new.text())
            self.updatePresetLbl(new.text())

    def paintEvent(self, e):
        # this is automatically called when gui display is updated
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawStuff(qp)
        qp.end()
        
    def drawStuff(self, qp):    
        # all the "drawing" is done here
        # first create and set the pen
        pen = QtGui.QPen(eval(self.conf.gui.qPenColorStr), \
                             self.conf.gui.qPenThickness, \
                             eval(self.conf.gui.qPenTypeStr)) 
        qp.setPen(pen)
        # then daw ths base image
        qp.drawPixmap(0,self.conf.gui.tbY,self.pm)
        # then draw the overlay images
        for k in self.conf.vocab.guiKeyLis:
            qp.drawPixmap(0,self.conf.gui.tbY,self.pmm[k])
        """    
        # these lines indicate the click-zones for pickup toggling
        qp.drawLine(self.xL,   0, self.xL,   self.conf.gui.winParams[3])
        qp.drawLine(self.xNM,  0, self.xNM,  self.conf.gui.winParams[3])
        qp.drawLine(self.xMBN, 0, self.xMBN, self.conf.gui.winParams[3])
        qp.drawLine(self.xBN,  0, self.xBN,  self.conf.gui.winParams[3])
        qp.drawLine(self.xR,   0, self.xR,   self.conf.gui.winParams[3])
        """
        
    def updatePickupDisplay(self,boolDict):
        # this uses a dict to set the overlay images on or off as needed
        for k in self.conf.vocab.guiKeyLis:
            if boolDict[k]:
                self.pmm[k] = QtGui.QPixmap(self.conf.gui.imageFileDict[k])
            else:
                self.pmm[k] = QtGui.QPixmap('')

    def mousePressEvent(self, event):
        # when a mouse key goes down, record start time to 
        # be able to see if it's a click or a hold
        self.pressTime = time.time()
        self.startPos  = event.pos()
        #print "start of tracking... " + str(self.startPos)

    def mouseMoveEvent(self, e):
        # this is called when a mouse key is down and the mouse is moved
        # we use it to update the vt display, but the v and t are only set
        # when the mouse is realeased.
        #print "mouse move..."
        self.curdXY = (e.pos().x() - self.startPos.x(), 
                       e.pos().y() - self.startPos.y() )
        v = self.calc(self.model.currentSettings[self.conf.vocab.volKey], 
                      self.curdXY[0],                        
                      self.conf.gui.winParams[2],
                      self.conf.model.guiVTMax) 
        t = self.calc(self.model.currentSettings[self.conf.vocab.toneKey], 
                      -self.curdXY[1],                        
                      self.conf.gui.winParams[3],
                      self.conf.model.guiVTMax) 
        self.updateVTLabel(v,t)

    def updateVTLabel(self,v,t):
        # this puts the v and t values into the label and adjusts its size
        self.labelVT.setText(self.conf.gui.textMask % (v,t))
        self.labelVT.adjustSize()  

    def mouseReleaseEvent(self, e):
        # when mouse is released we need to know if it was a click or a hold
        # use the time pressed deltaT to determine that
        deltaT = time.time() - self.pressTime
        if (deltaT >= self.conf.gui.singleClickTime):
            # so it is a hold, do the v and t updating
            #print "mouse released."
            (v,t) = self.calcVT(e.pos().x() , e.pos().y())
            self.model.updateVT(v,t)
            #p = e.pos()
            #print "started at: " + str(self.startPos)
            #print "ended at: " + str(p)
        else:
            # it was a click, so process the click
            self.mouseClicked(e)
            
    def mouseClicked(self, e):
        # left click is pickup toggle, right click is all on/off toggle
        if e.button() == QtCore.Qt.LeftButton:
            #print "mouse left click at x = " + str(e.pos().x())
            self.clickLogic(e.pos().x())
        else:
            #print "mouse right click."
            self.model.allOnOff()
            
    def clickLogic (self, mX):
        # react to a click depending on its position
        # if it's too far to left or right, do nothing
        if (mX<self.conf.gui.xL or mX>self.conf.gui.xR):
            return
        # otherwise if it is to left of neck/middle line, then it's a neck toggle
        elif (mX<self.conf.gui.xNM):
            self.model.toggle(self.model.conf.vocab.neckKey)
        # otherwise if it is to left of middle/bridge-north line, then it's a middle toggle
        elif (mX<self.conf.gui.xMBN):
            self.model.toggle(self.model.conf.vocab.middleKey)
        # otherwise if it is to left of bridge-north line, then it's a bridge-north toggle
        elif (mX<self.conf.gui.xBN):
            self.model.toggle(self.model.conf.vocab.bridgeNorthKey)
        # otherwise it's a bridge-both toggle
        else:
            self.model.toggle(self.model.conf.vocab.bridgeBothKey)

    def calcVT(self,curMouseX,curMouseY):
        # use the cursor postion to calculate a v and t value
        v  = self.calc(self.model.currentSettings[self.conf.vocab.volKey],
                       curMouseX -self.startPos.x(),
                       self.conf.gui.winParams[2],
                       self.conf.model.guiVTMax) 
        t = self.calc(self.model.currentSettings[self.conf.vocab.toneKey],
                      self.startPos.y() - curMouseY,
                      self.conf.gui.winParams[3],
                      self.conf.model.guiVTMax)
        return (v,t)

    def calc(self, currentVal, deltaPos, deltaMax, rangeMax):
        # current vol tone value,
        # delta in position since start of drag
        # deltaMax, i.e. the window size in that axis
        # rangeMax, the maximum value that can be output, eg 10
        # drag right increases vol, left decreases
        # drag up increases tone, drag down decreases

        deltaMax *= self.conf.gui.dragSensitivityMultiplier #0.5   # to make it more sensitive
        minDiviser = self.conf.gui.dragMinDiviser #6.0 

        # if the move is less than 1/mindiser of window dimension in the axis, do nothing
        m1 = interp1d([0,deltaMax],[currentVal,rangeMax])
        m2 = interp1d([-deltaMax,0],[0, currentVal])

        result = currentVal
        if (abs(deltaPos) < deltaMax/minDiviser):
            True
            #print "Min displacement not reached"
        elif (deltaPos > deltaMax):  # if we went beyond window, then take the window's dim
            #print "Max delta reached..."
            deltaPos = deltaMax
            result =float(m1(deltaPos))
        elif (deltaPos > 0):  # so we moved a bit
            #print "positve delta..."
            result = float(m1(deltaPos))
        elif (deltaPos < -deltaMax): 
            #print "-Max delta reached..."
            deltaPos = -deltaMax
            result = float(m2(deltaPos))
        elif (deltaPos < 0):
            #print "Negative delta..."
            result = float(m2(deltaPos))
            
        #print "calc result = " + str(round(result))
        return round(result)


    #toolbar methods
    def writeCurrentPreset (self):
        self.model.updatePreset(self.list.currentItem().name)
        print "Wrote: " + str(self.model.currentSettings) + \
            " to preset: " + self.list.currentItem().name

    def createNewPreset(self):
        # use the newCounter to make a unique name for the new preset, 
        newName = self.conf.gui.newPresetName % (self.conf.gui.newCounter)
        while (newName in self.model.preset.presets.keys()):
            self.conf.gui.newCounter += 1
            newName = self.conf.gui.newPresetName % (self.conf.gui.newCounter)
        item = NamedListItem(newName)  #self.conf.gui.newPresetName % (self.conf.gui.newCounter))
        self.conf.gui.newCounter += 1
        # configure the item and add to the list box and set as current
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        #print item.name, self.model.currentSettings
        self.model.addPreset(item.name) # current values are already known)
        self.list.addItem(item)
        self.list.setCurrentItem(item)
        
    def onItemChanged(self,item):
        # this is the 'rename current preset method'
        # it is called when an item's text is edited in the listbox
        old = item.name
        new = item.text()
        if new !='' and old != new:
            # first be sure it is unique
            while new in self.model.preset.presets.keys():
                new = new + "-%d" % self.conf.gui.newCounter
                self.conf.gui.newCounter += 1
            print "Preset: "+ item.name + " is now called: " + new
            self.model.renamePreset(old,new)
            item.name = new
            item.setText(new)
            self.updatePresetLbl(new)
        else:
            item.setText(old)
            print 'Preset Name change aborted...' 

    def deleteCurrentPreset(self):
        # delete the current preset item and from the model, 
        # but only do it if it is NOT the last one
        if self.list.count() > 1:
            ci = self.list.takeItem(self.list.currentRow())
            self.model.deletePreset(ci.name)
            print "Deleted preset: " + ci.name
        else:
            print "Unable to delete last preset!"

    def savePresetFile(self):
        # pop a file save dialog, and save if a file was selected
        # update the preset file name label
        fname, _ = QtGui.QFileDialog.getSaveFileName(self, 
                                                     self.conf.gui.saveFileWindowTitle,
                                                     self.model.preset.filePath, 
                                                     options=QFileDialog.DontConfirmOverwrite)
        if fname != '':
            print "Got file to save: " + fname
            self.model.savePresets(fname)
            self.updatePresetFileLabel()
        else:
            print "Cancelled file save."


    def openPresetFile(self):
        # pop an open save dialog, and open if a file was selected
        # update the preset file name label
        fname, _ = QtGui.QFileDialog.getOpenFileName(self, 
                                                     self.conf.gui.openFileWindowTitle,
                                                     self.model.preset.filePath.rsplit(self.conf.gui.dirSeparator,1)[0])

        if fname != '':
            print "Got file to open: " + fname
            self.model.loadPresetFile(fname)
            self.updatePresetFileLabel()
            self.conf.gui.newCounter = 0
            print "loaded preset file: "+ fname
        else:
            print "Cancelled file open."        
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

