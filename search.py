import math
import re
import sys

# check if number to remove numbers and titles
def contains_digits(s):
    return any(char.isdigit() for char in s)

def tf(f):
    return 1 + math.log(f)

def w(tf, idf):
    return tf * idf

def sim(wi,wq):

    di = 0
    dNi = 0
    dNq = 0
    size = 0
    if len(wi) > len(wq):
        size = len(wq)
    else:
        size = len(wi)
    for i in range(size):
        di += wi[i] * wq[i]
        dNi += wi[i] * wi[i]
        dNq += wq[i] * wq[i]
    dNi = math.sqrt(dNi)
    dNq = math.sqrt(dNq)
    return ((di)/(dNi*dNq))

def searching(query, k):
    relevent = []
    if k is None:
        k = 10
    # get N
    N = 3203
    wordList = []

    # get idf values
    frequencyList = {}
    # pass list
    passList = []
    postings = open("invertedIndex/postings.txt", "r")
    for line in postings:
        words = line.split(": ")
        idf = math.log(N/int(words[1]))
        if idf >= 0.3:
            passList.append(words[0])
        val = words[1].replace("\n", "")
        frequencyList[words[0]] = [val,idf]

    # get wordList
    wordFile = open("invertedIndex/words.txt","r")
    for line in wordFile:
        line = line.replace('\n','')
        wordList.append(line)
    numberList = [0]*len(wordList)
    wordsInQuery = []
    # get information from query
    query = query.split(" ")
    # get frequencies
    for i in query:
        if contains_digits(i):
            continue
        # clean query
        val = re.sub(r'\W+', '', i.rstrip()).lower()
        if val=="":
            continue
        if val not in wordList:
            continue
        # get frequency
        index = wordList.index(val)
        # words position else not in database and take out low idf vals
        if index >= 0 and val in passList:
            numberList[index] += 1
            # number of relevent words
            if val not in wordsInQuery:
                wordsInQuery.append(val)
    
    wq = []
    wadjusted = []
    # get query weights
    for i in range(len(numberList)):
        if numberList[i] > 0:            
            # fetch frequency
            tfi = tf(numberList[i])
            idf = frequencyList.get(wordList[i])
            if(idf == None):
                continue
            wq.append(w(tfi, idf[1]))
        else:
            wq.append(0)

    # get documentList (frequency of each value in each document)
    documentList = {}
    documentFile = open("invertedIndex/documents.txt", "r")
    for line in documentFile:
        docs = line.split(": ")
        cleanList = docs[1].replace("[","")
        cleanList = cleanList.replace("]","")
        documentList[docs[0]] = cleanList.split(", ")

    top_vals = []

    #index elimination
    # get w for documents and check rank (add queue and pop off bottom vals)
    wi = []
    threshold = 0.9

    numberVal = len(wordsInQuery)
    # no useable words
    if numberVal == 0:
        raise Exception('Word(s) in query may not be relevant words.')
        return {}

    while(len(wi) < k):
        for i in documentList:
            # already in list
            if documentList[i] == []:
                continue
            checkVals = 0
            # get document list and check k-rating
            for j in range(len(documentList[i])):
                # contains 90% of query values
                if int(documentList[i][j]) > 0 and int(numberList[j]) > 0:
                    checkVals+=1

            if (checkVals/numberVal) >threshold:
                # add to list
                wi.append([i,documentList[i]])
                # remove documentList to remove duplication
                documentList[i] = []
                # top k hit
                if len(wi) == k:
                    break
        # hit all relevent data
        if threshold == 0.1:
            break
        threshold-=0.1

    # find weightss and sim and return list
    result = {}
    wd = []
    # go through each top k results
    for lists in wi:
        #sim
        wd = []
        for i in range(len(lists[1])):
            f = int(lists[1][i])
            if f > 0:            
                # fetch frequency
                tfi = tf(f)
                idf = frequencyList.get(wordList[i])
                wd.append(w(tfi, idf[1]))
            else:
                wd.append(0)
        similarity = sim(wd, wq)
        result[lists[0]]=similarity
    return result