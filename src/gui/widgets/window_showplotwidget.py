import os

os.environ["QT_API"] = "PyQt6"

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from gui.events.mpl_canvas import MplCanvas

class PlotWindow(QWidget):
      def __init__(self, data):
        super().__init__()

        self.data = data

        sc = MplCanvas(self, width=10, height=10, dpi=100)
        sc.axes.imshow(self.data)
        sc.axes.axis("off")
        toolbar = NavigationToolbar(sc, self)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        self.setLayout(layout)
        