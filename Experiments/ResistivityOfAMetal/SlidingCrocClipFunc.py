
wireLeft = 100
wireWidth = 50
maxLength = 100
interval = 10
crocPoint = 100,100
currentLength = 0


def moveCrocClip(crocPoint,currentLength):
    if crocPoint[0] == wireLeft:
        print("RECORD VALUE")
        currentLength += interval

    crocPointx = crocPoint[0] + 1
    nextRecordPoint = wireLeft + (wireWidth * (currentLength+interval) / maxLength)
    if crocPointx == nextRecordPoint:
        print("RECORD VALUE")
        #current, resistance = genValue(self.currentLength)
        currentLength += interval
        #sendValues(resistance, current)

    return (crocPointx, crocPoint[1]),currentLength

for i in range(50):
    crocPoint,currentLength = moveCrocClip(crocPoint,currentLength)
    print("Point: ",crocPoint)
    print("CurrentLength: ",currentLength)
