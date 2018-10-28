import os
from os import walk
from collections import defaultdict
import re
import nltk
import time
import heapq


def find__hole__word__nltk(word, text):
    words = nltk.word_tokenize(text)
    return words.count(word)


def find__hole__word(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def print__dictionary__list(dictionary__list):
    for key in dictionary__list:
        print(dictionary__list[key])


def merge__dictionary(dict):
    # for k in sorted(dict, key=lambda k: len(dict[k])):
    #     print(k)

    # mergedlist = []
    # sorted_dictionary = sorted(dict, key=lambda k: len(dict[k]))
    i, j = 0, 0
    k = 0
    while i < len(dict[word1]) and j < len(dict[word2]):
        if dict[word1][i] == dict[word2][j]:
            filePath = list(dictionary.keys())[list(dictionary.values()).index(dict[word1][i])]
            directory = filePath[(filePath.rindex("/") - 1)::]
            print(directory)
            k = k + 1
            # mergedlist.append(dict[word1][i])
            i = i + 1
            j = j + 1
        elif dict[word1][i] < dict[word2][j]:
            i = i + 1
        else:
            j = j + 1
    # return mergedlist
    # print(k)


def sort__posting__list(dict):
    sorted_dictionary = sorted(dict, key=lambda k: len(dict[k]))
    print(sorted_dictionary)
    with open("test.out", "a+") as f:
        for word in sorted_dictionary:
            for item in dict[word]:
                f.write("%s " % item)
            f.write("\n")


def merge__posting__lists__from__disk():
    merged_final = list()
    for file in os.listdir(os.getcwd()):
        if file.endswith(".out"):
            with open(file, 'r+') as f:
                first_line = [int(x) for x in f.readline().split()]
                second_line = [int(x) for x in f.readline().split()]
                merged_list = list(heapq.merge(first_line, second_line, key=lambda a: a == a))
                if not merged_final:
                    merged_final = merged_list
                else:
                    merged_final = list(heapq.merge(merged_final, merged_list, key=lambda a: a == a))
    print(merged_final)


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


# os.chdir('D:/Facultate/Master/Regasirea Informatiei/Lab1/real_data/')
os.chdir('C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 1 - index, query and compression/')
# root = 'D:/Facultate/Master/Regasirea Informatiei/Lab1/real_data/'
root = 'C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 1 - index, query and compression/real_data/'
i = 0
filenum = -1
word1 = 'are'
word2 = 'we'
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
                if find__hole__word(word1)(fileContent) is not None:
                    dictionaryList[word1].append(i)
                if find__hole__word(word2)(fileContent) is not None:
                    dictionaryList[word2].append(i)
                    # if find__hole__word__nltk(word1, fileContent) != 0:
                    #     dictionaryList[word1].append(i)
                    #  if find__hole__word__nltk(word2, fileContent) != 0:
                    #     dictionaryList[word2].append(i)
        except IOError as e:
            print(e)
    dictionaryList = write__postings__list__to__disk(dictionaryList)
    filenum = filenum + 1

# print__dictionary__list(dictionaryList)
# list1 = dictionaryList.get(word1)
# list2 = dictionaryList[word2]
# print(len(list1))
# print(len(list2))
# merge__dictionary(dictionaryList)

# sort__posting__list(dictionaryList)

merge__posting__lists__from__disk()
print(time.time() - start_time)
