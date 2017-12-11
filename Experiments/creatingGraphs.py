import matplotlib.pyplot as plt
import numpy as np

def createGraph(xPoints, yPoints,xLabel,yLabel):
    plt.scatter(xPoints, yPoints)
    plt.plot(np.unique(xPoints), np.poly1d(np.polyfit(xPoints, yPoints, 1))(np.unique(xPoints)))
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.savefig("graph.png")
    gradient = calcGradient(xPoints, yPoints)
    yIntercept = calcYintercept(gradient, xPoints[0], yPoints[0])
    return gradient, yIntercept

def calcGradient(xPoints, yPoints):
    return (yPoints[-1] - yPoints[0]) / (xPoints[-1] - xPoints[0])

def calcYintercept(gradient, xPoint, yPoint):
    return (yPoint - (gradient * xPoint))
