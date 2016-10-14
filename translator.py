import nltk

arpabet = nltk.corpus.cmudict.dict()

string = input("Enter a string in quotes: ")

stringInArpabet = arpabet[string]

# Flatten the list of lists
flattenedString = [val for sublist in stringInArpabet for val in sublist]
arpabetInput = []

for string in flattenedString:
    arpabetInput.append(str(string))

print(arpabetInput)