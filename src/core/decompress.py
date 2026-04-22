import shutil
import py7zr
from py7zr import WriterFactory, Py7zIO
import zipfile
import tarfile
import os
from handler.file_handler import FileOsHandler

BLOCK_SIZE = 1024

class _FlatWriter(Py7zIO):
    def __init__(self, target_path):
        self.file = open(target_path, 'wb')
        self._size = 0

    def write(self, data):
        self.file.write(data)
        self._size += len(data)

    def flush(self):
        return super().flush()
    
    def read(self, size = None):
        return super().read(size)
    
    def seek(self, offset, whence = 0):
        return super().seek(offset, whence)

    def size(self):
        return self._size
    
    def close(self):
        self.file.close()


class _FlatWriterFactory(WriterFactory):
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def create(self, filename):
        flat_name = os.path.basename(filename)
        if not flat_name:
            return None
        return _FlatWriter(os.path.join(self.output_dir, flat_name))
    

class Decompress():
    def __init__(self, directory: str, file_s: list, pwd: str = None):
        self.directory = directory
        self.file_s = file_s
        self.pwd = pwd

        self.extract()

    def decrypt(self):
        pass

    def extract(self):
        path = FileOsHandler().formulate_files_dir()
        FileOsHandler().create_dir(path[0], path[1])

        if not self.check_validity():
            return None
        
        try:
            for file in self.file_s:
                for opt in self.check_validity():
                    match opt:
                        case "zip":
                            if zipfile.is_zipfile(file):
                                self.zip_extract()
                        case "tar":
                            if tarfile.is_tarfile(file):
                                self.tar_extract()
                        case "7zip":
                            if py7zr.is_7zfile(file):
                                self.py7zip_extract()

        except Exception as ex:
            print("Exception:", ex)
            return None


    def check_validity(self):
        arr = []
        for file in self.file_s:
            if zipfile.is_zipfile(file):
                try:
                    with zipfile.ZipFile(file) as z:
                        if z.testzip() is None:
                            arr.append("zip")
                            continue
                except Exception: pass

            if py7zr.is_7zfile(file):
                try:
                    with py7zr.SevenZipFile(file) as s:
                        s.test()
                        arr.append("7zip")
                        continue
                except Exception: pass

            if tarfile.is_tarfile(file):
                if self.test_tar(file) is None:
                    arr.append("tar")
                    continue

            print(f"File {file} is invalid.")
            return False
        
        return arr if arr else False
            
    def test_tar(self, file_path: str | bytes) -> str | None:
        try:
            with tarfile.open(file_path, "r:*") as tar:
                for member in tar.getmembers():
                    if member.isfile():
                        try:
                            f = tar.extractfile(member)
                            if f is not None:
                                while f.read(BLOCK_SIZE * BLOCK_SIZE):
                                    pass

                        except (tarfile.TarError, OSError, EOFError):
                            return member.name
            return None
        except tarfile.ReadError:
            return "Archive Header Corrupt"
        

    def zip_extract(self):
        for file in self.file_s:
            try:
                with zipfile.ZipFile(file, 'r') as z:
                    for member in z.infolist():
                        if member.is_dir():
                            continue

                        file_name = os.path.basename(member.filename)
                        if not file_name:
                            continue

                        target_path = os.path.join(self.directory, file_name)

                        with z.open(member.filename) as source:

                            with open(target_path, 'wb') as f:
                                shutil.copyfileobj(source, f)

            except Exception: pass

    def py7zip_extract(self):
        factory = _FlatWriterFactory(self.directory)

        for file in self.file_s:
            try:
                with py7zr.SevenZipFile(file, 'r') as s:
                    s.extract(factory=factory)

            except Exception: pass

    def tar_extract(self):
        for file in self.file_s:
            try:
                with tarfile.open(file, 'r:*') as tar:
                    for member in tar.getmembers():
                        if member.isreg():
                            member.name = os.path.basename(member.name)
                            tar.extract(member, self.directory)

            except Exception: pass