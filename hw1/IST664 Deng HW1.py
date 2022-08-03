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

dict2={}
dict1['text']=[ryzen5990x(d['text']) for d in data3]


import nltk
import re
def alpha_filter(w):
    pattern = re.compile('[^a-z]+')
    if (pattern.match(w)):
        return True
    else:
        return False
stopwords = nltk.corpus.stopwords.words('english')

def ryzen5990x(w):
    g=nltk.word_tokenize(w)
    k = [a.lower( ) for a in g]
    l = [b for b in k if not alpha_filter(b)]
    m = [c for c in l if c not in stopwords]
    return m


dict1['text']=[ryzen5990x(d['text']) for d in data3]

from nltk import FreqDist
fdistcountry=FreqDist(dict1['country'])
counting=0
for x in dict1['text']:
    counting+=len(x)

averagelength=counting/len(dict1['text'])
fdistcountry
averagelength



tokens=[]
for x in dict1['text']:
    tokens+=x

fdisttoken=FreqDist(tokens)
topkeys = fdisttoken.most_common(50)
for pair in topkeys:
    	print(pair)

tokenbigrams=list(nltk.bigrams(tokens))
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(tokens)
finder.apply_freq_filter(2)
scored = finder.score_ngrams(bigram_measures.raw_freq)
for a in scored[:50]:
    print(a)

bigram_measures = nltk.collocations.BigramAssocMeasures()
finder3 = BigramCollocationFinder.from_words(tokens)
finder3.apply_word_filter(alpha_filter)
finder3.apply_word_filter(lambda x: x in stopwords)
finder3.apply_freq_filter(5)
scored3 = finder3.score_ngrams(bigram_measures.pmi)
for extra in scored3[:50]:
    print(extra)



import pandas as pd
df = pd.DataFrame.from_dict(dict1, orient="index")
df.to_csv("data.csv",header=dict1.keys())


