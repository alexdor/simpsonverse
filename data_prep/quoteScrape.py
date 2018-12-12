import sqlite3
import os
import re
from bs4 import BeautifulSoup as bs
import string
print(os.getcwd())
conn = sqlite3.connect('simpsons.sqlite3')
c = conn.cursor()
quoteDict={}
quoteList=[]

x=c.execute('Select response_quotes From episodes;')
for quote in x.fetchall():
        soup=bs(str(quote),'html.parser')
        awesomestuff=soup.find_all("dd")
        for stuff in awesomestuff:
                quoteList.append(stuff)
f=open("unfilteredQuotes.txt",'w')
for line in quoteList:
        f.write(str(str(line).encode('UTF-8')))
f.close()


f=open("unfilteredQuotes.txt",'r')
r=f.readlines()
s=r[0]
quoteList=s.split('</dd>')
filteredQuotes=[]
for line in quoteList:
    line=str(line)
    line=line.lower()
    line=re.sub(r'<a.*?href=".*?>',"",line)
    line=re.sub(r"<dd>"," ",line)
    line=re.sub(r"</dd>"," ",line)
    line=re.sub(r"<b>"," ",line)
    line=re.sub(r"</dd>"," ",line)
    line=re.sub(r"</a>"," ",line) 
    line=re.sub(r"b'"," ",line)
    line=re.sub(r"\<i\>(\s)*(\(|\[).*?(\)|\])(\s)*\<\/i\>"," ",line)
    line=re.sub(r"<i>"," ",line)
    line=re.sub(r"</i>"," ",line)
    line=re.sub(r"\[.*?(\]|(\\){1,4}n)"," ",line)
    line=re.sub(r"(\\){1,4}n"," ",line)
    line=re.sub(r"</b>(\s)*:"," splitsplitsplit ",line)
    line=re.sub(r"&amp;","",line)
    line=re.sub(r"\(.*?\)","",line)
    line=re.sub(r"\\\w\w\w","",line)
    line=re.sub(r'[^\w\s]','',line)
    line=line.replace("audio clip","")
    filteredQuotes.append(line)
f.close()
f=open("filteredQuotes.txt",'w')
#-------------------------write name and quote in filteredQuotes.txt-----------------
for line in filteredQuotes:
    if len(line.strip())!=0:
        check=line.split('splitsplitsplit ')
        line=line.replace(" b ","  ")
        if (len(check)==2):
            if (line[0]=='b' or line[0:2]==' b' or line[0:3]=='  b'):
                refer=line.find('b')
                f.write(str(line)[refer+1:]+'\n')
            else:
                f.write(str(line)+'\n')
f.close()



