import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    largestring = ""
    for count in range(n):
        largestring = largestring + string
    return largestring

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    #isOK = False
    count = 0
    for num in nums:
        count = count+1
        if (num == 9):
            isOK = True
            break
    if count < 5 and isOK:
        return isOK
    else:
        return False
# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    lasttwo=string[-2:]
    count = 0
    for index in range(0, len(string)-2):
        if string[index:index+2] == lasttwo:
            count = count + 1
    return count
    
# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):
    
    def testStringTimes(self):
        self.assertEqual(string_times('Hel', 2),'HelHel' )
        self.assertEqual(string_times('Toto', 1),'Toto' )
        self.assertEqual(string_times('P', 4),'PPPP' )
    
    def testArrayFront9(self):
        self.assertEqual(array_front9([1, 2, 9, 3, 4]) , True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]) , False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]) , False)
    
    def testLast2(self):
        self.assertEqual(last2('hixxhi') , 1)
        self.assertEqual(last2('xaxxaxaxx') , 1)
        self.assertEqual(last2('axxxaaxx') , 2)
        



def main():
    unittest.main()

if __name__ == '__main__':
    main()