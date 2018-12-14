import json
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


def reinit_dictionary(dictionary):
    for key in dictionary:
        dictionary[key] = 0


def construct_title_tf(title_word):
    if title_word == 'header':
        return
    for key in tft:
        if key == title_word:
            tft[key] = tft[key] + 1


def construct_header_tf(header_word):
    if header_word == 'header' or header_word == 'body_hits':
        return
    for key in tfh:
        if key == header_word:
            tfh[key] = tfh[key] + 1

def convert_dictionary_to_list(dictionary):
    new_list = []
    for key in dictionary:
        new_list.append(dictionary[key])
    return new_list


def construct_body_tf(body_element):
    body_tf.append(len(body_element.split(' ')) - 1)


def construct_tf_array(tf_list):
    title_length = len(title.split(' '))
    L = title_length + headers_length + int(body_length)
    return [(1 + math.log(x)) / L if x != 0 else 0 for x in tf_list]


def construct_query_vector_df(fileContent):
    for query_word in query_vector_df:
        query_vector_df[query_word] = query_vector_df[query_word] + fileContent.count(query_word)


def construct_query_vector():
    os.chdir('C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 1 - index, query and compression/')
    root = 'C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 1 - index, query and compression/real_data/0'
    for dirpath, dirnames, filenames in walk(root):
        for file in filenames:
            try:
                with open(dirpath + "/" + file, 'r') as f:
                    fileContent = f.read()
                    construct_query_vector_df(fileContent)
            except IOError as e:
                print(e)
    os.chdir('C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 2 - Ranking/pa3-data/')
    root = 'C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 2 - Ranking/pa3-data/Training/'


def construct_idf_query_vector():
    new_list = []
    title_length = len(title.split(' '))
    L = title_length + headers_length + int(body_length)
    for key in query_vector_df:
        if query_vector_df[key] != 0:
            new_list.append(math.log(L/query_vector_df[key]))
        else:
            new_list.append(0)
    print(new_list)
    print(query_vector_df)
    return new_list


queries = {}
nr = 0
words = nltk.word_tokenize(fileContent)
i = 0
title_tf_array = []
headers_tf_array = []
body_tf = []
tft = {}
tfh = {}
tfb = []
query_vector_df = {}
headers_length = 0
df_file = 'dfile.out'
while i < len(words):
    if words[i] == "query":
        desc = ""
        desc1 = []
        tft = {}
        tfh = {}
        query_vector_df = {}
        u = 0
        urls = {}
        i = i + 2
        while i < len(words) and words[i] != "url":
            desc = desc + words[i] + " "
            desc1.append(words[i])
            tft[words[i]] = 0
            tfh[words[i]] = 0
            query_vector_df[words[i]] = 0
            i = i + 1
        construct_query_vector()
        with open(df_file, "a") as f:
            f.write(json.dumps(query_vector_df))
        while i < len(words) and words[i] != "query":
            if words[i] == "url":
                url = ""
                title = ""
                headers = {}
                bodyHits = {}
                reinit_dictionary(tft)
                reinit_dictionary(tfh)
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
                urls[u] = Classes.Url(url, title, headers, bodyHits)
                u = u + 1

                title_tf_array = construct_tf_array(convert_dictionary_to_list(tft))
                headers_tf_array = construct_tf_array(convert_dictionary_to_list(tfh))
                tfb = construct_tf_array(body_tf)
                headers_length = 0
                body_tf = []
                # print(query_vector_df)
                # title_tf_array = []
                # headers_tf_array = []
                # print(tft)
                # print(tfh)
        print(title_tf_array)
        print(headers_tf_array)
        print(tfb)
        construct_idf_query_vector()
        queries[nr] = Classes.Query(desc, urls)
        nr = nr + 1


# def print_queries():
# # print(queries)
#     for val in queries:
#         print(queries[val])


