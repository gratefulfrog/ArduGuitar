# csv.py
# my implementation of csv reading and writing

"""
READING interface:

 try:
                with open(self.filePath, 'r') as csvfile:
                    #print "opened file: " + self.filePath
                    reader = csv.Reader(csvfile)
                    self.header = next(reader)
                    for row in reader:
                        self.rowDict2confDict(row)

WRITING Interface:
 with open(self.filePath, 'w') as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames = self.conf.Vocab.headings,
                                    delimiter=',')
                                    #quotechar="'", 
                                    #quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.header)
            for p in self.presets.keys():
                writer.writerow(self.confDict2RowDict(p,self.presets[p]))
"""

class CSV():
    class Reader():
        """
        usage:
        f=open('aFile.csv', 'r')
        reader = Reader(f)
        header = next(reader)
        lines = [l for l in reader]
        f.close()
        or 
        with open('aFile.csv', 'r') as f:
          reader = Reader(f)
          header = next(reader)
          lines = [l for l in reader]
        """
        def __init__(self,openFile,delimeter=',',quote='"'):
            # read rows, return list of cells, quoting if needed,
            # all cells are read and returned as strings
            self.openFile  = openFile
            self.delimeter = delimeter
            self.quote     = quote

        def __iter__(self):
            return self

        def __next__(self):
            line = self.openFile.readline()
            if line == '':
                raise StopIteration
            return self.parse(line)
            
        def parse(self,line):
            return self.parseIter(line,current='',mode=0,res=[])

        def parseIter(self,line,current,mode,res):
            """
            mode=0
            current = ''
            0: looking for any character or eol
             : if c==delimeter, append current, loop
             : if c==quote, mode<-1, loop
             : if eol, append current, return res
             : else current+=c, mode<-2, loop
            1: looking for closing quote
             : if eol: raise missing closing quote error
             : if c==quote, mode<-3, loop
             : else, current+=c, loop
            2: reading chars, looking for delimeter or eol
             : if eol: append current, return
             : if c==delimeter, append current, current<-'', mode<-0, loop
             : else: current+=c, loop
            3: finished a quoted expr, need delimeter
             : if c != delimeter: raise missing delimeter error
             : else, append current, current<-'', mode<-0,loop
            """
            for c in line:
                if c=='\r':
                    continue
                if mode==0:
                    if c=='\n':
                        res.append(current)
                        return res
                    if c == self.delimeter:
                        res.append(current)
                        current=''
                        continue 
                    elif c==self.quote:
                        mode = 1
                        continue 
                    else:
                        current+=c
                        mode=2
                        continue
                elif mode==1:
                    if c=='\n':
                        raise Exception('Missing Closing Quote!')
                    if c==self.quote:
                        mode = 3
                        continue
                    else:
                        current+=c
                        continue
                elif mode==2:
                    if c=='\n':
                        res.append(current)
                        return res
                    if c==self.delimeter:
                        res.append(current)
                        current = ''
                        mode=0
                        continue
                    else:
                        current+=c
                        continue
                elif mode==3:
                    if c=='\n':
                        res.append(current)
                        return res
                    elif c==self.delimeter:
                        res.append(current)
                        current = ''
                        mode=0
                        continue 
                    else:
                        raise Exception('Found character after quote before delimeter!')
            return res
                
    class Writer():
        """
         writer = csv.DictWriter(csvfile)
         writer.writeRow(self.header)
         for p in self.presets.keys():
             writer.writerow(self.confDict2RowDict(p,self.presets[p]))
        """
        def __init__(self,openFile,delimeter=',',quote='"'):
            self.openFile   = openFile
            self.delimeter  = delimeter
            self.quote      = quote

        def writeRow(self,row):
            """
            row is a list of elements, potentially contaning a delimeter!
            if the elt has a delimeter, then quote it,
            
            """
            toFile = ''
            for elt in row[:-1]:
                toFile += self.fix(elt) + self.delimeter
            toFile += row[-1] + '\n'
            self.openFile.write(toFile)

        def fix(self,elt):
            res = str(elt)
            if res.find(self.delimeter) >= 0:
                return '%c%s%c'%(self.quote,res,self.quote)
            else:
                return res
        
