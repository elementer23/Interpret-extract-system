from PyQt6.QtCore import QMutex, QMutexLocker

class FileLockManager:
    """
    A singular use class. Is used to lock files that are in use by the system.
    Makes sure that files can't be deleted, during execution. 

    DOES NOT PREVENT MANUAL DELETION, files can still be deleted from file explorer
    """
    def __init__(self):
        self.mutex = QMutex()
        self.locked_files = {}

    def lock_file(self, file_path):
        """
        This function locks the file that was given.
        """
        with QMutexLocker(self.mutex):
            if file_path not in self.locked_files:
                self.locked_files[file_path] = 0
            self.locked_files[file_path] += 1

    def unlock_file(self, file_path):
        """
        This function unlocks the file that was given.
        Won't unlock files that aren't present in the locked files.
        """
        with QMutexLocker(self.mutex):
            if file_path in self.locked_files:
                self.locked_files[file_path] -= 1
                if self.locked_files[file_path] <= 0:
                    del self.locked_files[file_path]

    def is_file_locked(self, file_path):
        """
        This function checks whether the file is locked or not.
        """
        with QMutexLocker(self.mutex):
            return file_path in self.locked_files
