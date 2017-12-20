import matplotlib.pyplot as plt
import numpy as np


def createGraph(xPoints,yPoints,xLbl,yLbl):
    plt.scatter(xPoints, yPoints)
    plt.plot(np.unique(xPoints), np.poly1d(np.polyfit(xPoints, yPoints, 1))(np.unique(xPoints)))
    plt.xlabel(xLbl)
    plt.ylabel(yLbl)
    plt.savefig("graph.png")
    g = calcGradient(xPoints,yPoints)
    return g,calcYintercept(g,xPoints[0],yPoints[0])

def calcGradient(xPoints, yPoints):
    return (yPoints[-1] - yPoints[0]) / (xPoints[-1] - xPoints[0])

def calcYintercept(gradient, xPoint, yPoint):
    return  (yPoint - (gradient * xPoint))


