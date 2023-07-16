def txt_reader(file):
    with open(file, 'r', encoding='utf-8') as f:
        return str(f.readlines())


def csv_reader(file):
    return ''


FILE_READER_MAP = {
    '.txt': txt_reader,
    '.csv': csv_reader
}
