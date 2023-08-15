"This class for image conversion may be executed individually or easily imported and integrated."
from PIL import Image
import os
import sys
import logging

logging.basicConfig(filename='file.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


class ImageConverter:
    @staticmethod
    def png_to_jpg(png_path: str, jpg_path: str) -> None:
        """
        Converts a PNG image to JPG format.

        Args:
            png_path (str): Path to the input PNG image.
            jpg_path (str): Path to save the converted JPG image.
        """
        try:
            img = Image.open(png_path)
            rgb_img = img.convert('RGB')
            rgb_img.save(jpg_path, 'JPEG')
        except Exception as e:
            logging.exception(f"Failed to convert PNG to JPG. PNG: {png_path}, JPG: {jpg_path}. Error: {str(e)}")

    @staticmethod
    def jpg_to_png(jpg_path: str, png_path: str) -> None:
        """
        Converts a JPG image to PNG format.

        Args:
            jpg_path (str): Path to the input JPG image.
            png_path (str): Path to save the converted PNG image.
        """
        try:
            img = Image.open(jpg_path)
            img.save(png_path, 'PNG')
        except Exception as e:
            logging.exception(f"Failed to convert JPG to PNG. JPG: {jpg_path}, PNG: {png_path}. Error: {str(e)}")

    @classmethod
    def convert_folder(cls, directory: str, conversion: str) -> None:
        """
        Converts images in a directory based on the specified conversion type (png_to_jpg or jpg_to_png).

        Args:
            directory (str): Directory containing the images to be converted.
            conversion (str): Conversion type ("png_to_jpg" or "jpg_to_png").
        """
        for root, _, files in os.walk(directory):
            for file in files:
                if conversion == "png_to_jpg" and file.endswith(".png"):
                    jpg_path = os.path.join(root, os.path.splitext(file)[0] + '.jpg')
                    png_path = os.path.join(root, file)
                    cls.png_to_jpg(png_path, jpg_path)
                elif conversion == "jpg_to_png" and file.endswith(".jpg"):
                    png_path = os.path.join(root, os.path.splitext(file)[0] + '.png')
                    jpg_path = os.path.join(root, file)
                    cls.jpg_to_png(jpg_path, png_path)


class PDFConverter:
    @staticmethod
    def pdf_to_png(pdf_path: str, png_path: str) -> None:
        """
        Converts a PDF to PNG format. (Method not implemented)

        Args:
            pdf_path (str): Path to the input PDF.
            png_path (str): Path to save the converted PNG.
        """
        pass

    @staticmethod
    def pdf_to_jpg(pdf_path: str, jpg_path: str) -> None:
        """
        Converts a PDF to JPG format. (Method not implemented)

        Args:
            pdf_path (str): Path to the input PDF.
            jpg_path (str): Path to save the converted JPG.
        """
        pass


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("""
        Please enter a directory name.
        Example: python file.py directory_name
        """)
    else:
        directory_name = args[1].lower().strip()
        if os.path.exists(directory_name):
            print("Directory exists. Converting files...")
            try:
                ImageConverter.convert_folder(directory_name, "png_to_jpg")
                ImageConverter.convert_folder(directory_name, "jpg_to_png")
            except Exception as e:
                logging.exception(f"Failed to convert images in directory {directory_name}. Error: {str(e)}")
                print(f"Error while converting images in {directory_name}. Check the log for details.")
        else:
            print("Invalid directory name")
