import json
import os
from nltk.tokenize import word_tokenize
import urllib.request
from numba import jit
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean,stdev
import heapq

sentimentDict={}
filePath = 'https://journals.plos.org/plosone/article/file?type=supplementary&id=info%3Adoi%2F10.1371%2Fjournal.pone.0026752.s001'
response = urllib.request.urlopen(filePath)
data = response.read()
text = data.decode('utf-8')
for line in text.split('\n')[4:]:
    listThing=line.split('\t')
    if len(listThing) > 3:
        sentimentDict[listThing[0]]=[listThing[2],listThing[3]]

#Global services 800-992-4685

#opersations 877-742-9488

#@jit(cache=True)
def sentiment(list_of_tokens):
    sentiment_num=0
    sentiment_denom=0
    for token in list_of_tokens:
        if sentimentDict.get(token):
            sentiment_num+=float(sentimentDict[token][0])
            sentiment_denom+=1
    return (sentiment_num,sentiment_denom)


os.chdir("/media/removable/sdcard/SimpsonsGit/social-graphs-team/final_assigment")
with open('characterQuotesBySeason.json') as f:
    data = json.load(f)
f.close()

personScoresPerSeason={}
happyScores={}
numberOfWords={}
characterIndividWordScores={}


for season in data: 
    for person in data[season].keys():
        strippedName=person.strip()
        if not characterIndividWordScores.get(strippedName):
            characterIndividWordScores[strippedName]={'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0}
        
        for word in word_tokenize(data[season][person]):
            try:
                characterIndividWordScores[strippedName][str(int(round(sentiment([word])[0])))]+=1
            except:
                pass
        #actualWords[strippedName]=[(x,sentiment([x])[0]) for x in word_tokenize(data[season][person])]
        val=sentiment(word_tokenize(data[season][person]))
        if not numberOfWords.get(strippedName):
            numberOfWords[strippedName]=0
        numberOfWords[strippedName]+=len(word_tokenize(data[season][person]))
        if not personScoresPerSeason.get(strippedName):
            personScoresPerSeason[strippedName]=[]
        personScoresPerSeason[strippedName].append(val)
      
for person in personScoresPerSeason:
    numerator=0
    denominator=0
    for item in personScoresPerSeason[person]:
        numerator+=item[0]
        denominator+=item[1]
    if denominator!=0:
        happyScores[person]=numerator/denominator
    else:
        happyScores[person]=''




k_keys_sorted = heapq.nlargest(20, numberOfWords, key=numberOfWords.get)

finalArr=[(x,happyScores[x],characterIndividWordScores[x]) for x in k_keys_sorted]
finalDict={}

for i in range(len(k_keys_sorted)):
    finalDict[k_keys_sorted[i]]=[happyScores[k_keys_sorted[i]],characterIndividWordScores[k_keys_sorted[i]] ]


nameHere=input("input a name. for a list of names, type 'help'.")
if nameHere=='help':
    for name in finalDict.keys():
        print(name)
else:        
    pos = np.arange(len(finalDict[nameHere][1])
    width = 1.0     # gives histogram aspect to the bar diagram

    ax = plt.axes()
    ax.set_xticks(pos + (width / 2))
    ax.set_xticklabels(myDictionary.keys())

    plt.bar(finalDict[nameHere][1].keys(), finalDict[nameHere][1].values(), width, color='g')
    plt.show()
print()
