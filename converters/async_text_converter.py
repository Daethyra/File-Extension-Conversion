import os
import json
import yaml
import pandas as pd
from pdfminer.high_level import extract_text
from docx import Document
from ..utils.path_utils import get_extension
from ..models.text_classifier import TextClassifier
import logging

class AsyncConverter:
    """
    The AsyncConverter class handles the extraction of text from different file types,
    processes the extracted text (lemmatization and stop words removal), applies the language model
    for classification, and saves the processed and classified text to a CSV file.
    """
    def __init__(self, input_file, model_path):
        self.input_file = input_file
        self.input_extension = get_extension(input_file)
        self.classifier = TextClassifier(model_path)

    def extract_text(self):
        """
        Extract text from the input file. Currently supports .pdf, .docx, .txt, .json, .csv, and .yaml files.
        For other file types, additional conditions can be added.
        """
        try:
            if self.input_extension == '.pdf':
                text = extract_text(self.input_file)
            elif self.input_extension == '.docx':
                doc = Document(self.input_file)
                text = ' '.join([p.text for p in doc.paragraphs])
            elif self.input_extension == '.txt':
                with open(self.input_file, 'r') as file:
                    text = file.read()
            elif self.input_extension == '.json':
                with open(self.input_file, 'r') as file:
                    data = json.load(file)
                    text = json.dumps(data)  # Convert JSON to text
            elif self.input_extension == '.csv':
                df = pd.read_csv(self.input_file)
                text = df.to_string()  # Convert DataFrame to text
            elif self.input_extension == '.yaml':
                with open(self.input_file, 'r') as file:
                    data = yaml.safe_load(file)
                    text = yaml.dump(data)  # Convert YAML to text
            else:
                logging.error(f"Unsupported file type for text extraction: {self.input_extension}")
                text = None
            return text
        except Exception as e:
            logging.error(f"Error extracting text from {self.input_file}: {str(e)}")
            return None
        
    def save_to_csv(self, text, output_file='output.csv'):
        """
        Save the processed and classified text to a CSV file.
        """
        if text is not None:
            df = pd.DataFrame({
                'text': [text],
                'target': [self.classifier.classify_text(text)]
            })
            df.to_csv(output_file, index=False)
