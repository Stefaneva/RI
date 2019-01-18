from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
import math
import numpy as np
import pandas as pd
import operator
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')


D = fetch_20newsgroups(subset='train', shuffle=True)
C = D.target_names  # classes names


def joinStrings(stringList):
    return ''.join(string for string in stringList)


def ExtractVocabulary(D):
    count_vect = CountVectorizer()
    count_vect.fit_transform(D.data)
    return count_vect.get_feature_names()


def CountDocs(D):
    return len(D.data)


def CountDocsInClass(c):
    return len(fetch_20newsgroups(subset='train', categories=[c]).data)


def ConcatenateTextOfAllDocsInClass(c):
    return joinStrings(fetch_20newsgroups(subset='train', categories=[c]).data)


def CountTokensOfTerm(textC):
    corpus = [textC]
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    return pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())


def TrainMultinomialNB(C, D):
    V = ExtractVocabulary(D)
    N = CountDocs(D)
    prior = {}
    cond_prob = {}
    for c in C:
        nc = CountDocsInClass(c)
        prior.update({c: nc / N})
        textC = ConcatenateTextOfAllDocsInClass(c)
        T = CountTokensOfTerm(textC)
        T_sum = sum(T[t][0] + 1 if t in T.columns else 0 for t in V)
        for t in V:
            if t not in cond_prob:
                cond_prob.update({t: {c: (T[t][0] if t in T.columns else 1) / T_sum}})
            else:
                cond_prob[t].update({c: (T[t][0] if t in T.columns else 1) / T_sum})
    return V, prior, cond_prob


def ApplyMultinomialNB(C, prior, cond_prob, d):
    W = word_tokenize(d.lower())
    score = {}
    for c in C:
        score.update({c: (math.log(prior[c]) if prior[c] > 0 else 0)})
        score[c] = sum(math.log(cond_prob[t][c]) for t in W if t in cond_prob)
    key_max = max(score.items(), key=operator.itemgetter(1))[0]
    return C.index(key_max)


V, prior, cond_prob = TrainMultinomialNB(C, D)

twenty_test = fetch_20newsgroups(subset='test', shuffle=True)
test_data = twenty_test.data
predicted = [ApplyMultinomialNB(C, prior, cond_prob, test_data[i]) for i in range(0, len(test_data))]
res = np.mean(predicted == twenty_test.target)
print("Predicted accuracy: {0}%".format(res*100.0))
