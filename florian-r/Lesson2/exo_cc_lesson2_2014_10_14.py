import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    n_string = string
    for i in range(1,n):
        n_string+=string

    return n_string
=======
    return
>>>>>>> 8659b647e91e601ed89958183ca6264a0886023c
=======
    return string*n
>>>>>>> c1d13ecbaeed672249831b4d716b7ee250cbb11b
=======
    result=""  
    for count in range (0,n):
        result = result+string
        count = count+1
    return result

>>>>>>> 53a9c9df5ab425bf6cab7ab7af2975b00854ad06

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
 results = False
 index = 0
 for num in nums:
    if index < 4 and num == 9:
     results = True
     index +=1
    else: index +=1
 return results
=======
    return
>>>>>>> 8659b647e91e601ed89958183ca6264a0886023c
=======
    
    for i in range (1,4):
        if nums[i]==9:
            return True
        else:
            return False
            
>>>>>>> c1d13ecbaeed672249831b4d716b7ee250cbb11b
=======
    def is_true(x):
        if x==9:
            return True
    nums_2 = filter(is_true, nums)
    if len(nums_) == 4:
        return True
>>>>>>> 53a9c9df5ab425bf6cab7ab7af2975b00854ad06

# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
<<<<<<< HEAD
<<<<<<< HEAD
 str_search=string[-2:]
 count = 0
 for x in range(0,len(string)-len(str_search)):
    if string[x:x+len(str_search)] == str_search:
        count += 1
 return count
=======
    return
>>>>>>> 8659b647e91e601ed89958183ca6264a0886023c
=======
    count=0
    for i in range(len(string-2)):
        if string[i:i+2]==string[-2:]:
            count=count+1
                
    return count
    
>>>>>>> c1d13ecbaeed672249831b4d716b7ee250cbb11b


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
