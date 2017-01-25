# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis and Shay Cohen
# Revised November 2016 by Adam Lopez

# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
        #use a dictionary with categories as keys and keep a list of stems
    def __init__(self):
        self.allLexes={}
    def add(self,stem,cat):
        stemCatList = self.allLexes.get(cat)
        # Checks that the list is not empty
        if (not stemCatList):
            # If the list does not exist then create a new, empty list
            stemCatList=[]
        # Add the stem to the list 
        stemCatList.append(stem)
        # Replace the cat item in the dictionary with the new, updated list  
        self.allLexes[cat]=stemCatList
    def getAll(self,cat):
        catLexes = self.allLexes.get(cat)
        all=[]
        # Checks that the list is not empty
        if (catLexes):
            for elem in catLexes:
                 add(all,elem)
        return all
    

class FactBase:
    # Initialisation method
    def __init__(self):
        self.unaryList=[]
        self.binaryList=[]
    
    # Add an item to the unary list    
    def addUnary(self,pred,e1):
        self.unaryList.append((pred,e1))
        
    # Add an item to the binary list    
    def addBinary(self,pred,e1,e2):
        self.binaryList.append((pred,e1,e2))
        
    # Search for an item in the unary list    
    def queryUnary(self,pred,e1):
        return (pred,e1) in self.unaryList
        
    # Search for an item in the binary list
    def queryBinary(self,pred,e1,e2):
        return (pred,e1,e2) in self.binaryList

import re
from nltk.corpus import brown 

# Massively reduces computation time if brownTags is declared as a global variable and if declared as set (to remove duplicates)
brownTags = set(brown.tagged_words())

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    

    
    # If the stem ends in anything except s,x,y,z,ch,sh or a vowel, simply add s
    if (re.match(r"\w*([^aeiousxyzh]|[^cs]h)s$",s)):
        stem = s[0:len(s)-1]
        # Checks that the word is actually a verb
        if ((stem,"VB") in brownTags or (s,"VBZ") in brownTags or (stem in ['has','is','do'])):
            return stem
        else:
            return ""
        
    # If the stem ends in y preceded by a vowel, simply add s
    elif (re.match(r"\w*[aeiou]ys$",s)):
        stem = s[0:len(s)-1]
        if ((stem,"VB") in brownTags or (s,"VBZ") in brownTags or (stem in ['has','is','do'])):
            return stem
        else:
            return ""
        
    # If the stem ends in y preceded by a non-vowel and contains at least three letters, change the y to ies
    elif (re.match(r"\w+[^aeiou]ies$",s)):
        stem = s[0:len(s)-3]+"y"
        if ((stem,"VB") in brownTags or (s,"VBZ") in brownTags or (stem in ['has','is','do'])):
            return stem
        else:
            return ""
        
    # If the stem is of the form Xie where X is a single letter other than a vowel, simply add s
    elif (re.match(r"^\wies$",s)):
        stem = s[0:len(s)-1]
        if ((stem,"VB") in brownTags or (s,"VBZ") in brownTags or (stem in ['has','is','do'])):
            return stem
        else:
            return ""
        
    # If the stem ends in o,x,ch,sh,ss or zz, add es
    elif (re.match(r"\w*(o|x|ch|sh|ss|zz)es$",s)):
        stem = s[0:len(s)-2]
        if ((stem,"VB") in brownTags or (s,"VBZ") in brownTags or (stem in ['has','is','do'])):
            return stem
        else:
            return ""
        
    # If the stem ends in se or ze but not in sse or zze, add s
    elif (re.match(r"\w*(se|ze)s$",s) and (not re.match(r"\w*(sse|zze)s$",s))):
        stem = s[0:len(s)-1]
        if ((stem,"VB") in brownTags or (s,"VBZ") in brownTags or (stem in ['has','is','do'])):
            return stem
        else:
            return ""
        
    # If the stem is have, its 3s form is has
    elif (s=="has"):
        return "have"
        
    # Otherwise, if the stem ends in e not preceded by i,o,s,x,z,ch,sh, just add s
    elif (re.match(r"\w*es$",s) and not re.match(r"\w*(i|o|s|x|z|ch|sh)es$",s)):
        stem = s[0:len(s)-1]
        if ((stem,"VB") in brownTags or (s,"VBZ") in brownTags or (stem in ['has','is','do'])):
            return stem
        else:
            return ""
    else:
        return ""

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
        

# End of PART A.

