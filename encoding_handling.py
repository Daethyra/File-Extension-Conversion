import codecs
import chardet

def read_file_with_encoding(file_path, encoding=None):
    if encoding is None:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']

    with codecs.open(file_path, "r", encoding=encoding) as f:
        content = f.read()
    return content
