import os
import sys
from pdf_processing import process_pdf
from txt_processing import process_txt
from jpeg_processing import process_jpeg
from html_processing import process_html
from encoding_handling import read_file_with_encoding
from tokenization_normalization import tokenize_and_normalize
from flair_ner_extraction import load_flair_ner_model, extract_named_entities_flair
from text_summarization import summarize_text
from parallel_processing import process_file_parallel

def save_to_processed_data(data, filename):
    if not os.path.exists("processed_data"):
        os.makedirs("processed_data")

    with open(f"processed_data/{filename}", "w") as f:
        for item in data:
            f.write("%s\n" % item)

def main():
    file = input("Enter the file path: ")
    delimiters = input("Enter the delimiters (separated by '|'): ")

    if not os.path.isfile(file):
        print("File not found!")
        sys.exit()

    filename, file_extension = os.path.splitext(file)
    output_filename = os.path.basename(filename) + "_processed.txt"

    file_content = read_file_with_encoding(file)
    
    if file_extension.lower() == ".pdf":
        extracted_text = process_pdf(file, delimiters)
    elif file_extension.lower() == ".txt":
        extracted_text = process_txt(file, delimiters)
    elif file_extension.lower() == ".jpeg" or file_extension.lower() == ".jpg":
        extracted_text = process_jpeg(file, delimiters)
    elif file_extension.lower() == ".html":
        extracted_text = process_html(file, delimiters)
    else:
        print("Unsupported file type!")
        sys.exit()

    tokenized_text = tokenize_and_normalize(extracted_text)

    # Load Flair NER model and extract named entities
    flair_model = load_flair_ner_model()
    named_entities = extract_named_entities_flair(extracted_text, flair_model)

    summarized_text = summarize_text(extracted_text)

    save_to_processed_data(tokenized_text, output_filename)
    print(f"Processed data saved to: processed_data/{output_filename}")

if __name__ == "__main__":
    main()
