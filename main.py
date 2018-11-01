import os
from os import walk
from collections import defaultdict
import re
import nltk
import time
import heapq


def find__hole__word__nltk(word, text):
    indexesList = {}
    tokenizedQuery = nltk.word_tokenize(word)
    words = nltk.word_tokenize(text)
    for w in tokenizedQuery:
        indexesList[tokenizedQuery.index(w)] = [index for index, value in enumerate(words) if value == w]
    for i in indexesList:
        if len(indexesList[i]) == 0:
            return 0
    nr = 0
    for i in indexesList[0]:
        for j in indexesList:
            k = 1
            if not j == 0:
                if not (i + j) in indexesList[j]:
                    k = 0
        if k == 1:
            nr = nr + 1
    return nr


# def find__hole__word(w):
#     return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def print__merged__list(merged_list):
    # print(len(merged_list))
    for l in merged_list:
        filePath = list(dictionary.keys())[l-1]
        directory = filePath[(filePath.rindex("/") - 1)::]
        print(directory)


def merge__posting__lists__from__disk():
    merged_final = list()
    for file in os.listdir(os.getcwd()):
        if file.endswith(".out"):
            with open(file, 'r+') as f:
                new_list = [int(x) for x in f.readline().split()]
                merged_final = list(heapq.merge(merged_final, new_list))
    print__merged__list(merged_final)


def write__postings__list__to__disk(dict):
    if filenum == -1:
        return defaultdict(list)
    sorted_dictionary = sorted(dict, key=lambda k: len(dict[k]))
    s = str(filenum) + ".out"
    with open(s, "w+") as f:
        for word in sorted_dictionary:
            for item in dict[word]:
                f.write("%s " % item)
            f.write("\n")
    return defaultdict(list)


os.chdir('D:/Facultate/Master/Regasirea Informatiei/Lab1/')
# os.chdir('C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 1 - index, query and compression/')
root = 'D:/Facultate/Master/Regasirea Informatiei/Lab1/real_data/'
# root = 'C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 1 - index, query and compression/real_data/'
i = 0
filenum = -1
query = "we are"
dictionary = {}
dictionaryList = defaultdict(list)
start_time = time.time()
for dirpath, dirnames, filenames in walk(root):
    for file in filenames:
        dictionary[dirpath + "/" + file] = i
        i = i + 1
        try:
            with open(dirpath + "/" + file, 'r') as f:
                fileContent = f.read()
                # if find__hole__word(word1)(fileContent) is not None:
                #     dictionaryList[word1].append(i)
                # if find__hole__word(word2)(fileContent) is not None:
                #     dictionaryList[word2].append(i)
                if find__hole__word__nltk(query, fileContent) != 0:
                    dictionaryList[query].append(i)
                # if find__hole__word__nltk(word2, fileContent) != 0:
                #     dictionaryList[word2].append(i)
        except IOError as e:
            print(e)
    dictionaryList = write__postings__list__to__disk(dictionaryList)
    filenum = filenum + 1

merge__posting__lists__from__disk()
# print(time.time() - start_time)
