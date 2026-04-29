import os

os.environ["QT_API"] = "PyQt6"

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    """matplotlib canvas implementation of PyQt6
    Inherits the FigureCanvas class. Used so for matplotlib support, causing graphs and images to open in an PyQt6 window instead.

    :type width: integer
    :param width: width of the canvas, 10 by default.
    :type height: integer
    :param height: height of the canvas, 10 by default.
    :type dpi: integer
    :param dpi: dpi which the canvas should be generated with, 100 by default. 
    """
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)