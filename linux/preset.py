#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
preset.py
 preset mgt. part of the model layer
"""

import sys,csv
import config

class Preset():
    # the presets are kept in a dictionary of form:
    #{'presetName':{
    #               'vol':10,
    #               'tone':10;
    #               'neck':True,
    #               'middle':True,
    #               'bridge':False,
    #               'split':False},
    #  'anotherPresetName':{...},
    #  ...}

    def __init__(self,arduGuitarConf,fileName=None):
        # the fileName is used to load a presets file, if one exists,
        # if not, one is created
        self.conf = arduGuitarConf
        self.presets = {}
        if fileName==None:
            self.filePath = self.conf.preset.presetFileName
        else:
            self.filePath = fileName
        print "creating preset instance from " + self.filePath
        try:
            with open(self.filePath, 'r') as csvfile:
                print "opened file: " + self.filePath
                reader = csv.reader(csvfile, delimiter=',')
                self.header = reader.next()
                #print self.header
                if not self.header: raise IOError
                for row in reader:
                    rowDict = {}
                    for k,v in map(None,self.header,row):
                        if k != 'name':
                            rowDict[k] = eval(v)
                        else:
                            pName = v
                    self.presets[pName] = rowDict
        except:
            print "error reading preset file!  Creating new one!"
            self.createDefaultPresets()
        
    def createDefaultPresets(self):
        # this will create a default preset file in the default location
        # with default content
        self.presets = self.conf.preset.defaultPresets
        self.header = self.conf.vocab.keyLis
        self.toFile(self.conf.preset.presetFileName)

    def toFile(self, file = None):
        # this will write the presets to a file,
        # if a file argument is provided it is used and it
        # updates the instance filePath
        # otherwise the current instance filePath is used
        if file: 
            self.filePath = file
        with open(self.filePath, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar="'", 
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.header)
            for p in self.presets.keys():
                rowDict = self.presets[p]
                row = [p]
                for h in self.header[1:]:
                    row.append(rowDict[h])
                writer.writerow(row)

    def add(self,name,vDict):
        # add this to the presets, if the vDict is proper length:
        # and no keys are wrong
        # print "preset.add(",name,vDict,")", self.header
        assert(len(vDict) == len(self.header[1:]))
        assert [k in self.header for k in vDict.keys()]
        newDict = {}
        for k in vDict.keys():
            newDict[k] = vDict[k]
        self.presets[name]=newDict
        
    def remove(self,name):
        # just remove it or do nothing if not possible
        if name in self.presets.keys():
            del self.presets[name]

    def rename(self,old,new):
        # to rename a preset, we create a new dict copied from previous one
        # put it in with the new name
        # and remove the reference to the old name
        # if the old name is not found, do nothing
        # return True if success, False otherwise
        # print "renaming preset: " + old + " to: " + new
        res = False
        if old in self.presets.keys():
            newDict = {}
            for k in self.presets[old].keys():
                newDict[k] = self.presets[old][k]
            self.presets[new] = newDict
            del self.presets[old]
            res = True
        return res

def main():
    conf = config.ArduGuitarConf()
    #p = Preset(conf,"data/usr/temp.csv")
    p = Preset(conf)
    d = {'bridge': True, 'tone': 10, 'name': 'FRANK', 'vol': 10, 'middle': False, 'split': False, 'neck': False}
    p.add('FRANK', d)
    p.remove('Default')
    p.toFile()
    #p.toFile('data/usr/temp2.csv')

    

if __name__ == '__main__':
    main()
