#!/usr/bin/python

import sys
import re

# compare values
def testing(dictionaryLocation, postingsLocation):

    while True:
        print("Search: ")
        userInput = input()

        # end program
        if userInput == "ZZEND":
            break

        # filter value of non-alphanumeric values and lowercase it
        userInput = re.sub(r'\W+', '', userInput.rstrip()).lower()

        # open files
        fileOutDictionary = open(dictionaryLocation, "r")
        fileOutPostings = open(postingsLocation, "r")
        # search dictionary and postings
        for line in fileOutDictionary:
            vals = line.split(":")
            if vals[0] == userInput:
                print("\nDictionary: "+line+"\n")

        for line in fileOutPostings:
            vals = line.split(":")
            if vals[0] == userInput:
                print("Postings: "+line+"\n")

        #close files
        fileOutDictionary.close()
        fileOutPostings.close()

testing(sys.argv[1], sys.argv[2])