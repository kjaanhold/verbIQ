
## 1. Install nltk through terminal using:
`sudo pip install -U nltk`

## 2. Launch Python through terminal and type:
1. `import nltk` 
2. `nltk.download()` 

## 3. From the GUI that launched, go to corpora and install cmudict. 

## 4. Manual way to translate words to arpabet:
1. `arpabet = nltk.corpus.cmudict.dict()`
2. `print(arpabet["string"])`

For example:

`print(arpabet["carpet"])`

Returns: [[u'K', u'AA1', u'R', u'P', u'AH0', u'T']]
