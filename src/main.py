from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QTextEdit

import sys

# window_titles = [
#     'My App',
#     'My App',
#     'Still My App',
#     'Still My App',
#     'What on earth',
#     'What on earth',
#     'This is surprising',
#     'This is surprising',
#     'Something went wrong'
# ]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)
        self.label = QLabel("Clcik in this window")
        self.label.setMouseTracking(True)
        self.setCentralWidget(self.label)

    # def mouseMoveEvent(self, e):
    #     self.label.setText("mouseMoveEvent")

    # def mousePressEvent(self, e):
    #     self.label.setText("mousePressEvent")

    # def mouseReleaseEvent(self, e):
    #     self.label.setText("mouseReleaseEvent")

    # def mouseDoubleClickEvent(self, e):
    #     self.label.setText("mouseDoubleClickEvent")

        # self.n_times_clicked = 0
        # self.input_value = ""

        self.setWindowTitle("interpret & extract")

        # self.label = QLabel()

        # self.input = QLineEdit()
        # self.input.textChanged.connect(self.label.setText)
        # self.input.textEdited.connect(self.get_value_input)
        # self.input.textChanged.connect(self.input_changed)

        # self.button = QPushButton("Press Me!")
        # self.button.clicked.connect(self.button_clicked)

        # layout = QVBoxLayout()
        # layout.addWidget(self.input)
        # layout.addWidget(self.button)
        # layout.addWidget(self.label)

        # container = QWidget()
        # container.setLayout(layout)

        # self.button = QPushButton("Press Me!")
        # self.button.clicked.connect(self.the_button_was_clicked)

        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(1000, 900))

        # self.windowTitleChanged.connect(self.the_window_title_changed)

        # self.setCentralWidget(self.button)
        # self.setCentralWidget(container)

    # def button_clicked(self):
    #     self.label.setText(self.input_value)

    # def get_value_input(self, value):
    #     self.input_value = value

    # def the_button_was_clicked(self):
    #     print("Clicked.")
    #     new_window_title = choice(window_titles)
    #     print("Setting Title: %s" % new_window_title)
    #     self.setWindowTitle(new_window_title)

    # def the_window_title_changed(self, window_title):
    #     print("Window title changed: %s" % window_title)

    #     if window_title == "Something went wrong":
    #         self.button.setDisabled(True)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()