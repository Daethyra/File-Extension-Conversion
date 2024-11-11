import os
from PIL import Image

class ImageConverter:
    SUPPORTED_CONVERSIONS = {
        'png_to_jpg': ('.png', '.jpg'),
        'jpg_to_png': ('.jpg', '.png'),
        'bmp_to_jpg': ('.bmp', '.jpg'),
        'bmp_to_png': ('.bmp', '.png'),
        'webp_to_jpg': ('.webp', '.jpg'),
        'webp_to_png': ('.webp', '.png'),
        'jpg_to_webp': ('.jpg', '.webp'),
        'png_to_webp': ('.png', '.webp')
    }

    def __init__(self, input_path: str, output_path: str, conversion_type: str):
        """
        Initializes a new instance of the ImageConverter class.

        Args:
            input_path (str): Path to the input image file.
            output_path (str): Path to save the converted image file.
            conversion_type (str): Type of conversion to perform (e.g., 'png_to_jpg', 'jpg_to_png')
        """
        self.input_path = input_path
        self.output_path = output_path
        self.conversion_type = conversion_type

    def convert(self) -> None:
        """
        Converts an image to the desired format.

        Raises:
            ValueError: If the input file format is not supported or the conversion is not possible.
        """
        if self.conversion_type not in self.SUPPORTED_CONVERSIONS:
            raise ValueError(f"Unsupported conversion type: {self.conversion_type}")

        expected_input_ext, expected_output_ext = self.SUPPORTED_CONVERSIONS[self.conversion_type]
        input_ext = os.path.splitext(self.input_path)[1].lower()
        output_ext = os.path.splitext(self.output_path)[1].lower()

        if input_ext not in self.SUPPORTED_CONVERSIONS:
            raise ValueError(f"Unsupported input file format: {input_ext}. "
                             f"Supported file formats and conversions: {self.supported_conversions()}")

        if output_ext != expected_output_ext:
            raise ValueError(f"Invalid output format for {self.conversion_type}: expected {expected_output_ext}, got {output_ext}")

        try:
            img = Image.open(self.input_path)
            
            # Handle alpha channel for PNG/WebP to JPG conversion
            if output_ext == '.jpg':
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.getchannel('A'))
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
            
            # Handle WebP specific options
            if output_ext == '.webp':
                img.save(self.output_path, 'WEBP', quality=90, method=6, lossless=False)
            else:
                # For other formats, use standard save with format inference
                img.save(self.output_path)
            
        except Exception as e:
            raise ValueError(f"Error converting image: {str(e)}")

    @staticmethod
    def supported_conversions() -> str:
        """
        Returns a string with the supported file formats and conversions.

        Returns:
            str: A string with the supported file formats and conversions.
        """
        return "Supported file formats and conversions:\n" \
               "JPEG: can be converted to PNG, WebP\n" \
               "PNG: can be converted to JPEG, WebP\n" \
               "BMP: can be converted to JPEG, PNG\n" \
               "WebP: can be converted to JPEG, PNG"


def convert_image(input_path: str, output_path: str, conversion_type: str) -> None:
    """
    Converts an image to the desired format.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the converted image file.
        conversion_type (str): Type of conversion to perform (e.g., 'png_to_jpg', 'jpg_to_png')

    Raises:
        ValueError: If the input file format is not supported or the conversion is not possible.
    """
    converter = ImageConverter(input_path, output_path, conversion_type)
    converter.convert()