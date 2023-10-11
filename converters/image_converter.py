import os
from PIL import Image

class ImageConverter:
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
            ValueError: If the input file format is not supported.
        """
        try:
            img = Image.open(self.input_path)
            img.save(self.output_path)
        except Exception as e:
            logging.exception(f"Failed to convert image. Input: {self.input_path}, Output: {self.output_path}. Error: {str(e)}")
            raise ValueError(f"Failed to convert image. Input: {self.input_path}, Output: {self.output_path}. Error: {str(e)}. Please check that the input file format is supported and that the output file path is valid.")

    @staticmethod
    def supported_conversions() -> str:
        """
        Returns a string with the supported file formats and conversions.

        Returns:
            str: A string with the supported file formats and conversions.
        """
        return "Supported file formats and conversions:\n" \
               "JPEG: can be converted to PNG or JPEG (no conversion needed)\n" \
               "PNG: can be converted to JPEG or PNG (no conversion needed)\n" \
               "BMP: can be converted to JPEG or PNG"


def convert_file(input_path: str, output_path: str) -> None:
    """
    Converts an image to the desired format.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the converted image file.

    Raises:
        ValueError: If the input file format is not supported.
    """
    input_ext = os.path.splitext(input_path)[1].lower()
    output_ext = os.path.splitext(output_path)[1].lower()

    if input_ext == '.jpg' and output_ext == '.jpg':
        if input_path != output_path:
            os.replace(input_path, output_path)
        else:
            raise ValueError(f"Input and output paths are the same: {input_path}. Please provide a different output path.")
    elif input_ext == '.png' and output_ext == '.png':
        if input_path != output_path:
            os.replace(input_path, output_path)
        else:
            raise ValueError(f"Input and output paths are the same: {input_path}. Please provide a different output path.")
    elif input_ext == '.bmp' and (output_ext == '.jpg' or output_ext == '.png'):
        converter = ImageConverter(input_path, output_path)
        converter.convert()
    else:
        raise ValueError(f"Unsupported file format or conversion. Input: {input_ext}, Output: {output_ext}. {ImageConverter.supported_conversions()}")