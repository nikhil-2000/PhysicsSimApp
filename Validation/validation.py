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
        error = "Type something in the boxes"#Error returned
        return False,error
    
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
        error = "Enter integers only"
        return False,error

    if minIV >= maxIV:  #Ensures the minimum isn't larger than the maximum
        error = "Your minimum value should be smaller than the maximum value"
        return False,error

    if minIV < minRange or maxIV > maxRange:  #Checks that both numbers are within the range
        error = "Both the minimum and maximum should be between"+str(minRange)+"-"+str(maxRange)
        return False,error

    if maxIV * interval == 0:
        error = "Your maximum or interval can't equal zero"
        return False,error

    noOfIntervals = ((maxIV - minIV) // interval)  + 1 #Calculates the number of intervals
    if noOfIntervals < 5:
        error = "Make your range larger or decrease the interval"
        return False,error
        
    if noOfIntervals > 10:
        error = "Make your range smaller or increase the interval"
        return False,error

    intervalMatch = (maxIV - minIV) % interval == 0
    #This will be true if the interval lines up with the max value
    
    if not(intervalMatch):
        error = "Change the interval or maximum value as the values don't line up"
        return False,error
    
    return True,None  #If all the previous checks have passed, return true


def validateNewton2ndLaw(cartWeight,massWeight,weightSize,minRange,maxRange):
    inputs = [cartWeight, massWeight,weightSize]  # Makes it easy to check all the inputs using for loops
    emptyCheck = []

    print(inputs)
    # Checks that none of the inputs are empty
    for i in range(0, 3):
        if inputs[i] == "":
            emptyCheck.append(True)

    if any(emptyCheck):
        error = "Type something in both boxes a select a weight size"  # Error returned
        return False, error

    intCheck = []
    for i in range(0, 3):  # Uses function checkInt()
        if checkInt(inputs[i]):
            intCheck.append(True)
        else:
            intCheck.append(False)

    if all(intCheck):  # If all are only numbers, convert them to integers
        cartWeight = int(cartWeight)
        massWeight = int(massWeight)
        weightSize = int(weightSize)
    else:
        error = "Enter integers only"
        return False, error

    if cartWeight + massWeight > 10:#Makes sure there are less than 10 weights
        error = "The maximum amount of weights allowed is 10"
        return False,error


    if massWeight <= 0:  # Check that there are weights are on the mass holder
        error = "Start with some weights on the mass holder"
        return False, error

    if (cartWeight + massWeight) * weightSize > maxRange:  # Limit total weight to 1000g
        error = "The total weight in the system should be less than"+ str(maxRange)
        return False, error

    if cartWeight > 10 or cartWeight < 5:#Ensures 5 to ten recordings
        error = "You should have 5-10 recordings"
        return False, error

    return True, None  # If all the previous checks have passed, return true


