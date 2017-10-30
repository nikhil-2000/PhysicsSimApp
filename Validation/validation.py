#Validation Tests
def checkInt(num):
    if str.isdigit(num):
        return True
    return False
          

def validateInputs (minIV,maxIV,interval):
    minRange = 0
    maxRange = 100
    inputs = [minIV,maxIV,interval]
    emptyCheck = []
    for i in range(0,3):
        if inputs[i] == "":
            emptyCheck.append(True)

    
    if any(emptyCheck):
        print("Type something in the boxes")
        return False
    
    intCheck = []
    for i in range(0,3):
        if checkInt(inputs[i]):
            intCheck.append(True)
        else:
            intCheck.append(False)

    print(intCheck)
    if all(intCheck):
            maxIV = int(maxIV)
            minIV = int(minIV)
            interval = int(interval)
    else:
            print("Enter integers only")
            return False
        
        
    if minIV >= maxIV:
            print("Your minimum value should be smaller than the maximum value")
            return False

    if minIV < minRange or maxIV > maxRange:
            print("Both the minimum and maximum should be between 0-100")
            return False
        
    noOfIntervals = ((maxIV - minIV) // interval)  + 1
    if noOfIntervals < 5:
            print("Make your range larger or decrease the interval")
            return False
        
    if noOfIntervals > 10:
            print("Make your range smaller or increase the interval")
            return False

    intervalMatch = (maxIV - minIV) % interval == 0
    
    if not(intervalMatch):
        errorMsg = "Change the interval or maximum value as the values don't line up"
        return False
    
    return True


