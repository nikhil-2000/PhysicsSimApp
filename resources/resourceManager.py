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
internalResistanceDiagram = appresources.get_path("InternalResistanceDiagram.png")
resistivityOfAMetalDiagram = appresources.get_path("ResistivityOfAMetalDiagram.png")
rulerImg = appresources.get_path("ruler.png")
voltmeterImg = appresources.get_path("voltmeter.png")

