import os
import sys
import logging
from concurrent.futures import ThreadPoolExecutor
from main import input_file, output_format
from extensions import Converter

logging.basicConfig(filename='converter.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_file(file_path, output_format):
    try:
        input_file = os.path.abspath(file_path)
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
            raise ValueError(f"Unsupported output format: {output_format}")
        logging.info(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        logging.error(f"Error converting {input_file}: {str(e)}") # type: ignore


def batch_process(directory_path, output_format, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                executor.submit(process_file, file_path, output_format)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python utility.py <directory_path> <output_format>")
        sys.exit(1)

    directory_path = sys.argv[1]
    output_format = sys.argv[2].lower()

    if not output_format.startswith('.'):
        output_format = '.' + output_format

    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        sys.exit(1)

    batch_process(directory_path, output_format)
