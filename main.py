import sys
import os
import fitz
from pdf2image import convert_from_path, convert_from_bytes # type: ignore
from io import BytesIO
from PIL import Image
import html2text
import docx2txt
import base64

def get_content(input_file, input_extension):
    if input_extension in ['.pdf', '.PDF']:
        with open(input_file, 'rb') as f:
            content = f.read()
    else:
        content = None
    return content

def convert_to_pdf(input_file, input_extension, output_file):
    content = get_content(input_file, input_extension)
    
    if content is None:
        print("Unable to read file content.")
        sys.exit()

    if input_extension in ['.pdf', '.PDF']:
        with open(output_file, 'wb') as f:
            f.write(content)
    elif input_extension in ['.jpeg', '.jpg', '.JPEG', '.JPG']:
        images = convert_from_bytes(content)
        images[0].save(output_file, 'PDF', resolution=100.0, save_all=True, append_images=images[1:])
    elif input_extension in ['.docx', '.DOCX']:
        doc_text = docx2txt.process(input_file)
        with fitz.open() as pdf_doc: # type: ignore
            pdf_doc.new_page()
            page = pdf_doc[-1]
            page.insert_textbox(fitz.Rect(72, 72, 522, 720), doc_text)
            pdf_doc.save(output_file)
    else:
        print("Unsupported file type.")
        sys.exit()

def convert_to_jpeg(input_file, input_extension, output_folder):
    content = get_content(input_file, input_extension)
    
    if content is None:
        print("Unable to read file content.")
        sys.exit()

    if input_extension in ['.pdf', '.PDF']:
        images = convert_from_bytes(content)
        for i, image in enumerate(images):
            image.save(os.path.join(output_folder, f'page_{i+1}.jpg'), 'JPEG')
    else:
        print("Unsupported file type.")
        sys.exit()

def convert_to_html(input_file, input_extension, output_file):
    content = get_content(input_file, input_extension)
    
    if content is None:
        print("Unable to read file content.")
        sys.exit()

    if input_extension in ['.pdf', '.PDF']:
        images = convert_from_bytes(content)
        with open(output_file, 'w') as f:
            f.write('<!DOCTYPE html><html><head><title>PDF to HTML</title></head><body>')
            for i, image in enumerate(images):
                buffer = BytesIO()
                image.save(buffer, 'JPEG')
                img_base64 = base64.b64encode(buffer.getvalue()).decode() # 'base64 is not defined'
                f.write(f'<img src="data:image/jpeg;base64,{img_base64}" alt="Page {i+1}" width="100%" /><br><br>')
            f.write('</body></html>')
    elif input_extension in ['.docx', '.DOCX']:
        doc_text = docx2txt.process(input_file)
        html_text = html2text.html2text(doc_text)
        with open(output_file, 'w') as f:
            f.write(html_text)
    else:
        print("Unsupported file type.")
        sys.exit()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python main.py <input_file> <output_file> <conversion_type>")
        sys.exit()

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    conversion_type = sys.argv[3]

    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' does not exist.")
        sys.exit()

    input_extension = os.path.splitext(input_file)[1]

    if conversion_type == 'pdf':
        convert_to_pdf(input_file, input_extension, output_file)
    elif conversion_type == 'jpeg':
        output_folder = output_file
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        convert_to_jpeg(input_file, input_extension, output_folder)
    elif conversion_type == 'html':
        convert_to_html(input_file, input_extension, output_file)
    else:
        print(f"Unsupported conversion type: {conversion_type}")
        sys.exit()

