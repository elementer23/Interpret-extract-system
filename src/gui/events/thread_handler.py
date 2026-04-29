import time
from gui.events.worker import Worker
from typing import Any
from PyQt6.QtCore import QThreadPool, QObject

class ThreadHandler(QObject):
    """Thread Handler.

    Inherits from QObject. Initializes a QThreadPool and keeps track of event progress, completion, errors and results.
    Connects with the Worker class, to emit these signals.

    """

    def __init__(self, parent = None):
        super().__init__(parent)
        self.event_tracker = {}
        self.threadpool = QThreadPool()
        self.thread_id = 0

    def _clean_threadpool(self, amount_of_workers: list) -> bool:
        if not amount_of_workers:
            self.threadpool.waitForDone()
            self.threadpool.disconnect()
            print("Finished working.")

    def _event_progress(self, data):
        thread_id, n = data
        print(f"Event #{thread_id}: {n:.1f}% done")

    def _event_complete(self, thread_id):
        print(f"Event #{thread_id} COMPLETE!")

    def _event_error(self, error: tuple):
        print("event error thread handler")
        for err in error:
            print(err)

    def _event_result(self, result):
        print(f"{result}")

    def run_event(self, fn, fn_out: Any | None, *args, **kwargs):
        """Runs the given event, by initializing a new Worker and adding them to the threadpool.
        A main vocal point, to initialize the threads with, if necessary.

        fn -> function to execute, fn_out -> function to initialize the output of the executed function.
        (if it can only be done on the main thread, else fill in None)

        :param callback: the function callback to run on the worker thread.
                         supplied args and kwargs from the given function will be passed to the worker.
        :type callback: function
        :param callback_out: the function callback to pass the output off the first function callback.
                             Mainly used if the output can only be initialized on the main thread.
                             Can be None, if the output does not have to be initialized on the main thread.
        :type callback_out: output initializer
        :param args: Arguments to pass to the callback function (Is required, even if value is nothing)
        :param kwargs: Keywords to pass to the callback function (Currently not in use)
        """
        self.thread_id += 1

        worker = Worker(fn, args, thread_id=self.thread_id)

        worker.signals.result.connect(fn_out if fn_out is not None else self._event_result)
        worker.signals.finished.connect(self._event_complete)
        worker.signals.progress.connect(self._event_progress)
        worker.signals.error.connect(self._event_error)

        self.event_tracker[self.thread_id] = worker
        self.threadpool.start(worker) 

        self._update_status()

    def track_progress(self, progress_callback, thread_id):
        """Tracks the progress of the thread.
        
        :param progress_callback: must be present as a parameter in the function to be called back (used as emit).
        :param thread_id: must be present as a parameter in the function to be called back (used to keep track which thread is used.)
        """
        for n in range(0, 5):
            time.sleep(1)
            progress = n * 100 / 4
            progress_callback.emit((thread_id, progress))

    def _update_status(self):
        thread_count = self.threadpool.maxThreadCount()
        active_thread_count = self.threadpool.activeThreadCount()
        print(f"Limit of threads available {thread_count}")
        print(f"Current amount of active threads {active_thread_count}")




    