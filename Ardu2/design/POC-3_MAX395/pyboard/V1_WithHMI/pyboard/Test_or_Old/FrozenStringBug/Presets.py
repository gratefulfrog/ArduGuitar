# version for tests, no use of State.printT
# currently uses the original key lookup which failed in the past...

import csv

print('This is FROZEN Presets.py')

class Preset():

    def __init__(self,pyGuitarConf):
        self.conf = pyGuitarConf
        self.presets = {}
        self.filePath =  self.conf.LocalConf.presetDir +   self.conf.LocalConf.dirSeparator +  self.conf.LocalConf.presetFileName
        print ("creating preset instance from:\t" + self.filePath)
        with open(self.filePath, 'r') as csvfile:
            reader = csv.CSV.Reader(csvfile)
            self.header = next(reader)
            for row in reader:
                self.rowDict2confDict(row)

    def rowDict2confDict(self,row):
        curConfDict= {}
        self.presets[(int(row[0]),int(row[1]))]= curConfDict
        curConfDict[self.conf.Vocab.configKeys[0]] = row[2]
        for i in  range(1,6):
            curConfDict[self.conf.Vocab.configKeys[i]] = [int(row[1+2*i]),int(row[2+2*i])]
        curConfDict[self.conf.Vocab.configKeys[6]] = [None,int(row[13])]
        curConfDict[self.conf.Vocab.configKeys[7]] = row[14]
        j=15
        for k in self.conf.Vocab.configKeys[8:]:
                curConfDict[k] = int(row[j])
                j+=1

    
    def toFile(self):
        # this will write the presets to a file,
        with open(self.filePath, 'w') as csvfile:
            writer = csv.CSV.Writer(csvfile)
            writer.writeRow(self.header)
            for p in self.presets.keys():
                rowDict = self.confDict2RowDict(p,self.presets[p])
                print(rowDict)
                rawRow = [rowDict[k] for k in self.header]
                print(rawRow)
                writer.writeRow(rawRow)
        print( "Wrote file:\t" + self.filePath)

    def confDict2RowDict(self,key,conf):
        curRowDict= {}
        # horiz and verti
        for i in range(2):
            curRowDict[self.conf.Vocab.headings[i]] = key[i]
        #Name
        curRowDict[self.conf.Vocab.headings[2]] = conf[self.conf.Vocab.headings[2]]
        
        #M,A,B,C,D  vol and tone    
        for i in  range(1,6):
            curRowDict[self.conf.Vocab.headings[1+2*i]] = conf[self.conf.Vocab.configKeys[i]][0]
            curRowDict[self.conf.Vocab.headings[2+2*i]] = conf[self.conf.Vocab.configKeys[i]][1]
        # TneRange    
        curRowDict[self.conf.Vocab.headings[13]] = conf[self.conf.Vocab.configKeys[6]][1]
        #S,TREM,VIB,AUX0,AUX1
        for k in self.conf.Vocab.headings[14:]:
                curRowDict[k] = conf[k]
        return curRowDict
    
    def add(self,name,vDict):
        # add this to the presets
        newDict = {}
        for k in vDict.keys():
            newDict[k] = vDict[k]
        self.presets[name]=newDict
        
    def saveCurrentConfigAsPreset(self, key):
        self.currentDict[self.conf.vocab.configKeys[11]] = 0
        self.add(key,self.currentDict)
        self.toFile()
            
