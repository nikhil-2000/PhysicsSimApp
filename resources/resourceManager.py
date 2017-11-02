from external.pythonUtils.utils import resources as res
import os

apppath = os.path.dirname(os.path.abspath(__file__))
appresources = res.Resources(os.path.join(apppath, "resources"))
# Access some images
absoluteZeroDiagramImg = appresources.get_path("AbsoluteZeroDiagram.png")
ammeterImg = appresources.get_path("ammeter.png")
atomImg = appresources.get_path("atom.png")
batteryImg = appresources.get_path("battery.png")
beakerImg = appresources.get_path("beaker.png")
internalResistanceDiagram = appresources.get_path("InternalResistanceDiagram.png")
resistivityOfAMetalDiagram = appresources.get_path("ResistivityOfAMetalDiagram.png")
rulerImg = appresources.get_path("ruler.png")
voltmeterImg = appresources.get_path("voltmeter.png")


