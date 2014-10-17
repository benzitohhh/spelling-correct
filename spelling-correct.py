import re, collections

def words(text): return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('big.txt').read())) ## approx 1million words
    
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]       ## one char deleted
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]   # transpose (switch) chars
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]  ## 'or' shortcircuits here (like || in js) - first non-empty set is returned
    return max(candidates, key=NWORDS.get)

print correct('speling')

# BEN NOTES:

# logical shortcircuits (for lazy execution) - i.e. 'or' etc... Results of set 

# defaultdict(lambda: 1)  ## i.e. lowest freq is 2

# for list comprehensions below...
#   "if b"         -> excludes if b is empty-string (as empty string is falsy in python)
#   "if len(b)>1"  -> exclues if b is less than 2 chars in length

# python concat lists with "+" operator

#import heapq
from pprint import pprint

def top5(candidates):
    return sorted([(NWORDS[x], x) for x in candidates], reverse=True)[:5]

def correctB(word):
    one = known(edits1(word))
    two = topN(known_edits2(word), 5)
    original = [word]
    return {
        'original': top5(original),
        'one edit': top5(one),
        'two edits': top5(two)
    }

# pprint(correctB('corract'))
    
