import math
import os
from os import walk
import nltk
import Classes

# os.chdir('D:/Facultate/Master/Regasirea Informatiei/Lab 2 - Ranking/pa3-data/')
os.chdir('C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 2 - Ranking/pa3-data/')
# root = 'D:/Facultate/Master/Regasirea Informatiei/Lab 2 - Ranking/pa3-data/Training/'
root = 'C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 2 - Ranking/pa3-data/Training/'
i = 0
filenum = -1
dictionary = {}
for dirpath, dirnames, filenames in walk(root):
    try:
        with open(dirpath + "/" + filenames[0], 'r', encoding="utf8") as f:
            fileContent = f.read()
    except IOError as e:
        print(e)


def construct_title_tf(title_word):
    if title_word == 'header':
        return
    for word in desc1:
        if word == title_word:
            title_tf.append(1)
            return
    title_tf.append(0)


def construct_header_tf(header_word):
    if header_word == 'header' or header_word == 'body_hits':
        return
    for word in desc1:
        if word == header_word:
            headers_tf.append(1)
            return
    headers_tf.append(0)


def construct_body_tf(body_element):
    body_tf.append(len(body_element.split(' ')) - 1)


def construct_tf_array(tf_list):
    title_length = len(title.split(' '))
    L = title_length + headers_length + int(body_length)
    new_tf_list = [(1 + math.log(x)) / L for x in tf_list if x != 0]
    return new_tf_list


queries = {}
nr = 0
words = nltk.word_tokenize(fileContent)
i = 0
title_tf = []
headers_tf = []
body_tf = []
tft = []
tfh = []
tfb = []
headers_length = 0
while i < len(words):
    if words[i] == "query":
        desc = ""
        desc1 = []
        tfdb = []
        tfdt = []
        tfdh = []
        u = 0
        urls = {}
        i = i + 2
        while i < len(words) and words[i] != "url":
            desc = desc + words[i] + " "
            desc1.append(words[i])
            i = i + 1
        while i < len(words) and words[i] != "query":
            if words[i] == "url":
                url = ""
                title = ""
                headers = {}
                bodyHits = {}
                h = 0
                b = 0
                i = i + 2
                while i < len(words) and words[i] != "title":
                    url = url + words[i]
                    i = i + 1
                while i < len(words) and words[i] != "url" and words[i] != "query":
                    if words[i] == "title":
                        i = i + 2
                        while i < len(words) and words[i] != ":":
                            construct_title_tf(words[i])
                            title = title + words[i] + " "
                            i = i + 1
                        title = title.rsplit(' ', 2)[0]
                    else:
                        if words[i - 1] == "header":
                            i = i + 1
                            header = ""
                            while i < len(words) and words[i] != ":":
                                construct_header_tf(words[i])
                                header = header + words[i] + " "
                                i = i + 1
                            header = header.rsplit(' ', 2)[0]
                            headers[h] = Classes.Header(header)
                            h = h + 1
                            headers_length += len(header.split(' '))
                        else:
                            # headers_tf = []
                            if words[i - 1] == "body_hits":
                                i = i + 1
                                body = ""
                                while i < len(words) and words[i] != ":":
                                    body = body + words[i] + " "
                                    i = i + 1
                                body = body.rsplit(' ', 2)[0]
                                construct_body_tf(body)
                                bodyHits[b] = Classes.BodyHits(body)
                                b = b + 1
                            else:
                                if words[i - 1] == 'body_length':
                                    i = i + 1
                                    body_length = words[i]
                                i = i + 1
                                # construct_tf_array()
                                # body_tf = []
                urls[u] = Classes.Url(url, title, headers, bodyHits)
                u = u + 1
                tft = construct_tf_array(title_tf)
                tfh = construct_tf_array(headers_tf)
                tfb = construct_tf_array(body_tf)
                headers_length = 0
                title_tf = []
                headers_tf = []
                body_tf = []
        queries[nr] = Classes.Query(desc, urls)
        nr = nr + 1


# def print_queries():
# # print(queries)
#     for val in queries:
#         print(queries[val])


