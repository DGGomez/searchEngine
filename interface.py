#!/usr/bin/python

from search import searching
import sys
import re
# compare values
def interface():
    print("Query: ")
    query = input()
    print("K: ")
    k = int(input())
    # get results
    results = searching(query,k)
    #sort results
    sorted_x = sorted(results.items(), key=lambda kv: kv[1], reverse = True)
    # print results
    for i in sorted_x:
        print(i)
        # get value info (title and author)
        fileOutInfo = open("invertedIndex/info.txt", "r")
        for line in fileOutInfo:
            vals = line.split(":")
            if vals[0] == i[0]:
                print(" "+line+"\n")
        fileOutInfo.close()

interface()