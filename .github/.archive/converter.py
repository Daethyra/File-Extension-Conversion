import os
import logging
import click
import mimetypes
from PIL import Image
import json
import csv
import odf.opendocument
import xml.etree.ElementTree as ET


logging.basicConfig(filename='file.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


class FileConverter:
    def __init__(self, input_path: str, output_path: str):
        """
        Initializes a new instance of the FileConverter class.

        Args:
            input_path (str): Path to the input file.
            output_path (str): Path to save the converted file.
        """
        self.input_path = input_path
        self.output_path = output_path

    def convert(self) -> None:
        """
        Converts a file to the desired format.

        Raises:
            NotImplementedError: If the method is not implemented in the derived class.
            ValueError: If the input file format is not supported.
        """
        raise NotImplementedError

    @staticmethod
    def supported_conversions() -> str:
        """
        Returns a string with the supported file formats and conversions.

        Returns:
            str: Supported file formats and conversions.
        """
        return "Supported file formats and conversions:\n" \
               "JSON: can be converted to CSV or JSON\n" \
               "CSV: can be converted to JSON or CSV (no conversion needed)\n" \
               "ODT: can be converted to plain text\n" \
               "XML: can be converted to JSON"


class ImageConverter(FileConverter):
    def convert(self) -> None:
        """
        Converts an image to the desired format.

        Raises:
            ValueError: If the input file format is not supported.
        """
        try:
            img = Image.open(self.input_path)
            img.save(self.output_path)
        except Exception as e:
            logging.exception(f"Failed to convert image. Input: {self.input_path}, Output: {self.output_path}. Error: {str(e)}")
            raise ValueError("Unsupported file format.")


class TextConverter(FileConverter):
    def convert(self) -> None:
        """
        Converts a text document to the desired format.

        Raises:
            ValueError: If the input file format is not supported or the conversion is not possible.
        """
        input_ext = os.path.splitext(self.input_path)[1].lower()
        output_ext = os.path.splitext(self.output_path)[1].lower()

        if input_ext == '.json' and output_ext == '.csv':
            with open(self.input_path, 'r') as f:
                data = json.load(f)
            with open(self.output_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data[0].keys())
                for row in data:
                    writer.writerow(row.values())
        elif input_ext == '.csv' and output_ext == '.json':
            with open(self.input_path, 'r') as f:
                reader = csv.DictReader(f)
                data = [row for row in reader]
            with open(self.output_path, 'w') as f:
                json.dump(data, f, indent=4)
        elif input_ext == '.odt' and output_ext == '.txt':
            doc = odf.opendocument.load(self.input_path)
            with open(self.output_path, 'w') as f:
                f.write(doc.text().replace('\n', ' '))
        elif input_ext == '.xml' and output_ext == '.json':
            tree = ET.parse(self.input_path)
            root = tree.getroot()
            data = []
            for child in root:
                data.append(child.attrib)
            with open(self.output_path, 'w') as f:
                json.dump(data, f, indent=4)
        else:
            raise ValueError(f"Unsupported file format or conversion. Input: {input_ext}, Output: {output_ext}. "
                             f"{FileConverter.supported_conversions()}")

        if not os.path.exists(self.output_path):
            raise ValueError(f"Conversion failed. Input: {self.input_path}, Output: {self.output_path}. "
                             f"{FileConverter.supported_conversions()}")


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def convert_file(input_path: str, output_path: str) -> None:
    """
    Converts a file to the desired format.

    Args:
        input_path (str): Path to the input file.
        output_path (str): Path to save the converted file.

    Raises:
        ValueError: If the input and output file formats are the same or the input file format is not supported.
    """
    input_ext = os.path.splitext(input_path)[1].lower()
    output_ext = os.path.splitext(output_path)[1].lower()

    if input_ext == output_ext:
        raise ValueError("Input and output file formats cannot be the same.")

    file_type, _ = mimetypes.guess_type(input_path)
    if file_type is None:
        raise ValueError("Unsupported file format.")

    if file_type.startswith('image'):
        converter = ImageConverter(input_path, output_path)
    elif file_type.startswith('text'):
        converter = TextConverter(input_path, output_path)
    else:
        raise ValueError("Unsupported file format.")

    converter.convert()


if __name__ == "__main__":
    convert_file()