
import json
import csv
#impot json and csv



f = open('C:/Users/d2844/Desktop/SPRING2021/IST664/hw1/01.json',encoding="utf-8")
p = f.readlines()
data1 = [json.loads(i) for i in p]
f = open('C:/Users/d2844/Desktop/SPRING2021/IST664/hw1/02.json',encoding="utf-8")
p = f.readlines()
data2 = [json.loads(i) for i in p]

data3=data1+data2
#read the data and join two data

dict1={}
dict1['author']=[d['author'] for d in data3]
dict1['facebook']=[d['thread']['social']['facebook'] for d in data3]
dict1['title']=[d['title'] for d in data3]
dict1['published']=[d['published'] for d in data3]
dict1['url']=[d['url'] for d in data3]
dict1['replies_count']=[d['thread']['replies_count'] for d in data3]
dict1['country']=[d['thread']['country'] for d in data3]
dict1['facebook']=[str(d)for d in dict1['facebook']]
dict1['text']= [d['text'] for d in data3]
#make dictionary

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
#import necessary package

def alpha_filter(w):
    pattern = re.compile('[^a-z]+')
    if (pattern.match(w)):
        return True
    else:
        return False
#remove non alpha symbol
stopwords = nltk.corpus.stopwords.words('english')


def ryzen5990x(w):
    g=nltk.word_tokenize(w)
    k = [a.lower( ) for a in g]
    l = [b for b in k if not alpha_filter(b)]
    m = [c for c in l if c not in stopwords]
    return m
#remove stopword and non alpha word.

wordlist=[]
for d in data3:
    wordlist+=ryzen5990x(d['text'])
#process and join all the words
sentlist=[]
for d in data3:
    sentlist += sent_tokenize(d['text'])
all_words2 = nltk.FreqDist(wordlist)
#process and join all the sents

word_items2 = all_words2.most_common(2000)
word_features2 = [word for (word, freq) in word_items2]
#generate word list for word_feature




traintest=[]
for d in data3[:1000]:
    for sent in sent_tokenize(d['text']):
        scores = SentimentIntensityAnalyzer().polarity_scores(sent)
        if scores['compound']>=0.05:
            traintest.append((word_tokenize(sent),'pos'))
        if scores['compound']> -0.05 and scores['compound']<0.05:
            traintest.append((word_tokenize(sent),'neg'))
        if scores['compound']< -0.05:
            traintest.append((word_tokenize(sent),'neu'))
#use vader to train a labelled dataset

random.shuffle(traintest)
#shuffle the traintest
def document_features(document, word_features):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features
#def feature method


featuresets = [(document_features(d,word_features2), c) for (d,c) in traintest]
train_set, test_set = featuresets[1000:], featuresets[:1000]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print (nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(30)
#train classifier using this feature



def readSubjectivity(path):
    flexicon = open(path, 'r')
    # initialize an empty dictionary
    sldict = { }
    for line in flexicon:
        fields = line.split()   # default is to split on whitespace
        # split each field on the '=' and keep the second part as the value
        strength = fields[0].split("=")[1]
        word = fields[2].split("=")[1]
        posTag = fields[3].split("=")[1]
        stemmed = fields[4].split("=")[1]
        polarity = fields[5].split("=")[1]
        if (stemmed == 'y'):
            isStemmed = True
        else:
            isStemmed = False
        # put a dictionary entry with the word as the keyword
        #     and a list of the other values
        sldict[word] = [strength, posTag, isStemmed, polarity]
    return sldict
#method reading SL
SLpath = 'subjclueslen1-HLTEMNLP05.tff'
SL = readSubjectivity(SLpath)
#import SL

def SL_features(document, word_features2, SL):
    document_words = set(document)
    features = {}
    posscore=0
    for word in word_features2:
        features['contains(%s)' % word] = (word in document_words)

    for word in document_words:
        if word in SL:
            strength, posTag, isStemmed, polarity = SL[word]
            if strength == 'weaksubj' and polarity == 'positive':
                posscore+=1
            if strength == 'strongsubj' and polarity == 'positive':
                posscore += 2
            if strength == 'weaksubj' and polarity == 'negative':
                posscore -= 1
            if strength == 'strongsubj' and polarity == 'negative':
                posscore -= 2
    features['positivecount']= posscore
    features['negativecount']= (-posscore)
    features['neutralcount']= 2-abs(posscore)
    return features
#def SL feature with neg, pos, neu score


SL_featuresets = [(SL_features(d, word_features2, SL), c) for (d,c) in traintest]
#def SL feature dataset

train_set2, test_set2 = SL_featuresets[1000:], SL_featuresets[:1000]
classifier2 = nltk.NaiveBayesClassifier.train(train_set2)
print(nltk.classify.accuracy(classifier2, test_set2))
classifier2.show_most_informative_features(30)
#train a SL feature classifier
negstcount=[]
posstcount=[]
neustcount=[]
#generate list of negsent possent neusent count
negst=[]
posst=[]
neust=[]
#extract all the neg, pos, neu sent into individual list

for d in data3:
    tempneg=0
    temppos=0
    tempneu=0
    for sent in sent_tokenize(d['text']):
        result=classifier2.classify(SL_features(word_tokenize(sent),word_features2,SL))
        if result =='neg':
            negst.append(sent)
            tempneg+=1
        if result =='pos':
            posst.append(sent)
            temppos+=1
        if result =='neu':
            neust.append(sent)
            tempneu+=1
    negstcount.append(tempneg)
    posstcount.append(temppos)
    neustcount.append(tempneu)
#generate neg,pos,neu count

import nltk.chunk
import itertools
#import package for chunking


grammar = grammar = r"""
  NP: {<DT|NN.*>+}          # Chunk sequences of DT, JJ, NN
  PP: {<IN><NP|VB.*>}               # Chunk prepositions followed by NP
  VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
  AJP: {<JJ.*>|<JJ.*><NP|PP>}         # Chunk adjetive phrase
  AVP: {<VB.*><RB.*>|<RB.*><PP>}     # Chunk adverb phrase
  CLAUSE: {<NP><VP>}           # Chunk NP, VP
  """
#def chunking grammar
text1=word_tokenize("I badly at playing")
text2=word_tokenize("I am bad")
cp = nltk.RegexpParser(grammar)
cp.parse(nltk.pos_tag(text1))
cp.parse(nltk.pos_tag(text2))
#test grammar
tree=cp.parse(nltk.pos_tag(text1))
for subtree in tree.subtrees():
    if subtree.label() == 'AVP':
        print(nltk.chunk.regexp.UnChunkRule(grammar, subtree))
#test classfiying method

posadj=[]
posadv=[]
posvp=[]
negadj=[]
negadv=[]
negvp=[]
#create list of neg , pos adj phrase, verb phrase, adv phrase
for sent in posst:
    tree = cp.parse(nltk.pos_tag(word_tokenize(sent)))
    for subtree in tree.subtrees():
        if subtree.label() == 'VP':
            posvp.append(subtree)
        if subtree.label() == 'AJP':
            posadj.append(subtree)
        if subtree.label() == 'AVP':
            posadv.append(subtree)
#generate these phrases
for sent in negst:
    tree = cp.parse(nltk.pos_tag(word_tokenize(sent)))
    for subtree in tree.subtrees():
        if subtree.label() == 'VP':
            negvp.append(subtree)
        if subtree.label() == 'AJP':
            negadj.append(subtree)
        if subtree.label() == 'AVP':
            negadv.append(subtree)
#extract string in these list for freqdist


def untoken(docu):
    leavelist = []
    for d in docu:
        temppp = ''
        for (e, c) in d.leaves():
            temppp += ' '
            temppp += e
        leavelist.append(temppp)
    return leavelist
#def method generate string for analyze


negvpst=untoken(negvp)
negadjst=untoken(negadj)
negadvst=untoken(negadv)
posvpst=untoken(posvp)
posadjst=untoken(posadj)
posadvst=untoken(posadv)
#extract string in these list for freqdist
fdnvp=nltk.FreqDist(negvpst)
fdnav=nltk.FreqDist(negadvst)
fdnaj=nltk.FreqDist(negadjst)
fdpvp=nltk.FreqDist(posvpst)
fdpav=nltk.FreqDist(posadvst)
fdpaj=nltk.FreqDist(posadjst)
#freq.dist these strings


fdpav.most_common(50)
fdpaj.most_common(50)
fdpvp.most_common(50)
fdnaj.most_common(50)
fdnvp.most_common(50)
fdnav.most_common(50)
#show the top 50 for all freq.dist
dict1['negcount']=negstcount
dict1['poscount']=posstcount
dict1['neucount']=neustcount
#add neg,pos,neu count into dict1


dict1.keys()
dict2={'author':dict1['author'], 'facebook':dict1['facebook'],'title':dict1['title']
,'published':dict1['published'], 'url':dict1['url'],'replies_count':dict1['replies_count'], 'country':dict1['country'], 'text':dict1['text']
,'negcount':dict1['negcount'], 'poscount':dict1['poscount'], 'neucount':dict1['neucount'] }
#create valid dict
import csv
f = open('dict2.csv','w', encoding="utf-8")
w = csv.DictWriter(f,dict2.keys())
w.writeheader()
w.writerow(dict2)
f.close()
#write dict into csv