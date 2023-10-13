import os
from PIL import Image

class ImageConverter:
    SUPPORTED_CONVERSIONS = {
        '.jpg': {'.jpg'},
        '.png': {'.png'},
        '.bmp': {'.jpg', '.png'}
    }

    def __init__(self, input_path: str, output_path: str):
        """
        Initializes a new instance of the ImageConverter class.

        Args:
            input_path (str): Path to the input image file.
            output_path (str): Path to save the converted image file.
        """
        self.input_path = input_path
        self.output_path = output_path

    def convert(self) -> None:
        """
        Converts an image to the desired format.

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

        if input_ext == '.jpg' and output_ext == '.jpg':
            if self.input_path != self.output_path:
                os.replace(self.input_path, self.output_path)
            else:
                raise ValueError(f"Input and output paths are the same: {self.input_path}. Please provide a different output path.")
        elif input_ext == '.png' and output_ext == '.png':
            if self.input_path != self.output_path:
                os.replace(self.input_path, self.output_path)
            else:
                raise ValueError(f"Input and output paths are the same: {self.input_path}. Please provide a different output path.")
        elif input_ext == '.bmp' and (output_ext == '.jpg' or output_ext == '.png'):
            self._bmp_to_image(output_ext)
        else:
            raise ValueError(f"Conversion failed. Input: {self.input_path}, Output: {self.output_path}. "
                             f"{self.supported_conversions()}")

    def _bmp_to_image(self, output_ext: str) -> None:
        img = Image.open(self.input_path)
        img.save(self.output_path, output_ext.upper())

    @staticmethod
    def supported_conversions() -> str:
        """
        Returns a string with the supported file formats and conversions.

        Returns:
            str: A string with the supported file formats and conversions.
        """
        return "Supported file formats and conversions:\n" \
               "JPEG: can be converted to JPEG (no conversion needed)\n" \
               "PNG: can be converted to PNG (no conversion needed)\n" \
               "BMP: can be converted to JPEG or PNG"


def convert_file(input_path: str, output_path: str) -> None:
    """
    Converts an image to the desired format.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the converted image file.

    Raises:
        ValueError: If the input file format is not supported or the conversion is not possible.
    """
    converter = ImageConverter(input_path, output_path)
    converter.convert()