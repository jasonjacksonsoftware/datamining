import csv

churchhandle1 = 'test'
churchhandlenext = '1stchurchatl'

def findchurchname(churchhandle1):
    firstinp.seek(0)
    for row in csv.reader(firstinp):
        if churchhandle1 == str(row[9]):
            return(str(row[0]))
        else:
            continue

def findaddress(churchhandle1):
    firstinp.seek(0)
    for row in csv.reader(firstinp):
        if churchhandle1 == str(row[9]):
            return(str(row[1]))
        else:
            continue

def findstate(churchhandle1):
    firstinp.seek(0)
    for row in csv.reader(firstinp):
        if churchhandle1 == str(row[9]):
            return(str(row[3]))
        else:
            continue

def findzip(churchhandle1):
    firstinp.seek(0)
    for row in csv.reader(firstinp):
        if churchhandle1 == str(row[9]):
            return(str(row[12]))
        else:
            continue

def findreltrad(churchhandle1):
    firstinp.seek(0)
    for row in csv.reader(firstinp):
        if churchhandle1 == str(row[9]):
            return(str(row[11]))
        else:
            continue

with open('complete.csv', 'r', encoding='utf8') as inp, open('completedfully.csv', 'a', newline='',encoding='utf8') as out, open('church.csv','r') as firstinp:
    writer = csv.writer(out)
    churchhandle = '1stchurchatl'
    for rows in csv.reader(inp):
        while churchhandle == churchhandlenext:
            for rowe in csv.reader(inp):
                churchhandle = str(rowe[2])
                date = str(rowe[0])
                time = str(rowe[1])
                state = findstate(churchhandle)
                zipcode = findzip(churchhandle)
                reltrad = findreltrad(churchhandle)
                retweet = str(rowe[8])
                tweetmessage = str(rowe[9])
                polcont = str(rowe[10])
                boolcont = str(rowe[11])
                churchname = findchurchname(churchhandle)
                address = findaddress(churchhandle)
                writer.writerow([date, time, churchhandle, churchname, address, state, zipcode, reltrad, retweet, tweetmessage, polcont, boolcont])
                if str(rowe[2]) != churchhandle:
                    churchhandlenext = str(rowe[2])

