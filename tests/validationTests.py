import validationChecks as v
import unittest

class TestValidationFunction(unittest.TestCase):
    def test_normalInputs(self):
        validInputs = v.validateInputs("10","100","10")
        self.assertEqual(validInputs,True)

    def test_floatInputs(self):
        validInputs = v.validateInputs("3.2","4.2","0.2")
        self.assertEqual(validInputs,False)

    def test_negativeInputs(self):
        validInputs = v.validateInputs("-12","0","2")
        self.assertEqual(validInputs,False)

    def test_moreThan10Intervals(self):
        validInputs = v.validateInputs("0","11","1")
        self.assertEqual(validInputs,False)

    def test_lessThan5Intervals(self):
        validInputs = v.validateInputs("0","30","10")
        self.assertEqual(validInputs,False)

    def test_lowerThanRange(self):
        validInputs = v.validateInputs("-10","60","10")
        self.assertEqual(validInputs,False)

    def test_higherThanRange(self):
        validInputs = v.validateInputs("90","160","10")
        self.assertEqual(validInputs,False)

    def test_intervalMatch(self):
        validInputs = v.validateInputs("75","90","2")
        self.assertEqual(validInputs,False)

    def test_minMoreThanMax(self):
        validInputs = v.validateInputs("60","50","0")
        self.assertEqual(validInputs,False)        


if __name__ == "__main__":
    unittest.main()
