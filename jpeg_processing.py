import pytesseract
from PIL import Image

def process_jpeg(file, delimiters):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    img = Image.open(file)
    text = pytesseract.image_to_string(img)
    return text
