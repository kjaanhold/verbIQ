import fuzzy

soundex = fuzzy.Soundex(4)

def soundex_distance(a,b):
    a = list(str(soundex(a)))
    b = list(str(soundex(b)))
    counter = 0
    for i in range(0,4):
        if a[i] == b[i]:
            counter += 1
    return 1-(counter/4.0)

print("Said: father \nMeant: mother \nSoundex difference: " + str(soundex_distance("mother","father")))
print("\nSaid: farmer \nMeant: father \nSoundex difference: " + str(soundex_distance("father","farmer")))
print("\nSaid: farmer \nMeant: mother \nSoundex difference: " + str(soundex_distance("mother","farmer")))
