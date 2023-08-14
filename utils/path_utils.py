import os
from urllib.parse import urlparse

def is_url(input_path):
    """
    Check if the input path is a URL.
    """
    try:
        result = urlparse(input_path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def get_extension(input_file):
    """
    Get the extension of a file.
    """
    return os.path.splitext(input_file)[1].lower()
