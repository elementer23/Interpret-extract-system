import shutil
import py7zr
from py7zr import WriterFactory, Py7zIO
import zipfile
import tarfile
import os
from handler.file_handler import FileOsHandler
from utils.utilities import BasicUtils, FileType

BLOCK_SIZE = 1024

class __FlatWriter(Py7zIO):
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


class __FlatWriterFactory(WriterFactory):
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def create(self, filename):
        flat_name = os.path.basename(filename)
        if not flat_name:
            return None
        return __FlatWriter(os.path.join(self.output_dir, flat_name))
    

class Decompress():
    """Decompress class decompresses and passes regular files if needed.
    This class is used to extract files from an archive and place them in the given directory.
    Or simply copy the files to the given directory. Currently accepts 'zip', 'tar' and '7zip' for extraction.

    :type directory: string
    :param directory: the full path of the directory (required)
    :type file_s: list
    :param file_s: the list of files or compressed files (can be combined) (required)
    :type pwd: str = None
    :param pwd: parameter for password, currently not in use.
    """
    def __init__(self, directory: str, file_s: list, pwd: str = None):
        self.directory = directory
        self.file_s = file_s
        self.pwd = pwd
        
    def __decrypt(self):
        pass

    def extract(self):
        """Extracts the files from the compressed file or copies the given files to the given directory"""
        path = FileOsHandler().formulate_files_dir()
        FileOsHandler().create_dir(path[0], path[1])

        if not self.check_validity():
            return None
        
        extensions = [FileType.PDF, FileType.IMAGE, FileType.TEMPLATE_EXTENSION, FileType.TEXT_EXTENSION]

        try:
            library = self.check_validity() if isinstance(self.check_validity(), dict) else False
            if not library:
                return
            
            for key, value in library.items():
                match key:
                    case "zip":
                            self.zip_extract(value)
                    case "tar":
                            self.tar_extract(value)
                    case "7zip":
                            self.py7zip_extract(value)
                    case "non-compressed":
                        for i in range(len(value)):
                            if BasicUtils.categorize_file_type(value[i]) in extensions:
                                FileOsHandler().copy_files(value[i], self.directory)

        except Exception as ex:
            print("Exception:", ex)
            return None


    def check_validity(self):
        """Checks the validity of the given file(s) and categorizes them as 'zip', '7zip', 'tar' or 'non-compressed'"""
        library = {"zip": [], "7zip": [], "tar": [], "non-compressed": []}
        for file in self.file_s:
            if zipfile.is_zipfile(file):
                try:
                    with zipfile.ZipFile(file) as z:
                        if z.testzip() is None:
                            library['zip'].append(file)
                            continue
                except Exception: pass

            if py7zr.is_7zfile(file):
                try:
                    with py7zr.SevenZipFile(file) as s:
                        s.test()
                        library["7zip"].append(file)
                        continue
                except Exception: pass

            if tarfile.is_tarfile(file):
                if self.test_tar(file) is None:
                    library["tar"].append(file)
                    continue

            if BasicUtils.categorize_file_type(file) in [FileType.PDF, FileType.IMAGE, FileType.TEMPLATE_EXTENSION, FileType.TEXT_EXTENSION]:
                library["non-compressed"].append(file)
                continue

            print(f"File {file} is invalid.")
            return False
    
        return library if library else False
            
    def test_tar(self, file_path: str | bytes) -> str | None:
        """This function tests whether the given tar file is a tarfile and
        whether any file inside the compressed file is corrupted or not. 
        Mainly due to the tarfile not having a test function in their module.
        Will return None, if no corrupted files are found.
        Will otherwise return the name of the first corrupted file it could find.

        :type file_path: string | bytes
        :param file_path: the path of the file to check, can be a string or in the form of bytes.

        :return str | None:
        """
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
        

    def zip_extract(self, file_list: list):
        """Extracts the files in the zip archive, but does it flatly.
        (Basically ignoring directories in the archive, only going for the files).

        :type file_list: list
        :param file_list: list of files and checks whether a zip file is present, only extracting those.
        """
        for file in file_list:
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

    def py7zip_extract(self, file_list: list):
        """Extracts the files in the 7zip archive, but does it flatly.
        (Basically ignoring directories in the archive, only going for the files).

        :type file_list: list
        :param file_list: list of files and checks whether a 7zip file is present, only extracting those.
        """
        factory = __FlatWriterFactory(self.directory)

        for file in file_list:
            try:
                with py7zr.SevenZipFile(file, 'r') as s:
                    s.extract(factory=factory)

            except Exception: pass

    def tar_extract(self, file_list: list):
        """Extracts the files in the tar archive, but does it flatly.
        (Basically ignoring directories in the archive, only going for the files).

        :type file_list: list
        :param file_list: list of files and checks whether a tar file is present, only extracting those.
        """
        for file in file_list:
            try:
                with tarfile.open(file, 'r:*') as tar:
                    for member in tar.getmembers():
                        if member.isreg():
                            member.name = os.path.basename(member.name)
                            tar.extract(member, self.directory)

            except Exception: pass