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
