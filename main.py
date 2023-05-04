import os
import sys
import shutil
import pypandoc
import img2pdf
from pdf2image.pdf2image import convert_from_path
import fitz
import requests
from urllib.parse import urlparse

pdflatex_path = r"C:\Users\dae\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"

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

def convert_to_pdf(input_file, input_extension, output_file):
    print(f"Processing {input_file}...")

    try:
        if input_extension in ['.pdf', '.PDF']:
            shutil.copy(input_file, output_file)
        elif input_extension.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
            with open(output_file, "wb") as pdf_file:
                pdf_bytes = img2pdf.convert(input_file)
                if pdf_bytes:
                    pdf_file.write(pdf_bytes)
                else:
                    raise ValueError("Empty output")
        else:
            output = pypandoc.convert_file(input_file, 'pdf', outputfile=output_file, extra_args=['--pdf-engine', pdflatex_path, '--quiet'])
    except Exception as e:
        print(f"Error converting {input_file} to PDF: {str(e)}")
        return

    print(f"Converted {input_file} to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    
    if is_url(input_path):
        url_filename = os.path.basename(urlparse(input_path).path)
        input_file = f"temp_{url_filename}"
        download_file(input_path, input_file)
    else:
        input_file = input_path

    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' does not exist.")
        sys.exit(1)

    input_filename, input_extension = os.path.splitext(input_file)
    output_file = f"{input_filename}_output.pdf"

    convert_to_pdf(input_file, input_extension, output_file)

    if is_url(input_path):
        os.remove(input_file)  # Clean up the temporary file
