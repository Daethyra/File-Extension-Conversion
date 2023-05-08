╔══════════════════════════════════════════════════════════════════════════════════╗
║ ███████╗░█████╗░░█████╗░███╗░░░███╗░█████╗░                                    ║
║ ██╔════╝██╔══██╗██╔══██╗████╗░████║██╔══██╗                                    ║
║ █████╗░░███████║██║░░╚═╝██╔████╔██║██║░░██║    Multi-Extension Converter      ║
║ ██╔══╝░░██╔══██║██║░░██╗██║╚██╔╝██║██║░░██║                                    ║
║ ███████╗██║░░██║╚█████╔╝██║░╚═╝░██║╚█████╔╝                                    ║
║ ╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░░░░╚═╝░╚════╝░                                    ║
╚════════════════════════════════════════════════════════════════════════════════╝

## Welcome to the Multi-Extension Converter (MEC) - a Python-based console application that converts various file formats, such as HTML, images, and documents, into PDF, JPEG, JSON, CSV, or YAML files.

# 1. FEATURES
- Accepts local files and URLs as input.
- Supports various file formats, including HTML, images (JPEG, PNG, BMP), and documents (DOCX, ODT, TXT, PDF).
- Automatically detects the input file's format and handles it accordingly.
- Improved error handling, providing informative error messages.
- Flexible: supports additional document formats via Pandoc conversion.

# 2. Installation
To get started with MEC, you'll need to have Docker installed on your machine. Follow these steps to use the tool:

### Step A: Pull the Docker image
`docker pull daethyra/pypandoc:v1`

### Step B: Run the Docker container and mount your local working directory
`docker run -it --rm -v "$(pwd):/app/documents" daethyra/pypandoc:v1`

This command mounts your current working directory as a volume inside the container, allowing the program to access and convert your files.

Once the container is running, you'll immediately enter the interactive mode. Follow the on-screen instructions to convert your files.

### 3. Usage
Alternatively, to use the script itself, first navigate to the directory containing the source code, and run the following command:
`python main.py`

And follow the CLI instructions.

The script will create a "Conversions" folder if it does not already exist. Then it will export the converted file into the same folder with "_output.

### 4. Requirements
`pypandoc==1.11
requests
pandas
img2pdf
pdf2image`

### 5. License