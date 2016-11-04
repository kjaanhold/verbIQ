import fuzzy
import itertools

soundex = fuzzy.Soundex(4)

def soundex_distance(a,b):
    a = list(str(soundex(a)))
    b = list(str(soundex(b)))
    counter = 0
    for i in range(0,4):
        if a[i] == b[i]:
            counter += 1
    return 1-(counter/4.0)