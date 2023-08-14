# Image Converter

This is a simple command-line tool that allows users to convert image files between PNG and JPG formats. Users can either specify a particular image file for conversion or provide a directory to convert all the relevant images within it.

## Features:

* Convert a single PNG image to JPG.
* Convert a single JPG image to PNG.
* Convert all PNG images in a specified directory to JPG.
* Convert all JPG images in a specified directory to PNG.

## Prerequisites:

* Python 3.x
* Pillow (`pip install Pillow`)

## How to Use:

1. Clone this repository or download the source code.
2. Navigate to the directory containing the `main.py` script in your terminal or command prompt.
3. Run the program using the command: `python main.py`
4. Follow the on-screen instructions to select the conversion operation you'd like to perform.
5. Provide the path to the image file or directory as prompted.

## Error Handling:

The tool provides basic error handling to ensure the validity of the input paths. If any errors occur during the conversion, they are displayed on the terminal.
