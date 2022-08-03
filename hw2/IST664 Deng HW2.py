import json
import csv



f = open('C:/Users/gg/Desktop/SPRING2021/IST664/hw1/01.json',encoding="utf-8")
p = f.readlines()
data1 = [json.loads(i) for i in p]
f = open('C:/Users/gg/Desktop/SPRING2021/IST664/hw1/02.json',encoding="utf-8")
p = f.readlines()
data2 = [json.loads(i) for i in p]

data3=data1+data2


dict1={}
dict1['author']=[d['author'] for d in data3]
dict1['facebook']=[d['thread']['social']['facebook'] for d in data3]
dict1['title']=[d['title'] for d in data3]
dict1['published']=[d['published'] for d in data3]
dict1['url']=[d['url'] for d in data3]
dict1['replies_count']=[d['thread']['replies_count'] for d in data3]
dict1['country']=[d['thread']['country'] for d in data3]
dict1['facebook']=[str(d)for d in dict1['facebook']]

[dict2={}
dict2['text']= d['text'] for d in data3]]

sentanalyze=[]

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import brown
from nltk.tag import pos_tag, map_tag
brown_news_tagged = brown.tagged_words(categories='news', tagset='universal')
tag_fd = nltk.FreqDist(tag for (word, tag) in brown_news_tagged)

def adjor(w):
    j=word_tokenize(w)
    k=[(word, map_tag('en-ptb', 'universal', tag)) for word, tag in pos_tag(j)]
    for (a,b) in k:
        if a == '!' or b == 'ADJ':
            return True
        else:
            return False

def extractsent(a):
    for sent in sent_tokenize(a):
        if adjor(sent):
            sentanalyze.append(sent)


for d in dict2['text']:
    extractsent(d)

calc=0
for d in sentanalyze:
    calc+=len(d)
calc/len(sentanalyze)


def adjorize(w):
    j=word_tokenize(w)
    k=[(word, map_tag('en-ptb', 'universal', tag)) for word, tag in pos_tag(j)]
    return k

wordanalyze=[]
for d in sentanalyze:
    wordanalyze.append(adjorize(d))
flatword = []
for b in wordanalyze:
    for c in b:
        flatword.append(c)

word_tag_fd = nltk.FreqDist(flatword)

mostfreqAdj=[wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1] == 'ADJ']
mostfreqAdj[:50]
mostfreqVerb=[wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1] == 'VERB']
mostfreqVerb[:50]
mostfreqNoun=[wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1] == 'NOUN']
mostfreqNoun[:50]