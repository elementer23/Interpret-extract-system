from PyQt6.QtCore import QObject, pyqtSignal

class ErrorHubSignals(QObject):
    error_raised = pyqtSignal(str, str)

