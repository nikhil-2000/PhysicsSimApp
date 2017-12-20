import prettytable
import matplotlib.pyplot as plt
from math import *
import numpy as np


voltage = 20
resistivity = 1 * 10 ** -6
crossSectionArea = pi * (0.02 * 10 ** -2) ** 2
xPoints = []
yPoints = []

def genValues(currentLength):

    if currentLength == 0:
        return 0, 0

    resistance = resistivity * currentLength / crossSectionArea
    current = voltage / resistance

    # Rounding both values to reasonable number of signiicant figures
    return current, resistance

tbl = prettytable.PrettyTable(["Length","Current","Resistance"])

currentLength = 50
for i in range(6):
    current,resistance = genValues(currentLength)
    currentOut = round(current, 3)
    resistanceOut = round(resistance, 3)
    tbl.add_row([currentLength,currentOut,resistanceOut])
    xPoints.append(currentLength)
    yPoints.append(resistance)
    currentLength += 10

print(tbl)

def createGraph(xPoints, yPoints):
    plt.scatter(xPoints, yPoints)
    plt.plot(np.unique(xPoints), np.poly1d(np.polyfit(xPoints, yPoints, 1))(np.unique(xPoints)))
    plt.xlabel("Current Length/cm")
    plt.ylabel("Resistance/Ω")
    plt.savefig("graph.png")
    gradient = calcGradient(xPoints, yPoints)
    yIntercept = calcYintercept(gradient, xPoints[0], yPoints[0])
    return gradient, yIntercept

def calcGradient(xPoints, yPoints):
    return (yPoints[-1] - yPoints[0]) / (xPoints[-1] - xPoints[0])

def calcYintercept(gradient, xPoint, yPoint):
    return (yPoint - (gradient * xPoint))

gradient,yInt = createGraph(xPoints,yPoints)

print("Gradient:", round(gradient,3))
print("Y-Intercept:", round(yInt,3))

resistivityFromGraph = gradient * crossSectionArea
print("Calculated Resistivity: ",resistivityFromGraph)
print("Actual Resistivity: ",resistivity)