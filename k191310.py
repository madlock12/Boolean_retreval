############################################################################################################
#                                    IR Assignment 1
#                           Inverted Index + Positional Index
#
#                                       19k1310
#                                   Mir Mubashir Ali
#                                       3/16/2022
############################################################################################################
import pprint
import string
from os import remove
from pydoc import doc
from turtle import distance, pos
from webbrowser import get

import nltk  # pip install nltk (library for snowball stemmer)
# pip install tensorflow (i have used this library for tokenization)
from keras.preprocessing.text import text_to_word_sequence
from nltk.stem.snowball import SnowballStemmer
from numpy import single

f = open("Stopword-List.txt", "r")  # loading stop words
stopword = f.read()
stopword = text_to_word_sequence(stopword)
f.close()  # stop word file

dictionary = dict()
posindex = dict()
result = []
snow_stemmer = SnowballStemmer(language='english')

for docno in range(1, 449):
    f = open("./Abstracts/Abstracts/"+str(docno) +
             ".txt", "r")  # reading all 448 files
    if(f):
        data = (f.read())
        retreaved = text_to_word_sequence(data)  # tokenize text file

        for i in range(len(stopword)):
            if(stopword[i] in retreaved):  # if specific stopword is in token
                retreaved.remove(stopword[i])  # removing stop words

        for i in retreaved:  # stem each token
            temp = snow_stemmer.stem(i)
            # append all stemmed token in a single string for making dictionary
            result.append(temp)
        temp = 0  # used for position of each word (in posindex)
        aux = dict()
        for c in result:  # making an inverted index using pythn dictionary
            temp += 1
            if c not in dictionary:
                # if words is not present then enter word+docID
                dictionary.setdefault(c, [docno])
            else:
                # restricting duplicates in inverted index docID section
                if docno not in dictionary[c]:
                    # if word is already present then only enter docID
                    dictionary[c] += [docno]

            if c not in posindex:  # if word do not exist in positional index
                # make a new dictionaty for word with DOCid:[positions]
                posindex.setdefault(c, {})
                posindex[c].setdefault(docno, [temp])

            # if word exist in positional index but not DOCid
            elif docno not in posindex[c]:
                # enter DOCid:[positions] with respective word
                posindex[c].setdefault(docno, [temp])

            else:  # if word repeats in same DOCid, append new locations
                posindex[c][docno].append(temp)

        result.clear()
        f.close()
    else:
        print("ERROR: File Number", docno, "Failed!!!")


def get_inverted_list(str):
    return dictionary[str]


def common(l1, l2):#intersection used in AND
    a = set(l1)
    b = set(l2)
    com = (a & b)
    return com


def union(l1, l2):#used in OR
    a = set(l1)
    b = set(l2)
    ans = list(a | b)
    return ans


##############################          Main          ##############################
Stemmed_Query = []
result = []
print()
print("NOTE: Enter AND OR NOT in upper_case ONLY! and place NOT in front of the Term")
print()
print("Enter your Query[NOT proximity]: ")# i have used keras with snow ball stemmer which removing / from tokens
Query = input()
Query = text_to_word_sequence(Query)  # tokenize entered query
for i in Query:
    temp = snow_stemmer.stem(i)
    Stemmed_Query.append(temp)

if(len(Stemmed_Query) == 1):  # single word query
    print("Single word query")
    temp = Stemmed_Query[0]
    result = get_inverted_list(temp)
    # print("Retreaved in Doc: ", result)
else:
    if(Stemmed_Query):  # check for empty query
        # Non Proximity query
        for c in Stemmed_Query:
            if("not" == c):  # resolve all not in query
                # extract index of not in query
                index = Stemmed_Query.index('not')
                # get list of term occuring after NOT
                temp = get_inverted_list(Stemmed_Query[index+1])
                for i in range(1, 449):
                    if i not in temp:
                        result.append(i)
                Stemmed_Query.pop(index)  # pop not

            # mir AND mubashir
            elif("and" == c and (Stemmed_Query[Stemmed_Query.index('and')+1] != "not")):
                index = Stemmed_Query.index('and')
                temp = get_inverted_list(Stemmed_Query[index+1])
                # intersect small list with a potentially bigger list
                temp2 = common(temp, result)
                result = list(temp2)
                Stemmed_Query.pop(index)  # pop and

            # mir AND NOT mubashir
            elif("and" == c and Stemmed_Query[Stemmed_Query.index('and')+1] == 'not'):
                index = Stemmed_Query.index('and')
                temp = get_inverted_list(Stemmed_Query[index+2])
                temp2=[]
                for i in range(1, 449):
                    if i not in temp:
                        temp2.append(i)
                temp2 = set(temp2)
                temp3 = set(result)
                temp4 = temp3.intersection(temp2)
                result = list(temp4)
                Stemmed_Query.pop(index)  # pop and
                Stemmed_Query.pop(index)  # pop not

            # mir or mubashir
            elif("or" == c and Stemmed_Query[Stemmed_Query.index('or')+1] != 'not'):
                index = Stemmed_Query.index('or')
                temp = get_inverted_list(Stemmed_Query[index+1])
                temp2 = union(temp, result)
                result = list(temp2)
                Stemmed_Query.pop(index)  # pop or

            # mir or not mubashir
            elif("or" == c and Stemmed_Query[Stemmed_Query.index('or')+1] == 'not'):
                index = Stemmed_Query.index('or')
                temp = get_inverted_list(Stemmed_Query[index+2])
                temp2=[]
                for i in range(1, 449):
                    if i not in temp:
                        temp2.append(i)
                temp3 = union(temp2, result)
                result = list(temp3)
                Stemmed_Query.pop(index)  # pop or
                Stemmed_Query.pop(index)  # pop not

            else:
                # if a term with out any operator appears
                result = get_inverted_list(c)
result.sort()
print("Retreaved in Doc: ", result)
Stemmed_Query = []
Query=[]
temp=0

print("############################################")
print("Enter your PROXIMITY Query: ")# i have used keras with snow ball stemmer which removing / from tokens
Query = input()
Query = text_to_word_sequence(Query)  # tokenize entered query
for i in Query:
    temp = snow_stemmer.stem(i)
    Stemmed_Query.append(temp)#STEM

prox=int(Stemmed_Query[-1])
Term1=Stemmed_Query[0]
Term2=Stemmed_Query[1]
Term1_Doc_list=dictionary[Term1]
Term2_Doc_list=dictionary[Term2]
list_to_search=list(common(Term1_Doc_list,Term2_Doc_list))#better complexity
output=[]


for i in list_to_search:
    for j in posindex[Term1][i]:
        for k in posindex[Term2][i]:
            if(k-j<=prox and k-j>=0):
                if(i not in output):
                    output.append(i)

print("Retreaved in Doc: ", output)