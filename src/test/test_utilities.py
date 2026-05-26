from utils.utilities import BasicUtils
from handler.file_handler import FileHandler, FileOsHandler
from vision.detection_handler import DetectionHandler
from vision.image_handler import ImageHandler
from vision.text_handler import TextHandler
from py7zr import pack_7zarchive, unpack_7zarchive
import shutil
from enumeration.file_type import FileType
import json

#Register the package to prevent register and threading problems for later on.
try:
    shutil.register_archive_format('7zip', pack_7zarchive, description='7zip archive')
    shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
except Exception as e:
    pass

def test_is_class_present_positive():
    class_handlers = (FileHandler(), ImageHandler(), DetectionHandler(), TextHandler())
    class_to_check = FileHandler

    assert BasicUtils.is_class_present(class_handlers, class_to_check) == True

def test_is_class_present_negative():
    class_handlers = (ImageHandler(), DetectionHandler(), TextHandler())
    class_to_check = FileHandler

    assert BasicUtils.is_class_present(class_handlers, class_to_check) == False

def test_is_number_int_float_positive():
    mock_loop = [1, 1.0, "10"]

    for num in mock_loop:
        assert BasicUtils.is_number_int_float(num) == True

def test_is_number_int_float_negative():
    mock_loop = [1, 1.0, "asdfasdf"]

    for num in mock_loop:
        assert BasicUtils.is_number_int_float(num) in [True, True, False]

def test_is_symbol_positive():
    mock_loop = ["!", "^&%", "@#%"]
   
    for sym in mock_loop:
        assert True if BasicUtils.is_symbol(sym) else False

def test_is_symbol_negative():
    mock_loop = ["asda!", "^&1asd", "@#%jan"]

    for sym in mock_loop:
        assert True if not BasicUtils.is_symbol(sym) else False 

def test_categorize():
    mock_loop = ["!", "1", 1.00, 11, "test"]

    for val in mock_loop:
        assert BasicUtils.categorize(val) in ["symbool", "nummer", "nummer", "nummer", "tekst"]

def test_is_zip_present_positive():
    pth = "C:/Users/697/Documents"
    dir_name = "test_container"
    full_path = f"{pth}/{dir_name}"
    zip_name = "test"
    zip_dir = f"{full_path}/{zip_name}"
    FileOsHandler().create_dir(pth, dir_name=dir_name)
    FileOsHandler().create_dir(full_path, dir_name=zip_name)
    shutil.make_archive(base_name=zip_dir, format="zip", root_dir=zip_dir)
    FileOsHandler().remove_dir(zip_dir)
    
    assert BasicUtils.is_zip_present([]) is None
    assert BasicUtils.is_zip_present([f"{zip_dir}.zip"]) == True

    FileOsHandler().remove_dir(full_path)

def test_is_zip_present_negative():
    pth = "C:/Users/697/Documents"
    dir_name = "test_container"
    full_path = f"{pth}/{dir_name}"
    zip_name = "test"
    zip_dir = f"{full_path}/{zip_name}"
    FileOsHandler().create_dir(pth, dir_name=dir_name)
    FileOsHandler().create_dir(full_path, dir_name=zip_name)
    shutil.make_archive(base_name=zip_dir, format="tar", root_dir=zip_dir)
    FileOsHandler().remove_dir(zip_dir)
    
    assert BasicUtils.is_zip_present([]) is None
    assert BasicUtils.is_zip_present([f"{zip_dir}.zip"]) == None

    FileOsHandler().remove_dir(full_path)

def test_compressed_file_present_positive():
    pth = "C:/Users/697/Documents"
    dir_name = "test_container"
    full_path = f"{pth}/{dir_name}"
    zip_name = "test"
    zip_dir = f"{full_path}/{zip_name}"
    FileOsHandler().create_dir(pth, dir_name=dir_name)
    FileOsHandler().create_dir(full_path, dir_name=zip_name)
    shutil.make_archive(base_name=zip_dir, format="zip", root_dir=zip_dir)
    shutil.make_archive(base_name=zip_dir, format="7zip", root_dir=zip_dir)
    shutil.make_archive(base_name=zip_dir, format="tar", root_dir=zip_dir)
    FileOsHandler().remove_dir(zip_dir)
    
    assert BasicUtils.is_zip_present([]) is None
    assert BasicUtils.is_zip_present([f"{zip_dir}.zip", f"{zip_dir}.7z", f"{zip_dir}.tar"]) in [True, True, True]

    FileOsHandler().remove_dir(full_path)

def test_compressed_file_present_negative():
    pth = "C:/Users/697/Documents"
    dir_name = "test_container"
    full_path = f"{pth}/{dir_name}"
    zip_name = "test"
    zip_dir = f"{full_path}/{zip_name}"
    FileOsHandler().create_dir(pth, dir_name=dir_name)
    FileOsHandler().create_dir(full_path, dir_name=zip_name)
    shutil.make_archive(base_name=zip_dir, format="zip", root_dir=zip_dir)
    shutil.make_archive(base_name=zip_dir, format="7zip", root_dir=zip_dir)
    FileOsHandler().remove_dir(zip_dir)
    
    assert BasicUtils.is_zip_present([]) is None
    assert BasicUtils.is_zip_present([f"{zip_dir}.zip", f"{zip_dir}.7z", f"{zip_dir}.tar"]) in [True, True, False]

    FileOsHandler().remove_dir(full_path)

def test_does_file_exist_positive():
    pth = "C:/Users/697/Documents"
    dir_name = "test_container"
    full_path = f"{pth}/{dir_name}"
    file_name = "copy.txt"
    FileOsHandler().create_dir(pth, dir_name=dir_name)
    with open(f"{full_path}/{file_name}", "w") as file:
        file.write("Hello")

    assert BasicUtils.does_file_exist(None, "") is None
    assert BasicUtils.does_file_exist(f"{full_path}/{file_name}", f"{full_path}/") == True

    FileOsHandler().remove_dir(full_path)

def test_does_file_exist_negative():
    pth = "C:/Users/697/Documents"
    dir_name = "test_container"
    full_path = f"{pth}/{dir_name}"
    file_name = "copy.txt"
    FileOsHandler().create_dir(pth, dir_name=dir_name)
    with open(f"{full_path}/{file_name}", "w") as file:
        file.write("Hello")

    assert BasicUtils.does_file_exist(None, "") is None
    assert BasicUtils.does_file_exist(f"{full_path}/fail.txt", f"{full_path}/") == False

    FileOsHandler().remove_dir(full_path)

def test_strip_all_except_letters():
    test_str = "test122!"
    test_arr = ["test122!", "pass122!"]
    assert BasicUtils.strip_all_except_letters("") == ""
    assert BasicUtils.strip_all_except_letters(test_str) == "test"
    assert BasicUtils.strip_all_except_letters(test_arr) == ["test", "pass"]

def test_strip_special_characters():
    test_str = "test122!"
    test_arr = ["test122!", "pass122!"]
    assert BasicUtils.strip_special_characters("") == ""
    assert BasicUtils.strip_special_characters(test_str) == "test122"
    assert BasicUtils.strip_special_characters(test_arr) == ["test122", "pass122"]

def test_first_upper_case():
    test_str = "test122!"
    assert BasicUtils.first_upper_case("") == ""
    assert BasicUtils.first_upper_case(test_str) == "Test"

def test_is_directory_empty_positive():
    pth = "C:/Users/697/Documents"
    dir_name = "test_container"
    full_path = f"{pth}/{dir_name}"
    FileOsHandler().create_dir(pth, dir_name=dir_name)

    assert BasicUtils.is_directory_empty(f"{full_path}") == True

    FileOsHandler().remove_dir(full_path)
    
def test_is_directory_empty_negative():
    pth = "C:/Users/697/Documents"
    dir_name = "test_container"
    full_path = f"{pth}/{dir_name}"
    file_name = "copy.txt"
    FileOsHandler().create_dir(pth, dir_name=dir_name)
    with open(f"{full_path}/{file_name}", "w") as file:
        file.write("Hello")

    assert BasicUtils.is_directory_empty(f"{full_path}") == False

    FileOsHandler().remove_dir(full_path)

def test_categorize_file_type():
    pth = "C:/Users/697/Documents"
    dir_name = "test_container"
    full_path = f"{pth}/{dir_name}"
    file_name = "copy.txt"
    file_array = [f"{full_path}/{file_name}", f"{full_path}/{file_name}"]
    FileOsHandler().create_dir(pth, dir_name=dir_name)
    with open(f"{full_path}/{file_name}", "w") as file:
        file.write("Hello")

    assert BasicUtils.categorize_file_type("") == FileType.UNKNOWN
    assert BasicUtils.categorize_file_type(f"{full_path}/{file_name}") == FileType.TEXT_EXTENSION
    assert BasicUtils.categorize_file_type(file_array) == [FileType.TEXT_EXTENSION, FileType.TEXT_EXTENSION]

    FileOsHandler().remove_dir(full_path)

def test_maintain_compatible_extensions():
    pth = "C:/Users/697/Documents"
    dir_name = "test_container"
    full_path = f"{pth}/{dir_name}"
    file_name = "copy.txt"
    json_file = "copy.json"
    _json = { "export": [{ "test": 1 }] }
    file_array = [f"{full_path}/{file_name}", f"{full_path}/{json_file}"]
    FileOsHandler().create_dir(pth, dir_name=dir_name)
    with open(f"{full_path}/{file_name}", "w") as file:
        file.write("Hello")

    with open(f"{full_path}/{json_file}", "w+") as new_file:
        json.dump(_json, new_file, indent=4)

    assert BasicUtils.maintain_compatible_extensions([], "") is None
    assert BasicUtils.maintain_compatible_extensions(file_array, FileType.TEXT_EXTENSION, FileType.TEMPLATE_EXTENSION) == file_array
    assert BasicUtils.maintain_compatible_extensions(file_array, FileType.TEMPLATE_EXTENSION) == [f"{full_path}/{json_file}"]
    assert BasicUtils.maintain_compatible_extensions(file_array, FileType.PDF) == None

    FileOsHandler().remove_dir(full_path)



    
