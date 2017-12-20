import matplotlib.pyplot as plt
import numpy as np

class Graph():
    def __init__(self,xLbl,yLbl,graphName,subplot):
        self.xPoints = []
        self.yPoints = []
        self.graphName = graphName
        self.gradient = 0
        self.yInt = 0
        num = str("12") + str(subplot)
        self.graph = fig.add_subplot(int(num))
        self.graph.set_xlabel(xLbl)
        self.graph.set_ylabel(yLbl)


    def drawGraph(self):
        self.graph.scatter(self.xPoints, self.yPoints)
        self.graph.plot(np.unique(self.xPoints), np.poly1d(np.polyfit(self.xPoints, self.yPoints, 1))(np.unique(self.xPoints)))
        self.calcGradient()
        self.calcYintercept()
        fig.subplots_adjust(wspace = 0.3)
        fig.savefig("graphs.png")


    def calcGradient(self):
        self.gradient = (self.yPoints[-1] - self.yPoints[0]) / (self.xPoints[-1] - self.xPoints[0])
        self.gradient = round(self.gradient,1)


    def calcYintercept(self):
        self.yInt = (self.yPoints[0] - (self.gradient * self.xPoints[0]))
        self.yInt = round(self.yInt,1)

fig = plt.figure()





