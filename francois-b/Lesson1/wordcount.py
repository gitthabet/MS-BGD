# -*- coding: utf-8 -*-
"""
Created on Sun Oct 12 23:54:18 2014

@author: Paco
"""

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

"""Wordcount exercise
Google's Python class

The main() below is already defined and complete. It calls print_words()
and print_top() functions which you write.

1. For the --count flag, implement a print_words(filename) function that counts
how often each word appears in the text and prints:
word1 count1
word2 count2
...

Print the above list in order sorted by word (python will sort punctuation to
come before letters -- that's fine). Store all the words as lowercase,
so 'The' and 'the' count as the same word.

2. For the --topcount flag, implement a print_top(filename) which is similar
to print_words() but which prints just the top 20 most common words sorted
so the most common word is first, then the next most common, and so on.

Use str.split() (no arguments) to split on all whitespace.

Workflow: don't build the whole program at once. Get it to an intermediate
milestone and print your data structure and sys.exit(0).
When that's working, try for the next milestone.

Optional: define a helper function to avoid code duplication inside
print_words() and print_top().

"""

import sys
from operator import itemgetter
from collections import Counter

#####################################
# test with alixe.txt and small.txt
#####################################

# Sort by name with a counter
def print_words(filename):
    file = open(filename, 'r')
    text = file.read().lower().split()
    # itemgetter(0) is similar to key=lambda elem: elem[0]
    return sorted(Counter(text).items(), key=itemgetter(0))

# Sort by number and return the 20 most common    
def print_top(filename):
    file = open(filename, 'r')
    text = file.read().lower().split()
    return Counter(text).most_common(20)      

###

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
  if len(sys.argv) != 3:
    print 'usage: ./wordcount.py {--count | --topcount} file'
    sys.exit(1)

  option = sys.argv[1]
  filename = sys.argv[2]
  if option == '--count':
    print_words(filename)
  elif option == '--topcount':
    print_top(filename)
  else:
    print 'unknown option: ' + option
    sys.exit(1)

# if __name__ == '__main__':
main()
