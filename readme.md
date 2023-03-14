# Multi-Filetype Data Parser

This Python application allows you to extract data based on a user-input keyword from various file types, including PDF, TXT, JPEG, and HTML. The extracted data is then saved in a subfolder named `processed_data`.

## Installation

### Prerequisites

- Python 3.x
- Tesseract OCR engine (for OCR on JPEG files)

### Dependencies

Install the required libraries using pip:

```bash
pip install -r requirements.txt


### Tesseract OCR engine
To use OCR for JPEG files, you need to have the Tesseract OCR engine installed on your system. You can find the installation instructions here: https://github.com/tesseract-ocr/tesseract

Make sure to update the tesseract_cmd variable in the process_jpeg function with the correct path to the Tesseract executable on your system.

## Usage
To run the script, execute the following command:
python multi_filetype_data_parser.py

You'll be prompted to enter the file path and the keyword to parse.

Supported File Types
PDF
TXT
JPEG (using OCR)
HTML