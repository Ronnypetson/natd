from random import randint
from enum import Enum, unique

# T, F, ^, ~
# up to 20 atoms
#
n_atoms = 20

def genAtom():
    return chr(ord('a')+randint(0,n_atoms-1))

def genProp(n):  # Generates radom formula with n symbols in prefix notation
    if n == 1:
        return genAtom()
    elif n == 2:
        return '~'+genAtom()
    else:
        if randint(0,1) == 1:
            return '~'+genProp(n-1)
        else:
            l = randint(1,n-2)
            r = (n-1)-l
            return '^'+genProp(l)+genProp(r)

def getArgs(and_prop):
    if len(and_prop) < 3:
        print('Parameter and_prop is too small')
    l_end = 1
    atoms_left = 1
    while l_end < len(and_prop):
        if and_prop[l_end] == '^':
            atoms_left += 1
        elif and_prop[l_end] != '~':
            atoms_left -= 1
        
        if atoms_left == 0:
            return [and_prop[1:l_end+1],and_prop[l_end+1:len(and_prop)]]
        l_end += 1
    return [None,None]

def isNeg(a,b):
    if len(a) > 1 and a[0] == '~' and a[1:] == b:
        return True
    return False

def hasContr(Hyp,p):
    if len(p) < 2:
        for prop in Hyp:
            if len(prop) < 2:
                continue
            elif prop[0] == '~' and prop[1:] == p:
                return True
    else:
        for prop in Hyp:
            if len(prop) < 2 and p[0] == '~' and p[1:] == prop:
                return True
            elif (p[0] == '~' and p[1:] == prop) or (prop[0] == '~' and prop[1:] == p):
                return True
    return False

#
#and_ = '^'+genProp(randint(5,10))+genProp(randint(5,10))
#print(and_)
#print(getArgs(and_))

@unique
class Rule(Enum):
    AND_Elim_L = 0
    AND_Elim_R = 1
    AND_Intr = 2
    NOT_Intr = 3
    F_Elim = 4
    NOT_Elim = 5
    Hyp_Intr = 6

#class Prop:
#    def __init__(self,body,depth):
#        self.body = body
#        self.depth = depth

