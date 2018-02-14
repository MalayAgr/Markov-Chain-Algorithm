import re
import random
import time


class Table(object):
    """
    A class that represents the table of prefixes.
    Each object of the class will have a dictionary. The keys of the dictionary will be positive integers (just for the sake of having a key) and the values will be instances of the Prefix class.

    Attributes:
        table: A dictionary which will contain the prefixes and their corresponding suffixes.
    """

    def __init__(self):
        """
        Initializes the table attribute to an empty dictionary.
        """
        self.table = {}

    def addPrefix(self, prefix):
        """
        Adds a new item to the table dictionary, setting number as key and a Prefix object as the value. After adding the item, it returns that item.

        Arguments:
            firstPrefix: The first of the two prefixes.
            secondPrefix: The second of the two prefixes.
        """
        self.table[prefix] = []

    def addSuffix(self, prefix, suffix):
        self.table[prefix].append(suffix)

    def getTable(self):
        """
        Returns the table attribute.
        """
        return self.table


def lookup(searchPrefix, table):
    """
    A function which takes a list containing two prefixes and returns the list of suffixes corresponding to the it.

    Arguments:
         searchPrefix: The prefixes for which the suffixes need to be found.
         prefixes: The list of Prefix objects which is searched to get the suffix.
    """
    if searchPrefix in table.keys():
        return table[searchPrefix]
    return ['']


def isDuplicate(prefixes, table):
    """
    A function which returns True when a particular set of prefixes has already been accounted for in our text.

    Arguments:
         prefixes: A list whose duplicity is being checked.
         table: A Table object against which the duplicity is checked.
    """
    if prefixes in table.getTable().keys():
        return True
    return False


def createTable(words, text):
    """
    A function which obtains all the prefixes and their corresponding suffixes from a given text, and returns the result.

    Arguments:
         words: The words in the text.
         text: The actual text.
    """
    table = Table()
    count = 1
    length = len(words)
    for index, word in enumerate(words):
        if index == length - 1:
            break

        prefix = f'{word} {words[index + 1]}'
        if not isDuplicate(prefix, table):
            table.addPrefix(prefix)
            occurrences = re.finditer(prefix, text)
            for occurrence in occurrences:
                suffixBeginning = occurrence.end() + 1 #apparently, re.finditer() counts space
                suffix = text[suffixBeginning : text.find(' ', suffixBeginning)]
                table.addSuffix(prefix, suffix)

            count += 1

    return table.getTable()


def generate(table, wordCount):
    """
    A function which generates random text using the result of the previous function, word for word.

    Arguments:
         table: The prefixes and corresponding suffixes which will be used to produce the text.
         wordCount: The number of words that need to be generated.
    """
    items = list(table.items())
    currentPrefixes, currentSuffixes = items[0]
    print(currentPrefixes, end = ' ')

    count = 0
    while count < wordCount - 2:
        if currentSuffixes == [''] or currentSuffixes == []:
            randomPrefix = random.choice(items)
            currentPrefixes = randomPrefix[0]
            currentSuffixes = randomPrefix[1]
        else:
            word = random.choice(currentSuffixes)
            print(word, end = ' ')
            currentPrefixes = f'{currentPrefixes.split()[1]} {word}'
            currentSuffixes = lookup(currentPrefixes, table)
            count += 1


def main():
    text = input("Enter seed text: ")
    wordCount = int(input("Enter the number of words to be generated: "))
    words =  text.split()

    start = time.clock()
    table = createTable(words, text)
    print(f'Table creation for {len(words)} words: {time.clock() - start} seconds')

    start = time.clock()
    generate(table, wordCount)
    print(f'\nText generation for {wordCount} words: {time.clock() - start} seconds')


if __name__ == '__main__':
    main()