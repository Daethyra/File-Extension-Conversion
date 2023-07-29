import os
import img2pdf
from pdf2image.pdf2image import convert_from_path
from utils.path_utils import get_extension

class ImageConverter:
    """
    The ImageConverter class handles the processing of image files.
    """
    def __init__(self, input_file):
        self.input_file = input_file
        self.input_extension = get_extension(input_file)

    def to_pdf(self, output_file):
        """
        Convert image files to PDF.
        """
        if self.input_extension in ['.jpg', '.jpeg', '.png', '.bmp']:
            with open(output_file, "wb") as pdf_file:
                pdf_bytes = img2pdf.convert(self.input_file)
                if pdf_bytes:
                    pdf_file.write(pdf_bytes)
                else:
                    raise ValueError("Empty output")

    def to_jpeg(self, output_file):
        """
        Convert PDF files to JPEG.
        """
        if self.input_extension in ['.pdf', '.PDF']:
            pages = convert_from_path(self.input_file)
            for i, page in enumerate(pages):
                page.save(f"{output_file}_{i}.jpeg", "JPEG")
