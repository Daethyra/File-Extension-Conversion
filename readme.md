
# File Extension Converter

## Convert image types, text files, and structured data betweenst their respective formats.

File Extension Converter is a Python program that allows you to convert files of various types to other formats. It supports the following conversions:

* PNG to JPG
* JPG to PNG
* JSON to CSV
* CSV to JSON
* ODT to plain text
* XML to JSON

## Prerequisites:

* Python 3.x
* Pillow
* Odfpy

## Installation:

Clone the repository to your local machine.

Install the required dependencies by running

`pip install -r requirements.txt`

## How to Use:

1. Clone this repository or download the source code.
2. Navigate to the directory containing the `main.py` script in your terminal or command prompt.
3. To use the program, run python main.py from the command line. This will display the main menu
4. Enter the number of the conversion you want to perform, followed by the full path to the file or directory you want to convert. The program will then convert the file(s) and save them in the same directory as the original file(s) with a new extension.

## Error Handling:

The tool provides basic error handling to ensure the validity of the input paths. If any errors occur during the conversion, they are displayed on the terminal.

## Reasoning and Intentions Behind the Project

This project aims to be a one-stop solution for various file conversion needs. With a focus on modularity, each conversion type is implemented as a pluggable component, allowing for easy extension and integration into other projects. The goal is to empower developers and users alike to build faster and smarter.

Future plans include adding automated webhook file pushing via Discord and potentially other services to make the tool even more versatile.

## Detailed Usage Guide

### Setup

1. Clone the repository.
2. Install the required Python packages.
3. Drop your files in to the 'data/' folder.

### Running the Program

Execute `main.py` to start the application:

```bash

python main.py

```

You will be presented with a menu listing the available file conversion options. Enter the corresponding number for the conversion you wish to perform.

You can either specify a single file or a directory for batch conversion. For a single file, provide the full path, including the file name and extension. For a directory, provide the full directory path.

Converted files will be saved in the same directory as the original files but with new extensions.

### Logging

Logs are saved in a file named `converter.log`. The log level is set to `INFO`.
