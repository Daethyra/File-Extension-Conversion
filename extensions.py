import os
import pandas as pd
import pypandoc
import img2pdf
from pdf2image.pdf2image import convert_from_path
import fitz


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
