import os
from os import walk
from collections import defaultdict
import re
import nltk
import time
import heapq


def find__hole__word__nltk(text):
    indexesList = {}
    words = nltk.word_tokenize(text)
    for i in range(0, len(words)):
        words[i] = ps.stem(words[i])
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


def print__merged__list(merged_list):
    for l in merged_list:
        filePath = list(dictionary.keys())[l - 1]
        directory = filePath[(filePath.rindex("/") - 1)::]
        print(directory)


def merge__posting__lists__from__disk():
    merged_final = list()
    for file in os.listdir(os.getcwd()):
        if file.endswith(".out"):
            new_list = list()
            with open(file, 'r+') as f:
                file_content = f.read()
                i = 0
                nr = 0
                offset = ''
                file_length = len(file_content)
                while i < file_length - 1:
                    if file_content[i] == '1':
                        nr = nr + 1
                        i = i + 1
                    if file_content[i] == '0':
                        for j in range(0, nr):
                            i = i + 1
                            offset = offset + file_content[i]
                        offset = '1' + offset
                        new_list.append(int(offset, 2))
                        offset = ''
                        nr = 0
                        i = i + 1
            for i in range(1, len(new_list)):
                new_list[i] = new_list[i] + new_list[i-1]
            merged_final = list(heapq.merge(merged_final, new_list))
    print__merged__list(merged_final)


def write__postings__list__to__disk(dict):
    if filenum == -1:
        return defaultdict(list)
    i = len(dict[query]) - 1
    while i > 0:
        dict[query][i] = dict[query][i] - dict[query][i - 1]
        i = i - 1
    s = str(filenum) + ".out"
    with open(s, "w+") as f:
        for word in dict:
            for item in dict[word]:
                var = bin(item)[3:]
                offset__length = len(var)
                str__offset = '0'
                for i in range(0, offset__length):
                    str__offset = '1' + str__offset
                gamma__var = str__offset + str(var)
                f.write(gamma__var)
            f.write("\n")
    return defaultdict(list)


# os.chdir('D:/Facultate/Master/Regasirea Informatiei/Lab1/')
os.chdir('C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 1 - index, query and compression/')
# root = 'D:/Facultate/Master/Regasirea Informatiei/Lab1/real_data/'
root = 'C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 1 - index, query and compression/real_data/'
i = 0
filenum = -1
query = "we are"
tokenizedQuery = nltk.word_tokenize(query)
ps = nltk.PorterStemmer()
for i in range(0, len(tokenizedQuery)):
    tokenizedQuery[i] = ps.stem(tokenizedQuery[i])
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
                if find__hole__word__nltk(fileContent) != 0:
                    dictionaryList[query].append(i) 
        except IOError as e:
            print(e)
    dictionaryList = write__postings__list__to__disk(dictionaryList)
    filenum = filenum + 1


merge__posting__lists__from__disk()
print(time.time() - start_time)
