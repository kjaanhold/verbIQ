from wcm import *
from numpy import *

# Define user inputs
name = raw_input("Enter your kid's name: ")
age = raw_input("Enter your kid's age (in months): ")
words = raw_input("Enter the words your kid spoke (separated by comma): ")

# Add words to vector and score them
word_vector = words.split(', ')
word_scores = []

for string in word_vector:
    word_scores.append(wcm(string))

print(" ")
print("Your kid:")
print("Average WCM score: " + str(mean(word_scores)))
print("Maximum WCM score: " + str(max(word_scores)))
print("Variance of WCM score: " + str(var(word_scores)))

# Read in comparison data
with open('output.csv', 'rb') as f:
    reader = csv.reader(f)
    word_list = list(reader)

sameage_scores = []
for elem in range(1,len(word_list)):
    if word_list[elem][1] == age:
        sameage_scores.append(word_list[elem][9])

sameage_scores = array(sameage_scores).astype(float)

print(" ")
print("Average scores in this age: ")
print("Average WCM score: " + str(mean(sameage_scores)))
print("Maximum WCM score: " + str(max(sameage_scores)))
print("Variance of WCM score: " + str(var(sameage_scores)))