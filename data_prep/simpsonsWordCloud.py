from numba import jit
from nltk import word_tokenize
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt
import math
#create quote dictionary from filteredQuotes
f=open("filteredQuotes.txt",'r')
characterQuotes={}
r=f.read()
text=r.split('\n')
for quote in text: 
    character=quote.split('splitsplitsplit')[0]
    split_quote=quote.split()[1:]
    try: 
        split_quote.remove('splitsplitsplit')
    except:
        pass
    characters=character.split(' and ')
    for person in characters:
        person =person.strip()
        if characterQuotes.get(person):
                characterQuotes[person]+=split_quote
        else:
                characterQuotes[person]=split_quote
f.close()

#create documents for tf-idf
documents=[]
characterName=[]
for person in characterQuotes.keys():
    if len(characterQuotes[person])>400:
        quotes=characterQuotes[person]
        strQuotes=" ".join(quotes)
        tokens=word_tokenize(strQuotes)
        listToks=sorted(tokens)
        documents.append(listToks)
        characterName.append(person)

documentsWithUniqueWords = [sorted(set(x)) for x in characterQuotes.values() if len(x)>400]
documentsLength = len(documents)

# Calculate the tf-idf of a word
#@jit(cache=True)
def tfIdf(word, text):
    # Count how many documents include the word
    count = 0
    for document in documentsWithUniqueWords:
        if word in document:
            count += 1
    # Calculate the idf of the word
    idf = math.log( documentsLength / count)
    if (text.count(word) / len(text)) * idf >1:
        print(word+" "+(text.count(word) / len(text)) * idf)
    return (text.count(word) / len(text)) * idf


# Calculate and return a string in the way that the wordcloud library wants it, using the tf-idf algorithm
#@jit(cache=True)
def getWorldCloudStringFromADocument(document, documentWithUniqueWords):
    finalWords = []
    for word in documentWithUniqueWords:
        try:
            wordAppearance = tfIdf(word, document)*1000
        except:
            raise
        if wordAppearance > 0:
            for _ in range(round(wordAppearance)):
                finalWords.append(word)
            # finalWords.append(wordAppearance)
    return finalWords

# An array with all the strings for the wordcloud
res = []
resCharacterNames=[]
for documentIndex in range(len(documents)):
    if len(documents[documentIndex])!=0:
        wordList = getWorldCloudStringFromADocument(documents[documentIndex], documentsWithUniqueWords[documentIndex])
        res.append(wordList)
        resCharacterNames.append(characterName[documentIndex])
#set each list as a string for the word cloud
res = [" ".join(text) for text in res ]

#Generate cloud based on user input
cloudInput=input("Type the name of a character to see their word cloud. For a list of characters, type 'help'.")

if cloudInput.lower()=='help':
    for character in characterName:
        print(character)
elif cloudInput in characterName:
    wordCloud = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='white',
                          width=2000,
                          height=1000,
                          collocations=False
                         ).generate(res[characterName.index(cloudInput)])
    plt.figure(figsize=(20,10))
    plt.imshow(wordCloud)
    plt.axis('off')
    plt.figtext(0.5,0.9,cloudInput+" Wordcloud:\n",fontsize=30, ha='center')
    plt.show()
else: 
    print("You entered an unavailable character or something not recognized as a name."+"\n"+"For a list of available characters, enter 'help'.")
    
