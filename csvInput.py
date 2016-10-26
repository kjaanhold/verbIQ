from wcm import *

# Read input csv
with open('output.csv', 'rb') as f:
    reader = csv.reader(f)
    word_list = list(reader)

# Call WCM only for single words (ie not "a lot")
for elem in range(1, len(word_list)):
    if (' ' in word_list[elem][8]) == False:
        try:
            word_list[elem].append(wcm(word_list[elem][8]))
        except:
            pass

# Create a list of scored words
final_list = []
for elem in range(1,len(word_list)):
    if len(word_list[elem]) == 10:
        final_list.append(word_list[elem])

print(final_list)

# Write the results to a csv.
with open("new_output.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(final_list)
