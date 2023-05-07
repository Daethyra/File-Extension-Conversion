import os
import sys
import shutil
import requests
import pandas as pd
import pypandoc
import img2pdf
from pdf2image.pdf2image import convert_from_path
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(filename='converter.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Converter:
    def __init__(self, input_file):
        self.input_file = input_file
        self.input_extension = os.path.splitext(input_file)[1].lower()

    def to_pdf(self, output_file):
        if self.input_extension in ['.pdf', '.PDF']:
            shutil.copy(self.input_file, output_file)
        elif self.input_extension in ['.jpg', '.jpeg', '.png', '.bmp']:
            with open(output_file, "wb") as pdf_file:
                pdf_bytes = img2pdf.convert(self.input_file)
                if pdf_bytes:
                    pdf_file.write(pdf_bytes)
                else:
                    raise ValueError("Empty output")
        else:
            pypandoc.convert_file(self.input_file, 'pdf', outputfile=output_file, extra_args=['--pdf-engine', 'pdflatex', '--quiet'])

    def to_json(self, output_file):
        if self.input_extension in ['.html', '.htm']:
            df = pd.read_html(self.input_file)[0]
            df.to_json(output_file, orient='records')
        else:
            raise ValueError("Conversion to JSON is not supported for this file type")

    def to_csv(self, output_file):
        if self.input_extension in ['.html', '.htm']:
            df = pd.read_html(self.input_file)[0]
            df.to_csv(output_file, index=False)
        else:
            raise ValueError("Conversion to CSV is not supported for this file type")

    def to_yaml(self, output_file):
        if self.input_extension in ['.html', '.htm']:
            df = pd.read_html(self.input_file)[0]
            df.to_csv(output_file, index=False)
        else:
            raise ValueError("Conversion to YAML is not supported for this file type")
    
    def to_jpeg(self, output_file):
        if self.input_extension in ['.pdf', '.PDF']:
            pages = convert_from_path(self.input_file)
            for i, page in enumerate(pages):
                page.save(f"{output_file}_{i}.jpeg", "JPEG")
        else:
            try:
                print(f"Converting {self.input_file} to PDF before converting to JPEG.")
                temp_pdf = f"{output_file}_temp.pdf"
                self.to_pdf(temp_pdf)
                pages = convert_from_path(temp_pdf)
                for i, page in enumerate(pages):
                    page.save(f"{output_file}_{i}.jpeg", "JPEG")
                os.remove(temp_pdf)
            except Exception as e:
                raise ValueError(f"Conversion to JPEG is not supported for this file type: {str(e)}")

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

def process_file(input_file, output_format):
    input_filename = os.path.splitext(input_file)[0]
    output_file = f"{input_filename}_output{output_format}"
    converter = Converter(input_file)

    try:
        if output_format == '.pdf':
            converter.to_pdf(output_file)
        elif output_format == '.jpeg':
            converter.to_jpeg(output_file)
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

    except ValueError as e:
        print(f"Error: {str(e)}")


def batch_process(directory_path, output_format, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                executor.submit(process_file, file_path, output_format)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Interactive mode.")
        print("Enter 'quit' at any time to exit.")
        input_path = input("Enter the input file path or URL: ")
        if input_path.lower() == "quit":
            sys.exit(0)
        output_format = input("Enter the desired output format (e.g., .pdf, .json, .csv, .yaml, .jpeg): ").lower()
        if output_format.lower() == "quit":
            sys.exit(0)

        if not output_format.startswith('.'):
            output_format = '.' + output_format

        if is_url(input_path):
            local_filename = input_path.split("/")[-1]
            try:
                download_file(input_path, local_filename)
                input_file = local_filename
            except Exception as e:
                print(f"Error downloading the file: {str(e)}")
                sys.exit(1)
        else:
            input_file = input_path

        try:
            input_file = os.path.abspath(input_file)
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
            print(f"Successfully converted {input_file} to {output_file}")
        except Exception as e:
            print(f"Error converting {input_file}: {str(e)}")

    elif sys.argv[1].lower() == "--batch":
        if len(sys.argv) != 4:
            print("Usage: python main.py --batch <directory_path> <output_format>")
            sys.exit(1)

        directory_path = sys.argv[2]
        output_format = sys.argv[3].lower()

        if not output_format.startswith('.'):
            output_format = '.' + output_format

        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            print(f"Directory '{directory_path}' does not exist.")
            sys.exit(1)

        batch_process(directory_path, output_format)

    else:
        print("Invalid command.")
        print("Usage:")
        print("Interactive mode: python main.py")
        print("Batch mode: python main.py --batch <directory_path> <output_format>")
