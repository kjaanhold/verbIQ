from wcm import *
from numpy import *
from soundex import soundex_distance
import pandas as pd
import scipy.stats as stats
import itertools
from StringIO import StringIO

# Define user inputs
name = raw_input("Enter your kid's name: ")
age = raw_input("Enter your kid's age (in months): ")
words = raw_input("Enter the pronunciation of words your kid spoke (separated by comma): ")


# Add words to vector and score them
word_vector = words.split(', ')
word_scores = []
unknown_words = []

words_meanings = {}
for word in word_vector:
    words_meanings[word] = raw_input("Enter the meaning of " + str(word) + " (may leave blank if correctly pronounced): ")

soundex_scores = []
for key in words_meanings:
    soundex_scores.append(soundex_distance(key,words_meanings[key]))

for string in words_meanings:
    if not words_meanings[string]:
        try:
            word_scores.append(wcm(string))
        except:
            unknown_words.append(words_meanings[string])
    else:
        try:
            word_scores.append(wcm(words_meanings[string]))
        except:
            unknown_words.append(words_meanings[string])

# Read in comparison data
data = pd.read_csv('output.csv',dtype={'data_id':int,'age':int,'sex':object,'mom_ed':object,
                                       'value':object,'item_id':object,'type':object,'category':object,
                                       'definition':object,'score':int})

# Subset of same age data
sameage_data = data[data['age']==int(age)]

# Soundex
soundex_differences = []
for i,j in itertools.combinations(word_vector,2):
    soundex_differences.append(soundex_distance(i,j))

# Aggregate scores for each kid
max_scores = (sameage_data.groupby('data_id')['score'].max()).values.tolist()
avg_scores = (sameage_data.groupby('data_id')['score'].mean()).values.tolist()
var_scores = (sameage_data.groupby('data_id')['score'].var()).values.tolist()

# Aggregate scores for agegroup
max_scores_age = sameage_data.groupby('age')['score'].max().values.tolist()
avg_scores_age = sameage_data.groupby('age')['score'].mean().values.tolist()
var_scores_age = sameage_data.groupby('age')['score'].var().values.tolist()

print(" ")
print("Your kid:")
print("Average WCM score: " + str(round(mean(word_scores),3)))
print("Maximum WCM score: " + str(round(max(word_scores),3)))
print("Variance of WCM score: " + str(round(var(word_scores),3)))
print("Average pair-wise soundex difference: " + str(round(mean(soundex_differences),2)))
print("Pronounced word vs real meaning average soundex difference: " + str(round(mean(soundex_scores),2)))
if unknown_words:
    print("Unkown words: " + str(', '.join(str(e) for e in unknown_words)))

print(" ")
print("Average WCM score in this age: " + str(round(avg_scores_age[0],3)))
print("Maximum WCM score in this age: " + str(round(max_scores_age[0],3)))
print("Variance of WCM scores in this age: " + str(round(var_scores_age[0],3)))

print(" ")
print("Your kid's average WCM score is higher than " + str(round(stats.percentileofscore(avg_scores,mean(word_scores)),3)) + "% of others in same age!")
print("Your kid's maximum WCM score is higher than " + str(round(stats.percentileofscore(max_scores,max(word_scores)),3)) + "% of others in same age!")
#print("Your kid's variance of WCM score is higher than " + str(round(stats.percentileofscore(var_scores,var(word_scores)),3)) + "% of others in same age!")