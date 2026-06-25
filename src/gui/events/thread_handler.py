import time
from gui.events.worker import Worker
from typing import Any
from PyQt6.QtCore import QThreadPool, QObject, pyqtSignal
from error.error_hub import ErrorHub
import uuid
import gc
import ctypes

class ThreadHandler(QObject):
    """Thread Handler.

    Inherits from QObject. Initializes a QThreadPool and keeps track of event progress, completion, errors and results.
    Connects with the Worker class, to emit these signals. The threadpool is global, so it's used throughout the entire application.

    """
    func_finished = pyqtSignal(tuple)
    event_finished = pyqtSignal(str)
    event_started = pyqtSignal(tuple)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.event_tracker = {}
        self.threadpool = QThreadPool.globalInstance()

    def __clean_threadpool(self):
        self.threadpool.waitForDone()
        self.threadpool.disconnect()
        print("Finished working.")

    def __event_progress(self, data):
        thread_id, n = data
        time.sleep(0.1)
        print(f"\rEvent #{thread_id}: {n:.1f}% done", end="", flush=True)

    def __event_complete(self, thread_id):
        self.event_finished.emit(thread_id)

        worker = self.event_tracker.get(thread_id)

        if worker:
            try:
                worker.signals.progress.disconnect()
                worker.signals.result.disconnect()
                worker.signals.finished.disconnect()
                worker.signals.error.disconnect()
            except TypeError:
                pass
        
        self.pop_event_tracker(thread_id)

        if self.get_event_tracker_len() == 0:
            self.force_garbage_collection()
        
        print(f"\nEvent #{thread_id} COMPLETE!")

    def __event_error(self, error: tuple):
        print("event error thread handler")
        ErrorHub.error_msg("Something went wrong, check the terminal prints in the code.", "critical")
        for err in error:
            print(err)

    def __event_result(self, result):
        print(f"{result}")
        ErrorHub.error_msg(f"{result}", "information")

    def get_event_tracker_len(self) -> int:
        return len(self.event_tracker)
    
    def pop_event_tracker(self, thread_id):
        self.event_tracker.pop(thread_id, None)

    def run_event(self, fn, fn_out: Any | None, task: str="unknown", *args, **kwargs):
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
        :type task: str
        :param task: add a task name to keep track of which task is currently running ('unknown' as default)
        :param args: Arguments to pass to the callback function (Is required, even if value is nothing)
        :param kwargs: Keywords to pass to the callback function (Currently not in use)
        """
        current_event_id = str(uuid.uuid4())
        kwargs['thread_id'] = current_event_id

        self.event_started.emit((current_event_id, task))

        worker = Worker(fn, *args, **kwargs)

        worker.signals.progress.connect(self.func_finished.emit)
        worker.signals.result.connect(fn_out if fn_out is not None else self.__event_result)
        worker.signals.finished.connect(self.__event_complete)
        worker.signals.error.connect(self.__event_error)

        self.event_tracker[current_event_id] = worker
        self.threadpool.start(worker) 

        self.__update_status()

    def __update_status(self):
        thread_count = self.threadpool.maxThreadCount()
        active_thread_count = self.threadpool.activeThreadCount()
        print(f"Limit of threads available {thread_count}")
        print(f"Current amount of active threads {active_thread_count}")

    def force_garbage_collection(self):
        print("collecting leftover garbage!")
        gc.collect()
        
        try:
            ctypes.windll.psapi.EmptyWorkingSet(ctypes.windll.kernel32.GetCurrentProcess())
        except Exception:
            pass




    