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
        self.maxRange = 1000
        #Gives a clearer output of error messages for each test
        time.sleep(1)

    def test_normalInputs(self):  #Tests that the normal values are accepted by the algorithm
        validInputs,e= v.validateNewton2ndLaw("5","1","50",self.minRange,self.maxRange)
        print(e)

        self.assertEqual(validInputs,True)

    def test_emptyCheck(self):  #Tests that the inputs aren't empty
        validInputs,e= v.validateNewton2ndLaw("","","",self.maxRange,self.minRange)
        self.assertEqual(validInputs,False)

    def test_floatInputs(self):  #Tests that floats are rejected
        validInputs,e= v.validateNewton2ndLaw("6","4.2","100",self.maxRange,self.minRange)
        self.assertEqual(validInputs,False)

    def test_negativeInputs(self):  #Tests that negative numbers are rejected
        validInputs,e= v.validateNewton2ndLaw("-12","0","2",self.maxRange,self.minRange)
        self.assertEqual(validInputs,False)

    def test_moreThan10Intervals(self):  #Tests that there aren't too many intervals
        validInputs,e= v.validateNewton2ndLaw("11","0","50",self.maxRange,self.minRange)
        self.assertEqual(validInputs,False)

    def test_lessThan5Intervals(self):  #Tests that there aren't too little intervals
        validInputs,e= v.validateNewton2ndLaw("4","0","200",self.maxRange,self.minRange)
        self.assertEqual(validInputs,False)

    def test_lowerThanRange(self):  #Tests that IV can't be inputted below the minimum range
        validInputs,e= v.validateNewton2ndLaw("-1","3","100",self.maxRange,self.minRange)
        self.assertEqual(validInputs,False)

    def test_higherThanRange(self):  #Tests that the IV can't be inputted above the maximum range
        validInputs,e= v.validateNewton2ndLaw("9","3","100",self.maxRange,self.minRange)
        self.assertEqual(validInputs,False)

    def test_exceedMaxWeights(self):
        validInputs, e = v.validateNewton2ndLaw("9", "3", "100", self.maxRange, self.minRange)
        self.assertEqual(validInputs, False)



if __name__ == "__main__":
    unittest.main(verbosity = 2)  #Presents the test in a more readable way
