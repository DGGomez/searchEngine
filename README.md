# cps842_f19_assign2
TODO

- parallel processing
- improve k values returned
- update function to run invert.py
- add to stop words
- testing function to get search engine evaluation
- apply search to new data
- change search function to read list and then sort list for weights

Invert:

Creates posting list (sorted by id), dictionary list, document list( frequency list of each doc for fast SIM calculation),
word list (list of all words in the documents to remove irrelevenat words from query), and info list (title and author info for each doc for interface.py)

Search:

Go through postings list and get words with IDF values higher then 0.3 (threshold) for index elimmination. Read in word list (to check relevance of query words). Go through
query string and clean values removing non-alphabet chars, the frequency of the words
in this query are put into numberList and compared with word List to tell what word it is. Get query weight by getting IDF front array and calculating tf from numberList frequencies. Read in documents and put into a dictionary list (frequency list for each doc). With this list go through each doc getting weight if they contain at least 90% of the words in the query. When weight list has reached K values, then continue else remove 10% from filtering value. Use the final list and get SIM value and add to dictionary and return.

Eval:

Read queries from query.txt into dictionary with ID as key. The relevent doctument for each query is put into a dictionary 
id is key with an array as the value (array of relevent ids for documents in CACM.all). Go through query dictionary and send 
to search program. The returned dictionary is checked with MAP and R precision functions. This value is then printed and added
to totalMap and rPrecision values to get the average values.( in that order )

Interface:

Input your query and K value to user input. This is put into search program which will return a map of IDs and SIM values.
This is then sorted in descending order and printed. This ID value is used to get ID information (Title, Author)

How to run:
(please note that these can take between 5-10 minutes)
    # test queries:
    python eval.py  
    
    # query interface:
    python interface.py

    # refresh index documents:
    python invert.py
    python invert.py stopwords (remove stopwords)
    python invert.py stemmming (porter stemming) (not recommended as the stems arent included in eval or search)