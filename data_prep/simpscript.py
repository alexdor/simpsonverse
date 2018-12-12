import json
import os
from urllib import request
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop = stopwords.words("english")

episodeDict={}
episodeDict[1]=13
episodeDict[2]=22
episodeDict[3]=24
episodeDict[4]=22
episodeDict[5]=22
episodeDict[6]=25
episodeDict[7]=25
episodeDict[8]=25
episodeDict[9]=25
episodeDict[10]=23
episodeDict[11]=22
episodeDict[12]=21
episodeDict[13]=22
episodeDict[14]=22
episodeDict[15]=22
episodeDict[16]=21
episodeDict[17]=22
episodeDict[18]=22
episodeDict[19]=20
episodeDict[20]=21
episodeDict[21]=23
episodeDict[22]=22
episodeDict[23]=22
episodeDict[24]=22
episodeDict[25]=22
episodeDict[26]=22
episodeDict[27]=22
episodeDict[28]=22
episodeDict[29]=21
episodeDict[30]=1

os.chdir("/media/removable/sdcard/SimpsonsGit/social-graphs-team/final_assigment")
for season in episodeDict.keys():
    for episode in range(episodeDict[season]):
        seasonurl=str(season).zfill(2)
        episodeurl=str(episode+1).zfill(2)
        try:
            req=request.urlopen('https://www.springfieldspringfield.co.uk/view_episode_scripts.php?tv-show=the-simpsons&episode=s'+seasonurl+'e'+episodeurl)
            text=str(req.read())
            text=re.sub(r'.*?<div class="scrolling-script-container">',"",text)
            text=re.sub(r'</div>.*',"",text)
            text=re.sub(r'</div>.*',"",text)
            text = text.lower()
            text = text.replace("\\r", " ").replace("\\n", " ").replace("\\t", " ").replace("<br>", " ")
            text = re.sub(r"[^\w\s]", " ", text)
            text = re.sub(r"rt\t", " ", text)
            text = re.sub(r"\d+", " ", text)
            text = " ".join([word for word in text.split() if word not in stop])


            f=open("episodeScripts/season"+seasonurl+"episode"+episodeurl+".txt",'w')
            f.write(text)
            f.close()
        
        except:
            pass
        print("season "+seasonurl+" episode "+episodeurl)

