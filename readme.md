# PDF Conversion Tool

This Python script allows for easy conversion of PDF files to various formats including PDF, JPEG, and HTML.

## Usage

To use this script, provide the input file path, the output file path, and the desired conversion type as arguments when running the script.

- *python main.py <input_file> <output_file> <conversion_type>*


The following conversion types are supported:
- pdf: Converts the input file to a PDF.
- jpeg: Converts the input file to a series of JPEG images.
- html: Converts the input file to an HTML file.

## Dependencies

This script requires the following Python packages to be installed:
- PyMuPDF
- pdf2image
- html2text
- docx2txt
- pillow

## Example Usage

To convert a PDF file to a series of JPEG images:
- *python main.py input.pdf output_folder jpeg*

To convert a DOCX file to a PDF:
- *python main.py input.docx output.pdf pdf*
