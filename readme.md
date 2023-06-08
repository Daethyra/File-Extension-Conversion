# Multi-Extension-Converter (MEC)

A Python-based console application to convert various file formats, such as HTML, images, and documents, into PDF, JPEG, JSON, CSV, or YAML files.

## Features

- Accepts local files and URLs as input.
- Supports various file formats, including HTML, images (JPEG, PNG, BMP), and documents (DOCX, ODT, TXT, PDF).
- Automatically detects the input file's format and handles it accordingly.
- Improved error handling, providing informative error messages.
- Flexible: supports additional document formats via Pandoc conversion.

## Installation

1. Clone this repository or download the source code.
2. Ensure that you have Python 3.10+ installed on your system.
3. Install the required dependencies by running: ```pip install -r requirements.txt```

## Usage 
To use the script, first replace the {user} in `main.py` with your username, or otherwise point the program to the correct path.

Then, navigate to the directory containing the source code and run the following command:
```python main.py <input_file>```

Replace <input_file> with the path to the file you want to convert, or the URL of the file.

The script will generate a converted file in the same directory as the input file, with the same name and an _output suffix.

## Dependencies
pypandoc - A Python wrapper for Pandoc, the universal document converter.
img2pdf - A Python library to convert images to PDF without losing quality.
pdf2image - A library that converts PDFs to images.
Pillow - A powerful image processing library in Python.
requests - A popular Python library for making HTTP requests.
beautifulsoup4 - A library for pulling data out of HTML and XML files.

## License
This project is licensed under the GNU Affero General Public License. See the LICENSE file for details.
