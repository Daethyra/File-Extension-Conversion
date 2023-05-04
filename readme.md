# Multi-Type File Parser (MFE-Parse)

A Python-based console application to convert various file formats, such as HTML, images, and documents, into PDF files.

## Features

- Accepts local files and URLs as input.
- Supports various file formats, including HTML, images (JPEG, PNG, BMP), and documents (DOCX, ODT, TXT).
- Automatically detects the input file's format and handles it accordingly.
- Improved error handling, providing informative error messages.
- Flexible: supports additional document formats via Pandoc conversion.

## Installation

1. Clone this repository or download the source code.
2. Ensure that you have Python 3.6+ installed on your system.
3. Install the required dependencies by running:

```bash
pip install -r requirements.txt

# Usage 
To use the script, navigate to the directory containing the source code and run the following command:
python main.py <input_file>

Replace <input_file> with the path to the file you want to convert, or the URL of the file.

The script will generate a PDF file in the same directory as the input file, with the same name and an _output suffix.

# Dependencies
pypandoc - A Python wrapper for Pandoc, the universal document converter.
img2pdf - A Python library to convert images to PDF without losing quality.
requests - A popular Python library for making HTTP requests.
beautifulsoup4 - A library for pulling data out of HTML and XML files.

License
This project is licensed under the  License. See the LICENSE file for details.
