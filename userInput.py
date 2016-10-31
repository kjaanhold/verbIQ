from wcm import *
from numpy import *
import pandas as pd
import scipy.stats as stats
from StringIO import StringIO

# Define user inputs
name = raw_input("Enter your kid's name: ")
age = raw_input("Enter your kid's age (in months): ")
words = raw_input("Enter the words your kid spoke (separated by comma): ")

# Add words to vector and score them
word_vector = words.split(', ')
word_scores = []
unkown_words = []

for string in word_vector:
    try:
        word_scores.append(wcm(string))
    except:
        unkown_words.append(word_vector.pop(word_vector.index(string)))


print(" ")
print("Your kid:")
print("Average WCM score: " + str(round(mean(word_scores),3)))
print("Maximum WCM score: " + str(round(max(word_scores),3)))
print("Variance of WCM score: " + str(round(var(word_scores),3)))
print("Unkown words: " + str(''.join(str(e) for e in unkown_words)))

# Read in comparison data
data = pd.read_csv('output.csv',dtype={'data_id':int,'age':int,'sex':object,'mom_ed':object,
                                       'value':object,'item_id':object,'type':object,'category':object,
                                       'definition':object,'score':int})

# Subset of same age data
sameage_data = data[data['age']==int(age)]

# Aggregate scores for each kid
max_scores = (sameage_data.groupby('data_id')['score'].max()).values.tolist()
avg_scores = (sameage_data.groupby('data_id')['score'].mean()).values.tolist()
var_scores = (sameage_data.groupby('data_id')['score'].var()).values.tolist()

# Aggregate scores for agegroup
max_scores_age = sameage_data.groupby('age')['score'].max().values.tolist()
avg_scores_age = sameage_data.groupby('age')['score'].mean().values.tolist()
var_scores_age = sameage_data.groupby('age')['score'].var().values.tolist()

print(" ")
print("Average WCM score in this age: " + str(round(avg_scores_age[0],3)))
print("Maximum WCM score in this age: " + str(round(max_scores_age[0],3)))
print("Variance of WCM scores in this age: " + str(round(var_scores_age[0],3)))

print(" ")
print("Your kid's average WCM score is higher than " + str(round(stats.percentileofscore(avg_scores,mean(word_scores)),3)) + "% of others in same age!")
print("Your kid's maximum WCM score is higher than " + str(round(stats.percentileofscore(max_scores,max(word_scores)),3)) + "% of others in same age!")
#print("Your kid's variance of WCM score is higher than " + str(round(stats.percentileofscore(var_scores,var(word_scores)),3)) + "% of others in same age!")