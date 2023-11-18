from pathlib import Path


def check_python_module(pyfile_path: Path):
    if not pyfile_path.is_file() or pyfile_path.suffix != '.py':
        return False
    file_name = pyfile_path.name
    #  The first letter of the file name must be upper
    if not file_name[0].isupper():
        return False
    return True
