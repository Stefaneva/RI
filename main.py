import os
from os import walk
import nltk
import Classes

os.chdir('D:/Facultate/Master/Regasirea Informatiei/Lab 2 - Ranking/pa3-data/')
# os.chdir('C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 1 - index, query and compression/')
root = 'D:/Facultate/Master/Regasirea Informatiei/Lab 2 - Ranking/pa3-data/Training/'
# root = 'C:/Users/Eva/Desktop/Information retrieval/Lab/Lab 1 - index, query and compression/real_data/'
i = 0
filenum = -1
dictionary = {}
for dirpath, dirnames, filenames in walk(root):
    try:
        with open(dirpath + "/" + filenames[0], 'r', encoding="utf8") as f:
            fileContent = f.read()
    except IOError as e:
        print(e)

queries = {}
nr = 0
words = nltk.word_tokenize(fileContent)
i = 0
while i < len(words):
    if words[i] == "query":
        desc = ""
        u = 0
        urls = {}
        i = i + 2
        while i < len(words) and words[i] != "url":
            desc = desc + words[i] + " "
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
                            title = title + words[i] + " "
                            i = i + 1
                        title = title.rsplit(' ', 2)[0]
                    else:
                        if words[i-1] == "header":
                            i = i + 1
                            header = ""
                            while i < len(words) and words[i] != ":":
                                header = header + words[i] + " "
                                i = i + 1
                            header = header.rsplit(' ', 2)[0]
                            headers[h] = Classes.Header(header)
                            h = h + 1
                        else:
                            if words[i - 1] == "body_hits":
                                i = i + 1
                                body = ""
                                while i < len(words) and words[i] != ":":
                                    body = body + words[i] + " "
                                    i = i + 1
                                body = body.rsplit(' ', 2)[0]
                                bodyHits[b] = Classes.BodyHits(body)
                                b = b + 1
                            else:
                                i = i + 1
                urls[u] = Classes.Url(url, title, headers, bodyHits)
                u = u + 1
        queries[nr] = Classes.Query(desc, urls)
        nr = nr + 1

print(queries)


