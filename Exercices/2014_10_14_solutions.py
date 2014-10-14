import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(str, n):
  result = ""
  for i in range(n):  # range(n) is [0, 1, 2, .... n-1]
    result = result + str  # could use += here
  return result


# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.

def array_front9(nums):
  # First figure the end for the loop
  end = len(nums)
  if end > 4:
    end = 4

  for i in range(end):  # loop over index [0, 1, 2, 3]
    if nums[i] == 9:
      return True
  return False


 #Given a string, return the count of the number of times
 #that a substring length 2 appears  in the string and also as
 #the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).

def last2(str):
  # Screen out too-short string case.
  if len(str) < 2:
    return 0

  # last 2 chars, can be written as str[-2:]
  last2 = str[len(str)-2:]
  count = 0

  # Check each substring length 2 starting at i
  for i in range(len(str)-2):
    sub = str[i:i+2]
    if sub == last2:
      count = count + 1

  return count


# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):

    def testArrayFront9(self):
        self.assertEqual(array_front9([1, 2, 9, 3, 4]) , True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]) , False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]) , False)

    def testStringTimes(self):
        self.assertEqual(string_times('Hel', 2),'HelHel' )
        self.assertEqual(string_times('Toto', 1),'Toto' )
        self.assertEqual(string_times('P', 4),'PPPP' )

    def testLast2(self):
        self.assertEqual(last2('hixxhi') , 1)
        self.assertEqual(last2('xaxxaxaxx') , 1)
        self.assertEqual(last2('axxxaaxx') , 2)



def main():
    unittest.main()

if __name__ == '__main__':
    main()
