import re
import random
from functools import reduce
import time

class Prefix(object):
    """
    As per the algorithm, two prefixes are followed by a list of suffixes, which is being replicated over here.

    Attributes:
        prefixes: A list which contains the two prefixes for the object.
        suffixes: A list which contains the suffixes associated with the prefixes.
    """

    def __init__(self, firstPrefix = '', secondPrefix = ''):
        """
        Initializes a new Prefix object.

        It takes two strings as arguments and creates a prefix list out of them.

        Arguments:
             firstPrefix: The first prefix for this object.
             secondPrefix: The second prefix for this object.
        """
        self.prefixes = [firstPrefix, secondPrefix]
        self.suffixes = []

    def addSuffix(self, suffix):
        """
        A method that takes a suffix as its parameter and adds that suffix to the suffixes list of the Prefix object.

        Arguments:
            suffix: The suffix to be added to the list.
        """
        self.suffixes.append(suffix)


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

    def addPrefix(self, number, firstPrefix, secondPrefix):
        """
        Adds a new item to the table dictionary, setting number as key and a Prefix object as the value. After adding the item, it returns that item.

        Arguments:
            firstPrefix: The first of the two prefixes.
            secondPrefix: The second of the two prefixes.
        """
        self.table[number] = Prefix(firstPrefix, secondPrefix)
        return self.table[number]

    def getTable(self):
        """
        Returns the table attribute.
        """
        return self.table


def lookup(searchPrefix, prefixes):
    """
    A function which takes a list containing two prefixes and returns the list of suffixes corresponding to the it.

    Arguments:
         searchPrefix: The prefixes for which the suffixes need to be found.
         prefixes: The list of Prefix objects which is searched to get the suffix.
    """
    index = ((prefix.prefixes, prefix.suffixes) for prefix in prefixes)
    for prefix, suffix in index:
        if searchPrefix == prefix:
            return suffix
    return ['']


def isDuplicate(prefixes, table):
    """
    A function which returns True when a particular set of prefixes has already been accounted for in our text.

    Arguments:
         prefixes: A list whose duplicity is being checked.
         table: A Table object against which the duplicity is checked.
    """
    current = (prefix.prefixes for prefix in table.getTable().values())
    if prefixes in current:
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

        prefix1 = word
        prefix2 = words[index + 1]
        if not isDuplicate([prefix1, prefix2], table):
            entry = table.addPrefix(count, prefix1, prefix2)
            occurrences = re.finditer(f'{prefix1} {prefix2}', text)
            for occurrence in occurrences:
                suffixBeginning = occurrence.end() + 1 #apparently, re.finditer() counts space
                suffix = text[suffixBeginning : text.find(' ', suffixBeginning)]
                entry.addSuffix(suffix)
            count += 1

    return table


def generate(table, wordCount):
    """
    A function which generates random text using the result of the previous function, word for word.

    Arguments:
         table: The prefixes and corresponding suffixes which will be used to produce the text.
         wordCount: The number of words that need to be generated.
    """
    prefixes = list(table.getTable().values())
    currentPrefixes, currentSuffixes = prefixes[0].prefixes, prefixes[0].suffixes
    print(reduce(lambda x, y: x + " " + y, currentPrefixes), end = ' ')

    count = 0
    while count < wordCount - 2:
        if currentSuffixes == ['']:
            randomPrefix = random.choice(prefixes)
            currentPrefixes = randomPrefix.prefixes
            currentSuffixes = randomPrefix.suffixes
        else:
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
    print(f'Table creation for {len(words)} words: {time.clock() - start} seconds')

    start = time.clock()
    generate(table, wordCount)
    print(f'\nText generation for {wordCount} words: {time.clock() - start} seconds')


if __name__ == '__main__':
    main()