import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):

    tmpList = []

    if n > 0 :
        for i in range(n) :
            tmpList.append(string)

    return ''.join(tmpList)

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    index = 0

    for num in nums :
        if index < 4 and num == 9 :
            return True
        else :
            index += 1

    return False

# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):

    if len(string) < 2 :
        return 0

    index = 0
    lastCharacters = string[-2:]
    for i in range(len(string)-1) :
        tmpSubString = string[i:i+2]
        if(tmpSubString == lastCharacters) :
            index += 1

    return index-1


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
