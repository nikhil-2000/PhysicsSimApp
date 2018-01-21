import os
import sys
##sys.path.append(os.path.abspath('../externalModules/pythonUtils/utils'))
sys.path.append(os.path.abspath('..'))
#The previous three lines were taken from https://stackoverflow.com/questions/10272879/how-do-i-import-a-python-script-from-a-sibling-directory
#It explained how to access modules in sibling directories
from externalModules.pythonUtils.utils import resources as res




apppath = os.path.dirname(os.path.abspath(__file__))
appresources = res.Resources(os.path.join(apppath, "images"))
#Above two lines: Uses code which allows me to access all images and loads them
#Taken from: http://python-utilities.readthedocs.io/en/latest/resources.html
#Access some images
absoluteZeroDiagramImg = appresources.get_path("AbsoluteZeroDiagram.png")
ammeterImg = appresources.get_path("ammeter.png")
atomImg = appresources.get_path("atom.png")
batteryImg = appresources.get_path("battery.png")
beakerImg = appresources.get_path("beaker.png")
rulerImg = appresources.get_path("ruler.png")
voltmeterImg = appresources.get_path("voltmeter.png")
thermometerImg = appresources.get_path("thermometer.png")
pressureGaugeImg = appresources.get_path("pressureGauge.png")
internalResistanceEquations = appresources.get_path("internalResistanceEquations.PNG")
resistivityEquations = appresources.get_path("resistivityEquations.PNG")
resistivityDefinitions = appresources.get_path("resistivityDefinitions.PNG")
absoluteZero = appresources.get_path("pressureTemperatureEquation.PNG")
cartImg = appresources.get_path("cart.png")
pulleyImg = appresources.get_path("pulley.png")
massHolderImg = appresources.get_path("massHolder.png")
dataLoggerImg = appresources.get_path("dataLogger.png")
accelerationEquation = appresources.get_path("accelerationEquation.PNG")
variableResistorImg = appresources.get_path("variableResistor.png")
arrowImg = appresources.get_path("arrow.png")