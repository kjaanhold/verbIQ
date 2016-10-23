#!/usr/bin/env python

from syllabify import syllabify
import nltk

# Arpabet dictionary
arpabet = nltk.corpus.cmudict.dict()

# Constants
DORSALS = {'K', 'G', 'NG'}
LIQUIDS = {'L', 'R'}
VOICED_AF = {'V', 'DH', 'Z', 'ZH'}
AF = {'F', 'TH', 'S', 'SH', 'CH'} | VOICED_AF

# Ask for a word to score
strings = []
def userInput():
    string = raw_input("Enter a word to score (type Q once finished): ")
    strings.append(string)
    if string.lower() == "q":
        strings.remove("q")
        return strings
    userInput()

def translator(string):
    stringInArpabet = arpabet[string.lower()]
    arpabetInput = []
    if len(stringInArpabet) > 1:
        stringInArpabet = stringInArpabet[0]                        # If there are many results in arpabet for given word
        for string in stringInArpabet:                              # then use only one of these.
            arpabetInput.append(str(string))
        return (arpabetInput)
    if len(stringInArpabet) == 1:
        flattenedString = [val for sublist in stringInArpabet for val in sublist]
        for string in flattenedString:
            arpabetInput.append(str(string))
        return(arpabetInput)

def wcm(phonemes, *sylab):
    phonemes = translator(phonemes)
    syls = syllabify(phonemes) 
    score = 0

    if len(syls) > 2:
        score += 1                                                  # Productions with more than two syllables receive 1 point
    if len(syls) > 1 and not syls[0][1][-1].endswith('1'):
        score += 1                                                  # Productions with stress on any syllable but the first receive
    if syls[-1][2] != []:
        score += 1                                                  # Productions with a word-final consonant receive 1 point
    for syl in syls:
        if len(syl[0]) > 1:
            score += 1                                              # Productions with a sequence of two or more consonants within
        if len(syl[2]) > 1:                                         # a syllable receive one point for each cluster
            score += 1

    for syl in syls:
        score += sum(ph in DORSALS for ph in (syl[0] + syl[2]))     # Productions with a velar consonant receive 1 point for each
    for syl in syls:
        score += sum(ph in LIQUIDS for ph in (syl[0] + syl[2]))     # Productions with a liquid, a syllabic liquid, or a rhotic vowel
                                                                    # receive 1 point for each liquid, syllabic liquid, and rhotic vowel

        score += sum(len(ph) > 1 and ph[1] == 'R' for ph in syl[1]) # Productions with a fricative or affricate receive 1 point for
                                                                    # each fricative and affricate
        score += sum(ph in AF for ph in (syl[0] + syl[2]))
    for syl in syls:
        score += sum(ph in VOICED_AF for ph in (syl[0] + syl[2]))   # Productions with a voiced fricative or affricate receive 1 point
                                                                    # for each fricative and affricate (in addition to the point received
                                                                    # for #3)
    return score

# Call the function with input word
userInput()
for string in strings:
    print(string + ": " + str(wcm(string)))

