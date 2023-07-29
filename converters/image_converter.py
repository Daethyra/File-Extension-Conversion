import os
import img2pdf
from pdf2image.pdf2image import convert_from_path
from ..utils.path_utils import get_extension
import logging

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
            try:
                with open(output_file, "wb") as pdf_file:
                    logging.info(f"Starting conversion of {self.input_file} to PDF")
                    pdf_bytes = img2pdf.convert(self.input_file)
                    if pdf_bytes:
                        pdf_file.write(pdf_bytes)
                        logging.info(f"Successfully converted {self.input_file} to PDF")
                    else:
                        raise ValueError("Empty output")
            except Exception as e:
                logging.error(f"Error converting {self.input_file} to PDF: {str(e)}")

    def to_jpeg(self, output_file):
        """
        Convert PDF files to JPEG.
        """
        if self.input_extension in ['.pdf', '.PDF']:
            try:
                logging.info(f"Starting conversion of {self.input_file} to JPEG")
                pages = convert_from_path(self.input_file)
                for i, page in enumerate(pages):
                    jpeg_file = f"{os.path.splitext(output_file)[0]}_{i}.jpeg"
                    page.save(jpeg_file, "JPEG")
                logging.info(f"Successfully converted {self.input_file} to JPEG")
            except Exception as e:
                logging.error(f"Error converting {self.input_file} to JPEG: {str(e)}")
