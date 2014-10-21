#!/usr/bin/python2.4 -tt
# -*- coding: utf-8 -*-
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Additional basic string exercises

# D. verbing
# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
def verbing(s):
  
  # Cas où la longueur est inférieure à 3 
  if len(s) < 3 :
    return s

  # Cas où la fin du mot est 'ing'
  elif s.endswith('ing') :
    return s + 'ly'

  # Cas où le mot fait plus de 3 lettres et ne se termine pas par 'ing'
  else :
    return s + 'ing'


# E. not_bad
# Given a string, find the first appearance of the
# substring 'not' and 'bad'. If the 'bad' follows
# the 'not', replace the whole 'not'...'bad' substring
# with 'good'.
# Return the resulting string.
# So 'This dinner is not that bad!' yields:
# This dinner is good!
def not_bad(s):
  
  # Récupération de l'index du premier 'not' et du premier 'bad'
  firstNotIndex = s.find('not')
  firstBadIndex = s.find('bad')

  # Si il n'y a pas de not, de bad ou que le bad est avant le not on arrete
  if firstBadIndex == -1 or firstNotIndex == -1 or firstBadIndex < firstNotIndex :
    return s

  # Sinon on récupère la sous chaine avant le not et celle apres le bad
  stringBeforeNot = s[:firstNotIndex]
  stringAfterBad = s[firstBadIndex+3:] if firstBadIndex+3 < len(s) else ''

  # Retour de la chaine concaténée avec 'good' au milieu
  return stringBeforeNot + 'good' + stringAfterBad


# F. front_back
# Consider dividing a string into two halves.
# If the length is even, the front and back halves are the same length.
# If the length is odd, we'll say that the extra char goes in the front half.
# e.g. 'abcde', the front half is 'abc', the back half 'de'.
# Given 2 strings, a and b, return a string of the form
#  a-front + b-front + a-back + b-back
def front_back(a, b):
  
  # Calcul de a-front et a-back
  aMiddle = len(a) // 2 if len(a) % 2 == 0 else len(a) // 2 + 1 
  aFront = a[:aMiddle]
  aBack = a[aMiddle:]

  # Calcul de b-front et b-back
  bMiddle = len(b) // 2 if len(b) % 2 == 0 else len(b) // 2 + 1 
  bFront = b[:bMiddle]
  bBack = b[bMiddle:]

  # Retour de la chaine finale avec la bonne concaténation
  return aFront + bFront + aBack + bBack


# Simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))


# main() calls the above functions with interesting inputs,
# using the above test() to check if the result is correct or not.
def main():
  print 'verbing'
  test(verbing('hail'), 'hailing')
  test(verbing('swiming'), 'swimingly')
  test(verbing('do'), 'do')

  print
  print 'not_bad'
  test(not_bad('This movie is not so bad'), 'This movie is good')
  test(not_bad('This dinner is not that bad!'), 'This dinner is good!')
  test(not_bad('This tea is not hot'), 'This tea is not hot')
  test(not_bad("It's bad yet not"), "It's bad yet not")

  print
  print 'front_back'
  test(front_back('abcd', 'xy'), 'abxcdy')
  test(front_back('abcde', 'xyz'), 'abcxydez')
  test(front_back('Kitten', 'Donut'), 'KitDontenut')

if __name__ == '__main__':
  main()
