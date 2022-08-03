import os
path1= 'C:/Users/d2844/Desktop/SPRING2021/IST664/groupproject/aclImdb/test/neg'
path2= 'C:/Users/d2844/Desktop/SPRING2021/IST664/groupproject/aclImdb/test/pos'
path3= 'C:/Users/d2844/Desktop/SPRING2021/IST664/groupproject/aclImdb/train/neg'
path4= 'C:/Users/d2844/Desktop/SPRING2021/IST664/groupproject/aclImdb/train/pos'

datapath=[path1,path2,path3,path4]
dataset=[]
def read_text_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        dataset.append(f.read())

for path in datapath:
    os.chdir(path)
    for file in os.listdir():
    # Check whether file is in text format or not
        if file.endswith(".txt"):
            file_path = f"{path}\{file}"
            read_text_file(file_path)


import nltk
from nltk.corpus import sentence_polarity
import random
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import brown
from nltk.tag import pos_tag, map_tag
import nltk.classify

traintest=[]
for d in dataset:
    for sent in sent_tokenize(d):
        scores = SentimentIntensityAnalyzer().polarity_scores(sent)
        if scores['compound']>=0.05:
            traintest.append((word_tokenize(sent),'pos'))
        if scores['compound']> -0.05 and scores['compound']<0.05:
            traintest.append((word_tokenize(sent),'neu'))
        if scores['compound']< -0.05:
            traintest.append((word_tokenize(sent),'neg'))

dataset1=dataset
traintest1=traintest


newtrain=[]

for a in traintest:
    btemp=''
    for d in a[0]:
        btemp+=' '
        btemp+=d
    newtrain.append((btemp,a[1]))

sent=[]
for d in newtrain:
    sent.append(d[0])

label=[]
for d in newtrain:
    label.append(d[1])
dict = {'sent': sent, 'label': label}
import csv
f = open('trainset.csv','w', encoding="utf-8")
w = csv.DictWriter(f,dict.keys())
w.writeheader()
w.writerow(dict)
f.close()
#write dict into csv