import re
import random
import time

class Prefix(object):

    def __init__(self, firstPrefix = '', secondPrefix = ''):
        self.prefixes = [firstPrefix, secondPrefix]
        self.suffixes = []

    def addSuffix(self, suffix):
        self.suffixes.append(suffix)


class Table(object):

    def __init__(self):
        self.table = {}

    def addPrefix(self, number, firstPrefix, secondPrefix):
        self.table[number] = Prefix(firstPrefix, secondPrefix)
        return self.table[number]

    def getTable(self):
        return self.table


def lookup(searchPrefix, prefixes):

    for prefix in prefixes:
        if searchPrefix == prefix.prefixes:
            return prefix.suffixes

def isDuplicate(prefixes, table):

    for prefix in table.getTable().values():
        if prefix.prefixes == prefixes:
            return True
    return False

def createTable(words, text):

    table = Table()
    count = 1
    length = len(words)
    for index, word in enumerate(words):
        if index == length - 1:
            break

        if not isDuplicate([word, words[index + 1]], table):
            entry = table.addPrefix(count, word, words[index + 1])
            occurrences = re.finditer(f'{entry.prefixes[0]} {entry.prefixes[1]}', text)
            for occurrence in occurrences:
                suffixBeginning = occurrence.end() + 1
                suffix = text[suffixBeginning : text.find(' ', suffixBeginning)]
                entry.addSuffix(suffix)
            count += 1

    return table

def generate(table, wordCount):

    prefixes = list(table.getTable().values())
    currentPrefixes, currentSuffixes = prefixes[0].prefixes, prefixes[0].suffixes

    count = 0
    while count < wordCount:
        word = random.choice(currentSuffixes)
        print(word, end = ' ')
        currentPrefixes = [currentPrefixes[1], word]
        currentSuffixes = lookup(currentPrefixes, prefixes)
        count += 1

def main():
    text = input("Enter seed text: ")
    wordCount = int(input("Enter the number of words to be generated: "))
    words =  text.split()
    start = time.clock()
    table = createTable(words, text)
    generate(table, wordCount)
    print(time.clock() - start)


if __name__ == '__main__':
    main()