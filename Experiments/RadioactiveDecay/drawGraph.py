import matplotlib.pyplot as plt
import numpy as np

def clearFig():
    #Empties figure at the start of each simulation
    plt.gcf().clear()


class Graph():
    def __init__(self,xLbl,yLbl,graphName,subplot):
        #Lists represent the coordinates
        self.xPoints = []
        self.yPoints = []
        #Graph title
        self.graphName = graphName
        #Values to be calculated
        self.gradient = 0
        self.yInt = 0
        #First part of the string is the subplot size, sublot represents the position in the subplot
        num = str("12") + str(subplot)
        #Adds the graph to a subplot with the relevant labels
        self.graph = fig.add_subplot(int(num))
        self.graph.set_xlabel(xLbl)
        self.graph.set_ylabel(yLbl)


    def drawGraph(self,isExponential):
        #Plots coordinates
        self.graph.scatter(self.xPoints, self.yPoints)
        #Draws line of best fit
        if not isExponential:
            self.graph.plot(np.unique(self.xPoints), np.poly1d(np.polyfit(self.xPoints, self.yPoints, 1))(np.unique(self.xPoints)))
        #Sets gradient and y intercept
        self.calcGradient()
        self.calcYintercept()
        #Spaces out subplots
        fig.subplots_adjust(wspace = 0.3)
        #Saves graph as image
        fig.savefig("graphs.png")


    def calcGradient(self):
        #Takes first and last point to find gradient
        self.gradient = (self.yPoints[-1] - self.yPoints[0]) / (self.xPoints[-1] - self.xPoints[0])
        self.gradient = round(self.gradient,6)


    def calcYintercept(self):
        # Finds the y intercept using the gradient
        self.yInt = (self.yPoints[0] - (self.gradient * self.xPoints[0]))
        self.yInt = round(self.yInt,2)



fig = plt.figure()





