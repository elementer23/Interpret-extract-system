from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QLayout,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QHBoxLayout,
    QWidget,
    QProgressBar
    )

class ProgressOverviewWindow(QWidget):
    """
    This widget is essential enough, that it actually deserves a description.
    The ProgressOverviewWindow is essentially used to display the progress
    of each thread that is run in the system. It keeps track of the id,
    the percentage of a function and which task is currently done.

    This window only goes paired with the threadhandler and the standard
    functionalities that are required for the threads. Look at the basic setup
    in each window, that uses the threadhandler. 

    IMPORTANT?! when importing, don't import the class. Import the get_progress_overview function instead.
    This class requires a singular instance to work properly or else a new window will be opened for each
    new event.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Threading progression")

        self.MIN_HEIGHT = 120
        self.MAX_DYNAMIC_HEIGHT = 450

        self.setMinimumSize(QSize(600, self.MIN_HEIGHT))
        self.setMaximumSize(QSize(1000, 900))

        self.loaded_progressbars = {}

        main_layout = QVBoxLayout()
        scroll_view = QScrollArea()
        scroll_view.setWidgetResizable(True)
        scroll_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)
        self.content_layout.addStretch() 

        scroll_view.setWidget(content_widget)
        main_layout.addWidget(scroll_view)
        self.setLayout(main_layout)

    def adjust_window_height(self):
        """Calculates content height and resizes the window dynamically."""
        self.content_layout.activate()
        
        layout_hint = self.content_layout.minimumSize().height()
        margins = self.layout().contentsMargins()
        total_needed_height = layout_hint + margins.top() + margins.bottom() + 20

        target_height = max(self.MIN_HEIGHT, min(total_needed_height, self.MAX_DYNAMIC_HEIGHT))
        
        self.resize(self.width(), target_height)

    def add(self, task_data: tuple):
        """
        This function adds a new progressbar to the progress overview, 
        based on the thread_id. This functionality only has to be called once
        inside of the windows that uses threading. Look at the basic setup in the windows
        that use threading, for an example.
        """
        thread_id, task = task_data
        if thread_id in self.loaded_progressbars:
            return

        row = QHBoxLayout()
        current_task = QLabel(f"Task: ({task})")
        short_id = str(thread_id)[:8]
        current_thread = QLabel(f"Event #{short_id}")
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        progress_bar.setTextVisible(True)
        progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_bar.setFormat("Loading function... %p%")

        row.addWidget(current_task)
        row.addWidget(current_thread)
        row.addWidget(progress_bar)

        self.content_layout.insertLayout(self.content_layout.count() - 1, row)
        self.loaded_progressbars[thread_id] = progress_bar

        self.adjust_window_height()

    def update_progress(self, data: tuple):
        """
        This function updates the progress of the progressbar,
        depending on which thread_id belongs to the given progressbar.
        
        Does not require any further setup other than emitting it once
        inside of the window that uses threading. 

        Look inside windows that use threading for an example

        :type data: tuple
        :parameter data: this contains a thread_id, progression value and a message. 
        """
        thread_id, val, msg = data
        if thread_id in self.loaded_progressbars:
            self.loaded_progressbars[thread_id].setValue(int(val))
            self.loaded_progressbars[thread_id].setFormat(f"{msg}")

    def remove(self, thread_id: str):
        """
        This function removes the progressbar once the event has been completed.
        Removes based on the corresponding thread_id. 
        Will close the progression window, once there are no more events left that are running.

        Does not require any further setup other than emitting it once
        inside of the window that uses threading. 

        Look inside windows that use threading for an example
        """
        self.loaded_progressbars.pop(thread_id, None)
        short_id = str(thread_id)[:8]

        correct_widget = self.retrieve_widget_layout_in_scroll_view(label_name=f"Event #{short_id}")
        if correct_widget:
            while correct_widget.count():
                child = correct_widget.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            self.content_layout.removeItem(correct_widget)
            correct_widget.deleteLater()

        if not self.loaded_progressbars:
            self._close_window()
        else:
            self.adjust_window_height()

    def retrieve_widget_layout_in_scroll_view(self, label_name: str):
        """
        This function simply retrieves the corresponding widget inside of the
        progression window. Based on the label name. 
        """
        for i in range(self.content_layout.count() - 1):
            item = self.content_layout.itemAt(i)
            if item and item.layout():
                layout = item.layout()
                for y in range(layout.count()):
                    widget = layout.itemAt(y).widget()
                    if isinstance(widget, QLabel) and widget.text() == label_name:
                        return layout
        return None

    def open_window(self):
        self.show()

    def _close_window(self):
        self.close()

    def closeEvent(self, event):
        self.setParent(None)
        event.accept()

_progress_overview_instance = None

def get_progress_overview():
    """
    This function calls a 'singleton' instance of the ProgressOverviewWindow.
    Making this the default way to use and import the class. 
    """
    global _progress_overview_instance
    if _progress_overview_instance is None:
        _progress_overview_instance = ProgressOverviewWindow()
    return _progress_overview_instance