import nltk

def readFiles():

    import os
    aList = []
    # Explore the directory
    for filename in os.listdir(os.getcwd()):
        # Find doc files
        lines = ""
        if 'doc' in filename:
            file = open(filename, "r", encoding="ISO-8859-1")
            lines = file.read()
            file.close()

            # Replace undefined characters
            lines = lines.replace("’", "'")
            lines = lines.replace("‘", "'")
            lines = lines.replace("”", "\"")
            lines = lines.replace("“", "\"")

        aList.append(lines)

    return aList

def removeStopWords(words):
    from nltk.corpus import stopwords
    s = set(stopwords.words('english'))
    filterWords = []
    for word in words:
        if word.lower() not in s:
            filterWords.append(word)

    return filterWords


def printOutput(words, aList):
    from terminaltables import AsciiTable
    import re
    table_data = []
    table = AsciiTable(table_data)
    #Fill the headings of the table
    table.table_data.append(["Word(#)", "Documents", "Sentences containing the word"])

    for i in range (len(words)):
        row = []
        #Add the word to the first column
        row.append(words[i][0])

        #Add the documents' names to the second column
        tmp = ""
        for j in range(len(aList)):
            if words[i][0] in aList[j]:
                tmp +="doc" + str(j)+ ", "
        row.append(tmp[:len(tmp)-2])

        #Initiate third column as blank
        row.append("")
        table.table_data.append(row)

        #Add sentences to the third column
        for item in aList:
            if words[i][0] in re.findall(r'\w+', item):
                sentences = item.split('.')
                for sentence in sentences:
                    if words[i][0] in re.findall(r'\w+',sentence):
                        while len(sentence) > 0:
                            #Split the sentence to multiple lines
                            table.table_data[i+1][2] += "\n" + sentence[:50]
                            #Add '-' to the end of incomplete lines
                            if (len(sentence) > 50):
                                if (sentence[50] != ' ') & (sentence[49] != ' '):
                                    table.table_data[i+1][2] += "-"
                            sentence = sentence[50:]
                        table.table_data[i+1][2] += ".\n"

    table.inner_row_border = True
    #Print the table
    print (table.table)


def main():

    #Read the input files
    aList = readFiles()
    text = ""
    for line in aList:
        text += line

    #Parse the words in text
    import re
    words = re.findall(r'\w+', text)

    #Remove stop words
    filterWords = removeStopWords(words)

    #Count the 10 most common words
    from collections import Counter
    word_counts = Counter(filterWords).most_common(10)

    #Print output as table
    printOutput(word_counts, aList)

if __name__ == "__main__":
    main()
