import os
import sys
import shutil
import requests
from urllib.parse import urlparse
from extensions import Converter

def is_url(input_path):
    try:
        result = urlparse(input_path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def download_file(url, local_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_file> <output_format>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_format = sys.argv[2].lower()
    
    if not output_format.startswith('.'):
        output_format = '.' + output_format

    if is_url(input_path):
        url_filename = os.path.basename(urlparse(input_path).path)
        input_file = f"temp_{url_filename}"
        download_file(input_path, input_file)
    else:
        input_file = input_path

    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' does not exist.")
        sys.exit(1)

    input_filename = os.path.splitext(input_file)[0]
    output_file = f"{input_filename}_output{output_format}"
    
    converter = Converter(input_file)

    if output_format == '.pdf':
        converter.to_pdf(output_file)
    elif output_format == '.json':
        converter.to_json(output_file)
    elif output_format == '.csv':
        converter.to_csv(output_file)
    elif output_format == '.yaml':
        converter.to_yaml(output_file)
    else:
        print(f"Unsupported output format: {output_format}")
        sys.exit(1)

    print(f"Converted {input_file} to {output_file}")

    if is_url(input_path):
        os.remove(input_file)  # Clean up the temporary file
