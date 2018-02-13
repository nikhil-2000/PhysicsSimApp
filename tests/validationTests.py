import os
import sys
sys.path.append(os.path.abspath('..'))
#Allows me to access the file above and import scripts/modules from the root

import Validation.validation as v#Imports the file where the validation algorithm is held
import unittest #The python module for writing unit tests
import time#The python module for time

class TestValidationFunction(unittest.TestCase):
    def setUp(self):  #This method is ran before each test
        #These two variables are constant for each test
        self.minRange = 0
        self.maxRange = 100
        #Gives a clearer output of error messages for each test
        time.sleep(1)

    def test_normalInputs(self):  #Tests that the normal values are accepted by the algorithm
        validInputs = v.validateInputs("10","100","10",self.maxRange,self.minRange)
        self.assertEqual(validInputs[0],True)

    def test_emptyCheck(self):  #Tests that the inputs aren't empty
        validInputs = v.validateInputs("","","",self.maxRange,self.minRange)
        self.assertEqual(validInputs[0],False)

    def test_floatInputs(self):  #Tests that floats are rejected
        validInputs = v.validateInputs("3.2","4.2","0.2",self.maxRange,self.minRange)
        self.assertEqual(validInputs[0],False)

    def test_negativeInputs(self):  #Tests that negative numbers are rejected
        validInputs = v.validateInputs("-12","0","2",self.maxRange,self.minRange)
        self.assertEqual(validInputs[0],False)

    def test_moreThan10Intervals(self):  #Tests that there aren't too many intervals
        validInputs = v.validateInputs("0","11","1",self.maxRange,self.minRange)
        self.assertEqual(validInputs[0],False)

    def test_lessThan5Intervals(self):  #Tests that there aren't too little intervals
        validInputs = v.validateInputs("0","30","10",self.maxRange,self.minRange)
        self.assertEqual(validInputs[0],False)

    def test_lowerThanRange(self):  #Tests that IV can't be inputted below the minimum range
        validInputs = v.validateInputs("-10","60","10",self.maxRange,self.minRange)
        self.assertEqual(validInputs[0],False)

    def test_higherThanRange(self):  #Tests that the IV can't be inputted above the maximum range
        validInputs = v.validateInputs("90","160","10",self.maxRange,self.minRange)
        self.assertEqual(validInputs[0],False)

    def test_intervalMatch(self):  #Tests that the interval and the max range match
        # For example, if I kept adding 2 to 75, you wouldn't arrive at 90
        # This tests ensures that the numbers align correctly
        validInputs = v.validateInputs("75","90","2",self.maxRange,self.minRange)
        self.assertEqual(validInputs[0],False)

    def test_minMoreThanMax(self):  #Tests that the maximum value for the IV is below the minimum value
        validInputs = v.validateInputs("60","50","0",self.maxRange,self.minRange)
        self.assertEqual(validInputs[0],False)


if __name__ == "__main__":
    unittest.main(verbosity = 2)  #Presents the test in a more readable way
