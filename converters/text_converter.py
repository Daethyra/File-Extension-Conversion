import os
import json
import csv
import xml.etree.ElementTree as ET
from odf import opendocument

class TextConverter:
    SUPPORTED_CONVERSIONS = {
        '.json': {'.csv', '.json'},
        '.csv': {'.json', '.csv'},
        '.odt': {'.txt'},
        '.xml': {'.json'}
    }

    def __init__(self, input_path: str, output_path: str):
        """
        Initializes a new instance of the TextConverter class.

        Args:
            input_path (str): Path to the input text file.
            output_path (str): Path to save the converted text file.
        """
        self.input_path = input_path
        self.output_path = output_path

    def convert(self) -> None:
        """
        Converts a text document to the desired format.

        Raises:
            ValueError: If the input file format is not supported or the conversion is not possible.
        """
        input_ext = os.path.splitext(self.input_path)[1].lower()
        output_ext = os.path.splitext(self.output_path)[1].lower()

        if input_ext not in self.SUPPORTED_CONVERSIONS:
            raise ValueError(f"Unsupported input file format: {input_ext}. "
                             f"Supported file formats and conversions: {self.supported_conversions()}")

        if output_ext not in self.SUPPORTED_CONVERSIONS[input_ext]:
            raise ValueError(f"Unsupported output file format: {output_ext}. "
                             f"Supported file formats and conversions: {self.supported_conversions()}")

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
            doc = opendocument.load(self.input_path)
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

        if not os.path.exists(self.output_path):
            raise ValueError(f"Conversion failed. Input: {self.input_path}, Output: {self.output_path}. "
                             f"{self.supported_conversions()}")

    @staticmethod
    def supported_conversions() -> str:
        """
        Returns a string with the supported file formats and conversions.

        Returns:
            str: A string with the supported file formats and conversions.
        """
        return "Supported file formats and conversions:\n" \
               "JSON: can be converted to CSV or JSON\n" \
               "CSV: can be converted to JSON or CSV (no conversion needed)\n" \
               "ODT: can be converted to plain text\n" \
               "XML: can be converted to JSON"


def convert_file(input_path: str, output_path: str) -> None:
    """
    Converts a text document to the desired format.

    Args:
        input_path (str): Path to the input text file.
        output_path (str): Path to save the converted text file.

    Raises:
        ValueError: If the input file format is not supported or the conversion is not possible.
    """
    input_ext = os.path.splitext(input_path)[1].lower()
    output_ext = os.path.splitext(output_path)[1].lower()

    if input_ext == '.csv' and output_ext == '.csv':
        if input_path != output_path:
            os.replace(input_path, output_path)
    elif input_ext == '.json' and output_ext == '.json':
        if input_path != output_path:
            os.replace(input_path, output_path)
    else:
        converter = TextConverter(input_path, output_path)
        converter.convert()