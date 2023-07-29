import os
import argparse
from utils.logging_utils import setup_logging
from utils.download_utils import download_file, is_url
from utils.path_utils import get_extension
from converters.async_text_converter import AsyncConverter
from converters.image_converter import ImageConverter
from processors.text_processor import TextProcessor

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='Process text and image files.')
    parser.add_argument('input_file', help='Input file (text or image) or URL.')
    return parser.parse_args()

async def main(input_file):
    """
    Entry point for the script. This function orchestrates the process of text extraction, processing, classification, and saving.
    """
    setup_logging()
    
    # Load settings from .env
    load_dotenv()
    model_path = os.getenv('MODEL_PATH')

    # Check if the input_file is a URL. If so, download the file.
    if is_url(input_file):
        local_filename = input_file.split("/")[-1]
        try:
            download_file(input_file, local_filename)
            input_file = local_filename
        except Exception as e:
            logging.error(f"Error downloading the file: {str(e)}")
            sys.exit(1)

    # Get the file extension
    input_extension = get_extension(input_file)

    # Based on the file extension, determine whether to use the AsyncConverter or the ImageConverter
    if input_extension in ['.pdf', '.docx', '.txt', '.json', '.csv', '.yaml']:
        converter = AsyncConverter(input_file, model_path)
        text = await converter.extract_text()
        if text is not None:
            processor = TextProcessor()
            processed_text = processor.process_text(text)
            await converter.save_to_csv(processed_text)
    elif input_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.pdf']:
        converter = ImageConverter(input_file)
        # Convert images to PDF or PDFs to JPEG as needed
    else:
        logging.error(f"Unsupported file type for text extraction: {input_extension}")

if __name__ == "__main__":
    args = parse_args()
    await main(args.input_file)
