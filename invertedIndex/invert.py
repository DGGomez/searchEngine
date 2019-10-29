import math
import sys
import re
from stemming import PorterStemmer

p = PorterStemmer()

# control values
stem = False
stopwords = False

stopList = []
wordList = []
numberList = []

docInfo = {}
documentList={}
contextList = {}
frequencyList = {}
locationList = {}
totalList = {}

# check if number to remove numbers and titles
def contains_digits(s):
    return any(char.isdigit() for char in s)

# read doc
def readDoc(doc, context):
    lists = doc.split(" ")
    for w in range(len(lists)):
        i = lists[w]
        if i == '':
            continue
        if i not in context:
            context.pop(0)
            context.append(i)
        val = re.sub(r'\W+', '', i.rstrip()).lower()
        if stem:
            val = p.stem(val,0,len(val)-1)
        # check if value is a number
        if contains_digits(val):
            continue
        # check if value is a stop word
        if stopwords:
            if val in stopList:
                continue
        # add to frequency
        if val in wordList:
            if val not in locationList:
                locationList[val] = [w]
            else:
                locationList[val].append(w)
            if val not in contextList:
                contextList[val] = context
            index = wordList.index(val)
            numberList[index] = numberList[index] + 1
            continue
        # if word doesn't exist add it and strip all non-alphanumeric chars
        else:
            if len(val) >= 1:
                contextList[val] = context
                locationList[val] = [w]
                wordList.append(val)
                numberList.append(1)
            continue
# get final values
def finalVals(wordList, numberList, frequencyList, totalList, idVal, title, locationList, contextList):
    title = title.replace('\n', ' ')
    index = 0
    for num in numberList:
        if num > 0:
            key = wordList[index]
            if key in frequencyList:
                # add frequency
                orgVal = frequencyList.get(key)
                frequencyList[key] = orgVal + 1
            else:
                frequencyList[key] = 1
                # add value to totalList
            if key in totalList:
                totalVal = totalList.get(key)
                totalVal.append([idVal, title, num, locationList.get(key), contextList.get(key)])
                totalList[key] = totalVal
            else:
                totalList[key]=[[idVal, title, num, locationList.get(key), contextList.get(key)]]
        index = index + 1 

# check which function to run
if len(sys.argv) > 1:
    if sys.argv[1] == "stemming":
        stem = True
    elif sys.argv[1] == "stopwords":
        stopwords = True

# stop words
if stopwords:
    file = open("stopwords.txt", "r") 
    for line in file:
        stopList.append(line.rstrip())

# common words minus stop words
file = open("common_words", "r") 
for line in file:
    if stopwords:
        if line not in stopList:
            val = line.rstrip()
            wordList.append(val)
            frequencyList[val]= 0
    else:
        val = line.rstrip()
        wordList.append(val)
        frequencyList[val]= 0
numberList = [0] * len(wordList)

# read input
idVal = ""
start = 0
file = open("cacm.all", "r") 
title = ""
doc = ""
author = ""
for line in file:
    lists = line.split(" ")
    # start of new data value
    if line[0] == ".":
        if start == 1 or start == 2:
            doc = doc.replace('\n',' ')
            context = doc.split(" ")
            readDoc(doc,context[:10])
        doc = ""
        start = 0
    if start == 3:
        author = line
    if start == 2:
        title += line
    if start >0:
        # check if stop hit
        if line == ".N":
            start = 0
            continue
        else:
            # read one document
            doc += line

    # after these lines start reading
    if ".A" in line:
        start = 3
    if ".T" in line:
        start = 2
    if ".W" in line:
        start = 1

    # clear values for next document
    if lists[0] == ".I":
        # check frequency go through numberList and all none zeros get incremented 
        # make a function for this
        if idVal != "":
            # add doc info
            docInfo[idVal] = [title, author]
            # update documents
            documentList[idVal] = numberList            
            # update final values
            finalVals(wordList, numberList, frequencyList, totalList, idVal, title, locationList, contextList)
            #reset numberList
            numberList = [0] * len(wordList)
            # restart title
            title = ""
            author = ""
            # reset lcoationList
            locationList = {}
            contextList = {}
        idVal = lists[1].rstrip()

# update final values with last document
finalVals(wordList, numberList, frequencyList, totalList, idVal, title, locationList, contextList)

# sort totalList
sortedTotal = sorted(totalList)

# output files
fileOutDictionary = open("dictionary.txt", "w+")
fileOutPostings = open("postings.txt", "w+")

for key in sortedTotal:
    fileOutDictionary.write(key+": "+str(totalList[key])+"\n")
    fileOutPostings.write(key+": "+str(frequencyList[key])+"\n")
    
fileOutDictionary.close()
fileOutPostings.close()

fileOutWords = open("words.txt", "w+")
for val in wordList:
    fileOutWords.write(val+"\n")
fileOutWords.close()

fileOutInfo = open("info.txt", "w+")
for key in docInfo:
    fileOutInfo.write(key+": "+str(docInfo[key])+"\n")
fileOutInfo.close()

fileOutDocuments = open("documents.txt", "w+")
for key in documentList:
    fileOutDocuments.write(key+": "+str(documentList[key])+"\n")
fileOutDocuments.close()
