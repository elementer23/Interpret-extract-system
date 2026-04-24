import time
from gui.events.worker import Worker
from typing import Any
from PyQt6.QtCore import QThreadPool, QObject

class ThreadHandler(QObject):
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
        print(f"Something went wrong: Exception:", error)

    def _event_result(self, result):
        print(f"The actions of {result} have been executed.")

    def run_event(self, fn, fn_out: Any | None, *args, **kwargs):
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
        for n in range(0, 5):
            time.sleep(1)
            progress = n * 100 / 4
            progress_callback.emit((thread_id, progress))

    def _update_status(self):
        thread_count = self.threadpool.maxThreadCount()
        active_thread_count = self.threadpool.activeThreadCount()
        print(f"Limit of threads available {thread_count}")
        print(f"Current amount of active threads {active_thread_count}")




    