# Module Subjectivity reads the subjectivity lexicon file from Wiebe et al at http://www.cs.pitt.edu/mpqa/ (part of the Multiple Perspective QA project)
#
# This file has the format that each line is formatted as in this example for the word "abandoned"
#     type=weaksubj len=1 word1=abandoned pos1=adj stemmed1=n priorpolarity=negative
# In our data, the pos tag is ignored, so this program just takes the last one read
#     (typically the noun over the adjective)
#
# The data structure that is created is a dictionary where
#    each word is mapped to a list of 4 things:  
#        strength, which will be either 'strongsubj' or 'weaksubj'
#        posTag, either 'adj', 'verb', 'noun', 'adverb', 'anypos'
#        isStemmed, either true or false
#        polarity, either 'positive', 'negative', or 'neutral'

import nltk

# pass the absolute path of the lexicon file to this program
# example call:
# nancymacpath = 
#    "/Users/njmccrac/AAAdocs/research/subjectivitylexicon/hltemnlp05clues/subjclueslen1-HLTEMNLP05.tff"
# SL = readSubjectivity(nancymacpath)

# this function returns a dictionary where you can look up words and get back 
#     the four items of subjectivity information described above

def SL_features(document, word_features, SL):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    weakPos = 0
    strongPos = 0
    weakNeg = 0
    strongNeg = 0
    for word in document_words:
        if word in SL:
            strength, posTag, isStemmed, polarity = SL[word]
            if strength == 'weaksubj' and polarity == 'positive':
                weakPos += 1
            if strength == 'strongsubj' and polarity == 'positive':
                strongPos += 1
            if strength == 'weaksubj' and polarity == 'negative':
                weakNeg += 1
            if strength == 'strongsubj' and polarity == 'negative':
                strongNeg += 1
            features['positivecount'] = weakPos + (2 * strongPos)
            features['negativecount'] = weakNeg + (2 * strongNeg)
    return features

def NOT_features(document, word_features, negationwords):
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = False
        features['contains(NOT{})'.format(word)] = False
    # go through document words in order
    for i in range(0, len(document)):
        word = document[i]
        if ((i + 1) < len(document)) and ((word in negationwords) or (word.endswith("n't"))):
            i += 1
            features['contains(NOT{})'.format(document[i])] = (document[i] in word_features)
        else:
            features['contains({})'.format(word)] = (word in word_features)
    return features