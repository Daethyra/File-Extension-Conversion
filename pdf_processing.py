import PyPDF2

def process_pdf(file, delimiters):
    with open(file, "rb") as f:
        pdf_reader = PyPDF2.PdfFileReader(f)
        num_pages = pdf_reader.numPages
        extracted_text = ""

        for page in range(num_pages):
            page_obj = pdf_reader.getPage(page)
            extracted_text += page_obj.extractText()

    return extracted_text
