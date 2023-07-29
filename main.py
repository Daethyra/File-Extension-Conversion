import os
import argparse
import shutil
import logging
from urllib.parse import urlparse
import pandas as pd
import pypandoc
import img2pdf
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import requests
import spacy
from utils.logging_utils import setup_logging
from utils.download_utils import download_file
from utils.path_utils import get_extension, is_url
from converters.async_text_converter import AsyncConverter
from converters.image_converter import ImageConverter
from processors.text_processor import TextProcessor
from models.text_classifier import TextClassifier
from pathlib import Path
import asyncio

# Load environment variables from .env file
load_dotenv()

model_path = os.getenv('MODEL_PATH')
default_path = os.getenv('DEFAULT_PATH')

class Converter:
    def __init__(self, input_file, model_path):
        self.input_file = input_file
        self.input_extension = get_extension(input_file)
        self.text_processor = TextProcessor()
        self.image_converter = ImageConverter(input_file)
        self.text_classifier = TextClassifier(model_path)
        self.async_converter = AsyncConverter(input_file, model_path=model_path)

    def to_pdf(self, output_file):
        if self.input_extension in ['.pdf', '.PDF']:
            shutil.copy(self.input_file, output_file)
        elif self.input_extension in ['.jpg', '.jpeg', '.png', '.bmp']:
            self.image_converter.to_pdf(output_file)
        else:
            pypandoc.convert_file(self.input_file, 'pdf', outputfile=output_file, extra_args=['--pdf-engine', 'pdflatex', '--quiet'])

    def to_jpeg(self, output_file):
        if self.input_extension in ['.pdf', '.PDF']:
            self.image_converter.to_jpeg(output_file)
        else:
            temp_pdf = f"{output_file}_temp.pdf"
            self.to_pdf(temp_pdf)
            self.image_converter.to_jpeg(temp_pdf)
            os.remove(temp_pdf)

    async def to_csv(self, output_file):
        if self.input_extension in ['.html', '.htm']:
            df = pd.read_html(self.input_file)[0]
            df.to_csv(output_file, index=False)
        elif self.input_extension in ['.pdf', '.docx', '.txt', '.json', '.csv', '.yaml']:
            text = await self.async_converter.extract_text()
            processed_text = self.text_processor.process_text(text)
            classified_text = self.text_classifier.classify_text(processed_text)
            df = pd.DataFrame({'text': [processed_text], 'classification': [classified_text]})
            df.to_csv(output_file, index=False)

def parse_args():
    parser = argparse.ArgumentParser(description='Process files.')
    parser.add_argument('input_file', help='Input file or URL.')
    parser.add_argument('--batch', nargs=2, metavar=('directory_path', 'output_format'),
                        help='Batch processing mode. Provide a directory and an output format.')
    return parser.parse_args()

output_format_methods = {
    '.pdf': 'to_pdf',
    '.jpeg': 'to_jpeg',
    '.csv': 'to_csv'
}

async def process_file(input_file: str, output_format: str):
    input_filename = os.path.splitext(input_file)[0]
    output_file = f"{input_filename}_output{output_format}"
    converter = get_converter(input_file)

    method_name = output_format_methods.get(output_format)
    if method_name:
        method = getattr(converter, method_name)
        if asyncio.iscoroutinefunction(method):
            await method(output_file)
        else:
            method(output_file)
    else:
        logging.error(f"Unsupported output format: {output_format}")
        return

    print(f"Converted {input_file} to {output_file}")

async def batch_process(directory_path: str, output_format: str):
    tasks = []
    directory_path = Path(directory_path)
    for file_path in directory_path.glob('**/*'):
        if file_path.is_file():
            task = asyncio.ensure_future(process_file(str(file_path), output_format))
            tasks.append(task)
    await asyncio.gather(*tasks)

def main():
    setup_logging()
    args = parse_args()

    model_path = "models/model_path_placeholder"
    global converter
    converter = Converter(args.input_file, model_path)

    if args.batch is not None:
        directory_path, output_format = args.batch
        asyncio.run(batch_process(directory_path, output_format))
    else:
        input_file = args.input_file

        if is_url(input_file):
            local_filename = Path(input_file).name
            try:
                download_file(input_file, local_filename)
                input_file = local_filename
            except Exception as e:
                logging.error(f"Error downloading the file: {str(e)}")
                sys.exit(1)

        input_file = Path(input_file).resolve()
        output_file = Path("Conversions") / f"{input_file.stem}_output{output_format}"
        asyncio.run(process_file(str(input_file), output_format))

if __name__ == "__main__":
    main()
