EMF = 6
internalResistance = 20

def genValues(resistance):
    current = EMF/(resistance + internalResistance)
    voltage = resistance * current
    return current,voltage

print("(Current,Voltage)")
for i in range(1,10):
    print(genValues(i*10))
