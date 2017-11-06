#Validation
def checkInt(num):  #Confirms if the string passed in is made up of only integers
    if str.isdigit(num):
        return True
    return False
          

def validateInputs (minIV,maxIV,interval,maxRange,minRange):
    inputs = [minIV,maxIV,interval]  #Makes it easy to check all the inputs using for loops
    emptyCheck = []
    #Checks that none of the inputs are empty
    for i in range(0,3):
        if inputs[i] == "":
            emptyCheck.append(True)

    
    if any(emptyCheck):
        print("Type something in the boxes")#Error returned
        return False
    
    intCheck = []
    for i in range(0,3):  #Uses function checkInt()
        if checkInt(inputs[i]):
            intCheck.append(True)
        else:
            intCheck.append(False)

    if all(intCheck):  #If all are only numbers, convert them to intergers
            maxIV = int(maxIV)
            minIV = int(minIV)
            interval = int(interval)
    else:
            print("Enter integers only")
            return False

    if minIV >= maxIV:  #Ensures the minimum isn't larger than the maximum
            print("Your minimum value should be smaller than the maximum value")
            return False

    if minIV < minRange or maxIV > maxRange:  #Checks that both numbers are within the range
            print("Both the minimum and maximum should be between 0-100")
            return False
        
    noOfIntervals = ((maxIV - minIV) // interval)  + 1 #Calculates the number of intervals
    if noOfIntervals < 5:
            print("Make your range larger or decrease the interval")
            return False
        
    if noOfIntervals > 10:
            print("Make your range smaller or increase the interval")
            return False

    intervalMatch = (maxIV - minIV) % interval == 0
    #This will be true if the interval lines up with the max value
    
    if not(intervalMatch):
        print("Change the interval or maximum value as the values don't line up")
        return False
    
    return True  #If all the previous checks have passed, return true


