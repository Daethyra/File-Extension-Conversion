import os
import sys
import PyPDF2
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
import requests

def process_pdf(file, keyword):
    with open(file, "rb") as f:
        pdf_reader = PyPDF2.PdfFileReader(f)
        num_pages = pdf_reader.numPages
        extracted_text = ""

        for page in range(num_pages):
            page_obj = pdf_reader.getPage(page)
            extracted_text += page_obj.extractText()

    return extracted_text.split(keyword)

def process_txt(file, keyword):
    with open(file, "r") as f:
        content = f.read()
    return content.split(keyword)

def process_jpeg(file, keyword):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    img = Image.open(file)
    text = pytesseract.image_to_string(img)
    return text.split(keyword)

def process_html(file, keyword):
    with open(file, "r") as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text()
    return text.split(keyword)

def save_to_processed_data(data, filename):
    if not os.path.exists("processed_data"):
        os.makedirs("processed_data")

    with open(f"processed_data/{filename}", "w") as f:
        for item in data:
            f.write("%s\n" % item)

if __name__ == "__main__":
    file = input("Enter the file path: ")
    keyword = input("Enter the keyword to parse: ")

    if not os.path.isfile(file):
        print("File not found!")
        sys.exit()

    filename, file_extension = os.path.splitext(file)
    output_filename = os.path.basename(filename) + "_processed.txt"

    if file_extension.lower() == ".pdf":
        extracted_data = process_pdf(file, keyword)
    elif file_extension.lower() == ".txt":
        extracted_data = process_txt(file, keyword)
    elif file_extension.lower() == ".jpeg" or file_extension.lower() == ".jpg":
        extracted_data = process_jpeg(file, keyword)
    elif file_extension.lower() == ".html":
        extracted_data = process_html(file, keyword)
    else:
        print("Unsupported file type!")
        sys.exit()

    save_to_processed_data(extracted_data, output_filename)
    print(f"Processed data saved to: processed_data/{output_filename}")
