import os
from os import walk
from collections import defaultdict


def print__dictionary__list(dictionary__list):
    for key in dictionary__list:
        print(dictionary__list[key])


def merge__dictionary(dict):
    # for k in sorted(dict, key=lambda k: len(dict[k])):
    #     print(k)
    mergedlist = []
    sorted_dictionary = sorted(dict, key=lambda k: len(dict[k]))
    i, j = 0, 0
    while i < len(dict[word1]) and j < len(dict[word2]):
        if dict[word1][i] == dict[word2][j]:
            mergedlist.append(dict[word1][i])
            i = i + 1
            j = j + 1
        elif dict[word1][i] < dict[word2][j]:
            i = i + 1
        else:
            j = j + 1
    return mergedlist


# os.chdir('D:/Facultate/Master/Regasirea Informatiei/Lab1/real_data/')
os.chdir('C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 1 - index, query and compression/real_data/0/')
root = 'C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 1 - index, query and compression/real_data/'
i = 0
j = 0
word1 = 'we'
word2 = 'are'
dictionary = {}
dictionaryList = defaultdict(list)
# for dirpath, dirnames, filenames in walk('D:/Facultate/Master/Regasirea Informatiei/Lab1/real_data/'):
for dirpath, dirnames, filenames in walk(root):
    for file in filenames:
        dictionary[dirpath + "/" + file] = i
        i = i + 1
        if j <= 1:
            try:
                with open(dirpath + "/" + file, 'r') as f:
                    fileContent = f.read()
                    if word1 in fileContent:
                        dictionaryList[word1].append(i)
                    if word2 in fileContent:
                        dictionaryList[word2].append(i)
            except IOError as e:
                print(e)
    j = j + 1

# Test: print first 10 files
for item in dictionary:
    if dictionary[item] <= 10:
        print(item)

print__dictionary__list(dictionaryList)
list1 = dictionaryList.get(word1)
list2 = dictionaryList[word2]
print(len(list1))
print(len(list2))
print(merge__dictionary(dictionaryList))
