import sys
import traceback

from PyQt6.QtCore import QRunnable, pyqtSlot
from gui.events.worker_signals import WorkerSignals

class Worker(QRunnable):
    """Worker thread.

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread.
                     Supplied args and kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    """
    
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.thread_id = kwargs.get("thread_id", 0)
        self.cancelled = False
        self.has_ended = False

        self.kwargs["progress_callback"] = self.signals.progress

    @pyqtSlot()
    def run(self):
        """Initialize and run the function with the passed args and kwargs"""
        try:
            if self.cancelled:
                return
            
            result = self.fn(*self.args, **self.kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            if result is not None:
                self.signals.result.emit(result)
        finally:
            self.signals.finished.emit(self.thread_id)
            self.has_ended = True