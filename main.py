import os
from os import walk

os.chdir('D:/Facultate/Master/Regasirea Informatiei/Lab1/real_data/')
i = 0
dictionary = {}
for dirpath, dirnames, filenames in walk('D:/Facultate/Master/Regasirea Informatiei/Lab1/real_data/'):
    for file in filenames:
        dictionary[dirpath + "/" + file] = i
        i = i + 1
        # try:
        #     with open(dirpath + "/" + file, 'r') as f:
        #         print(f.read())
        # except IOError as e:
        #     print(e)

# Test: print first 10 files
for item in dictionary:
    if dictionary[item] <= 10:
        print(item)

