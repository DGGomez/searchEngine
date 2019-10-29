from search import searching

def MeanAveragePrecision(qrelsI, ids):
    precision = 0
    count = 0
    hit = 0
    for i in ids:
        count += 1
        if i in qrelsI:
            hit += 1
            precision += (hit/count)
    return precision/len(qrelsI)
    
def rPrec(qrelsI, ids):
    hit = 0
    count = len(qrelsI)
    for i in ids:
        if i in qrelsI:
            hit+=1
    return hit/count

queries = {}
qrels = {}
id = ""
start = 0
q = ""
# read query
file = open("query.text", "r")
for line in file:
    val = line.split(" ")
    check = val[0].replace("\n", "")
    if check == ".I":
        if id != "":
            queries[id] = q
            q=""
        id = val[1].replace("\n", "")
    elif check == ".N" or check == ".A":
        #add to queries
        start = 0 
    elif start == 1:
        q += line
    elif check == ".W":
        # read until next . value
        start = 1

# get relevent docs for each query
file = open("qrels.text", "r")
for line in file:
    vals = line.split(" ")
    id = str(int(vals[0]))
    if id in qrels:
        qrels[id].append(vals[1])
    else:
        qrels[id] = [vals[1]]
totalMap = 0
rPrecision = 0
for query in queries:
    if query in qrels:
        val = queries[query]
        valq = qrels[query]
        resultList = searching(val, 10)
        # map
        m = MeanAveragePrecision(valq, resultList)
        totalMap += m
        #r precision
        r = rPrec(valq, resultList)
        rPrecision += r
        print("ID: "+query)
        print(m)
        print(str(r)+"\n")

totalMap= totalMap/64
# output average map
print(totalMap)
rPrecision = rPrecision/64
# output average r-precision
print(rPrecision)