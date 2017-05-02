import csv

fuzzywords = []
phrases = []
singlewords = []

with open('wordlist.txt', "r") as word_list:
    words = word_list.read().split(', ') #split the list of words by commas
    for word in words:
        if word.endswith('*'):  #find words that are meant to be wildcard words
            newword = word.replace("*", "") #remove the asterisk
            fuzzywords.append(newword)  #add these to the fuzzy words list
        elif word.__contains__(' '): #if the word contains a space, it must be a multiword phrase
            phrases.append(word)  #append multi-word phrases to the phrases list
        else:
            singlewords.append(word) #all others must be single words, add them to the appropriate list

with open('first_edit.csv', 'r', encoding='utf8') as inp, \
        open('second_edit.csv', 'a', newline='', encoding='utf8') as out:  #open the original file containing all the mined tweets as input and a new file for output
    writer = csv.writer(out)
    for row in csv.reader(inp):
        foundmatch = False
        foundword = 'Matched Word(s): '
        row0 = str(row[0])
        row1 = str(row[1])
        row2 = str(row[2])
        row3 = str(row[3])
        row4 = str(row[4])
        row5 = str(row[5])
        row6 = str(row[6])
        row7 = str(row[7])
        row8 = str(row[8])
        row9 = str(row[9])
        row10 = str(row[10])
        row11 = str(row[11])
        row12 = str(row[12])

        for item in singlewords:
           if item in str(row[12]): #first check if the tweets column contains any words from the single words list
               foundword = foundword + str(item) + ', ' #If a matched word is found, add it to our string that increases with each match per individual tweet.
               foundmatch = True #This tweet will be tagged as a match now

        for item in phrases:
            if item in str(row[12]): #now search for multi-word phrases
                foundword = foundword + str(item) + ', '
                foundmatch = True #must set to True for each match in case no match was found for the previous kind of list

        for item in fuzzywords:
            potentialword = str(row[12])
            for word in potentialword.split(): #must split the tweet apart by each word separated by a space
                if word.startswith(item): #now we can check each word to see if it starts with a wildward word from our list
                    foundword = foundword + str(item) + ', '
                    foundmatch = True


        if foundmatch == True:
            # Tag it as a matched tweet with the appropriate headers and include all matched words and the original content
            writer.writerow([str(row[8]), str(row[7]), str(row[1]), str(row[2]), 'Address', 'State', 'Zip', 'Reltrad', 'RT', str(row[12]), foundword, '1'])
        else:
            writer.writerow([str(row[8]), str(row[7]), str(row[1]), str(row[2]), 'Address', 'State', 'Zip', 'Reltrad', 'RT', str(row[12]), 'No political content found.', '0']) #Tag it as a non-political tweet.

