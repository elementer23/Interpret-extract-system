import shutil
import py7zr
import zipfile
import tarfile

BLOCK_SIZE = 1024

class Decompress():
    def __init__(self, directory: str, file_s: list, pwd: str = None):
        self.directory= directory
        self.file_s = file_s
        self.pwd = pwd


    def decrypt(self):
        pass

    def extract(self):
        if not self.check_content():
            return None
        
        try:

            for file in self.file_s:
                for opt in self.check_content():
                    match opt:
                        case "zip":
                            if zipfile.is_zipfile(file):
                                zipfile.ZipFile(file, "r").extractall(path=self.directory, pwd=self.pwd)
                        case "tar":
                            if tarfile.is_tarfile(file):
                                tarfile.open(file, "r").extractall(path=self.directory)
                        case "7zip":
                            if py7zr.is_7zfile(file):
                                py7zr.SevenZipFile(file, "r").extractall(path=self.directory)

        except Exception as ex:
            print("Exception:", ex)
            return None


    def is_format_typing(self):
        if not self.file_s:
            return
        
        for file in self.file_s:
            if zipfile.is_zipfile(file):
                return True
            elif tarfile.is_tarfile(file):
                return True
            elif py7zr.is_7zfile(file):
                return True
            else:
                return False
                

    def check_content(self):
        arr = []
        if self.is_format_typing():
            try:
                for file in self.file_s:
                    if zipfile.ZipFile(file).testzip() is None:
                        arr.append("zip")
                    elif py7zr.SevenZipFile(file).testzip() is None:
                        arr.append("7zip")
                    elif self.test_tar(file) is None:
                        arr.append("tar")
                    else:
                        return False
            except Exception as ex:
                print("Exception:", ex)
                return False
            
            if not arr:
                return False
            else:
                return arr
            
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