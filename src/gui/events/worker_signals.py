from PyQt6.QtCore import QObject, pyqtSignal

class WorkerSignals(QObject):
    """Signals from a running worker thread.

    finished
        str thread_id

    error
        tuple (exctype, value, traceback.format_exc())

    result
        object data returned from processing, anything

    progress
        tuple (thread_id, progress_value)
    """

    finished = pyqtSignal(str)  # thread_id
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(tuple)  # (thread_id, progress_percentage)
