# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis and Shay Cohen
# Revised November 2016 by Adam Lopez

# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    with open("sentences.txt", "r") as f:
        stems = []
        nouns = {}
        for line in f:
            
            # Splits the file into groups of "a|b" where a is the word and b is the pos
            items = line.split(" ")
            for pairs in items:
                # Splits pair of "a|b" into word=a and pos=b
                word = pairs.split("|")[0]
                pos = pairs.split("|")[1]
                
                # Checks if the pos is equal to NNS and then checks if that has already been taged as NN
                if (pos == "NNS"):
                    if (nouns.get(word) == "NN"):
                        stems.append(word)
                    else:
                        nouns[word] = pos
                
                # Checks if the pos is equal to NN and then checks if that has already been tagged as NNS
                if (pos == "NN"):
                    if (nouns.get(word) == "NNS"):
                        stems.append(word)
                    else:
                        nouns[word] = pos

    return list(set(stems))
    
unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    if (s in unchanging_plurals_list):
        return s
        
    # If the noun stem ends in -f or -fe, the plural is obtained by replacing this with v and adding -es
    elif (re.match(r"\w*ves$",s)):
        return s[0:len(s)-3]+'f'
    
    
    # All of the below is copied from the statements.py file (because 3s rules applies here)
    elif (re.match(r"\w*([^aeiousxyzh]|[^cs]h)s$",s)):
        stem = s[0:len(s)-1]
        return stem
        
    # If the stem ends in y preceded by a vowel, simply add s
    elif (re.match(r"\w*[aeiou]ys$",s)):
        stem = s[0:len(s)-1]
        return stem
        
    # If the stem ends in y preceded by a non-vowel and contains at least three letters, change the y to ies
    elif (re.match(r"\w+[^aeiou]ies$",s)):
        stem = s[0:len(s)-3]+"y"
        return stem
        
    # If the stem is of the form Xie where X is a single letter other than a vowel, simply add s
    elif (re.match(r"^\wies$",s)):
        stem = s[0:len(s)-1]
        return stem
        
    # If the stem ends in o,x,ch,sh,ss or zz, add es
    elif (re.match(r"\w*(o|x|ch|sh|ss|zz)es$",s)):
        stem = s[0:len(s)-2]
        return stem
        
    # If the stem ends in se or ze but not in sse or zze, add s
    elif (re.match(r"\w*(se|ze)s$",s) and (not re.match(r"\w*(sse|zze)s$",s))):
        stem = s[0:len(s)-1]
        return stem
        
    # If the stem is have, its 3s form is has
    elif (s=="has"):
        return "have"
        
    # Otherwise, if the stem ends in e not preceded by i,o,s,x,z,ch,sh, just add s
    elif (re.match(r"\w*es$",s) and not re.match(r"\w*(i|o|s|x|z|ch|sh)es$",s)):
        stem = s[0:len(s)-1]
        return stem
        
    else:
        return ""

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    possTags = []
    
    # Find all of the lexes using the Lexicon class from statements
    lexP = lx.getAll("P")
    lexI = lx.getAll("I")
    lexA = lx.getAll("A")
    lexT = lx.getAll("T")
    lexN = lx.getAll("N")
    
    # Assign the noun stem/verb stem to the variables
    nounStem = noun_stem(wd)
    verbStem =verb_stem(wd)
    
    # Check if the word is in the function words and if it is then adds the associated tag
    for item in function_words_tags:
        if (item[0] == wd):
            possTags.append(item[1])
                
    # Goes through all possible cases to add all of the possible tags to the list
    if(wd in lexP):
        possTags.append("P")
        
    # Checks the verb stem
    if(verbStem in lexI):
        possTags.append("Is")

    # Checks the word
    if(wd in lexI):
       possTags.append("Ip")
    
    # Checks the verb stem
    if(verbStem in lexT):
        possTags.append("Ts")        
        
    # Checks the word
    if(wd in lexT):
        possTags.append("Tp")
    
    if(wd in lexA):
        possTags.append("A")
        
    # Checks the word
    if(wd in lexN):
       possTags.append("Ns")
    
    # Checks the noun stem
    if(nounStem in lexN):
        possTags.append("Np")
        
    return possTags

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.

