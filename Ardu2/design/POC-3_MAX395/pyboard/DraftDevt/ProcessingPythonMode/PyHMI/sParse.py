# sParse.py
# parse string expressions into connection function calls
"""
String expressions are of the form
* A
* a
* (|AB) 
* (+AbCd) 
* (+A(|Cd)b)

Reading the following gramar:
::== means 'is defined as'
| means 'or'
'c' means 'the literal c'
* means multiples may occur with min of zero
+ means multiples may occur with min of one

Gramar:
Exp::== Atom | Pexp
Atom::== StraightAtom | InvertedAtom
StraightAtom::== A | B | C | D 
InvertedAtom::== a | b | c | d 
Pexp::== '('Func Exp+')'
Func::== '|' | '+'

Validation rules for Exp E
General Rule:
if atom(j) occurs in E, then j and J must not occur anywhere else in E
if len(E) == 1, then Exp must be a valid Atom
if Atom(E), then E must be == to one of A a B b C c D d
if not(Atom(E), then e must be valid Pexp
if Pexp(E), then E[0] == '(' and E[1] is a valid func and E[-1] ==')'
if validFunc(E[i]) then E[i] must be == to one of '|' '+'

Now, how to interpret the String:

"""
from parse import ss,pp,connectionList

# stub inverter call
def invert(coil):
    print ('Inverted Coil:\t\t'+coil)
def connect(a,b):
    print ('Connected Coils:\t'+ a +','+b)


env = { 's':ss,
        'p':pp,
        'invert': invert,
        'connectionList': connectionList,
        'connect': connect,
        'a':'a',
        'b':'b',
        'c':'c',
        'd':'d',
        'A':'A',
        'B':'B',
        'C':'C',
        'D':'D'}

class SExpParser():
    straight = ['A','B','C','D']
    inverted = ['a','b','c','d']
    atoms    = straight + inverted
    funcs    = ['|', '+']
    evalFuncDict = {'|' : 'p(',
                    '+' : 's('}
    openP    = '('
    closeP   = ')'

    def __init__(self,Exp):
        self.checkDoubles(Exp)
        self.checkSingleton(Exp)
        self.tokens = list(Exp)

    def __repr__(self):
        return str(self.tokens)

    def checkDoubles(self,exp):
        """
        raise syntax error if the same coil is referneced more than once
        """
        for i in exp:
            if i in SExpParser.atoms:
                if exp.upper().count(i.upper())>1:
                    raise SyntaxError('coil occurs more than once: ' +i.upper())

    def checkSingleton(self,exp):
        if len(exp) == 1:
            if exp not in SExpParser.atoms:
                raise SyntaxError('unkonwn coil name: ' + exp)
        elif exp[0] != '(':
            raise SyntaxError('misformed expression: ' + exp)
        
    
    def readFromTokens(self,tokens):
        "Read an expression from a sequence of tokens. Physically destroys tokens"
        if len(tokens) == 0:
            raise SyntaxError('unexpected EOF while reading')
        token = tokens.pop(0)
        if '(' == token:
            L = []
            while tokens[0] != ')':
                L.append(self.readFromTokens(tokens))
            tokens.pop(0) # pop off ')'
            return L
        elif ')' == token:
            raise SyntaxError('unexpected )')
        else:
            return token

    def executable(self):
        res0 = self.pModal(self.readFromTokens([x for x in self.tokens]))
        res1= ''
        inverters = []
        for c in  res0:
            if c in SExpParser.inverted:
                inverters.append('invert('+c.upper()+')')
                res1+=c.upper()
            else:
                res1+=c
            
        return inverters+[res1]

    def execute(self):
        exps = self.executable()
        res=[]
        for exp in exps[0:-2]:
            res.append(eval(exp,env))
        for con in connectionList(eval(exps[-1],env)):
            connect(con[0],con[1])


    def pModal(self,expLis,mode=0,res=''):
        """
        modes are:
        0: looking for a func or singleton atom
        1: looking for 1st arg
        2: looking for more args or the end
        transistions are:
        0: find a func: add its deref, mode<-2, recurse on rest.
        0: find singleton atom, replace it by ['|',atom] recurse on full
        0: find anything else:  syntax error
        1: find a list: add the result of recursing on it in mode 0, and recurse on rest in mode 2
        1: find an atom, add it, mode <-2 recruse on rest
        1: find anything else: syntax error
        2: find a list: add a ',' plus the result of recursing on it in mode 0, and recurse on rest in mode 2
        2: find an atom, add a ',' plus it,  recruse on rest in mode 2
        2: find an empty list: add a ')' and return res

2: find an emply list, add ) and terminate
        """
        if not expLis:
            if mode == 2:
                return res + ')'
            else:
                raise SyntaxError('unexpected EOF')
        elif type(expLis)==str and len(expLis)==1:
            expLis = ['|',expLis]
        token = expLis.pop(0)
        if type(token) == list:
            if mode==0:
                raise SyntaxError('expected function, got expression:\t' + str(token))
            elif mode==1: # looking for 1st arg
                return self.pModal(expLis,2, res + self.pModal(token))
            else: # mode = 2, looking for more args or the end
                return self.pModal(expLis,2, res +',' + self.pModal(token))
        else: #an atom
            if mode==0:
                if token not in  SExpParser.evalFuncDict.keys():
                    raise SyntaxError("expected function, got:\t" +str(token))
                return self.pModal(expLis,
                                   1,
                                   res +  SExpParser.evalFuncDict[token])
            elif mode == 1: # looking for 1st arg
                if token not in  SExpParser.atoms:
                    raise SyntaxError('expected atom, got:\t' +str(token))
                else:
                    return self.pModal(expLis,
                                       2,
                                       res+token)
            else: #mode 2
                return self.pModal(expLis,
                                   2,
                                   res + ',' + token)

    
