from PIL import Image
import os
import sys
import logging

logging.basicConfig(filename='file.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


class ImageConverter:
    @staticmethod
    def png_to_jpg(png_path, jpg_path, png_to_jpg=True):
        try:
            img = Image.open(png_path)
            rgb_img = img.convert('RGB')
            rgb_img.save(jpg_path, 'JPEG')
        except Exception as e:
            logging.exception("Exception occurred")

    @staticmethod
    def jpg_to_png(jpg_path, png_path, jpg_to_png=True):
        try:
            img = Image.open(jpg_path)
            img.save(png_path, 'PNG')
        except Exception as e:
            logging.exception("Exception occurred")

    @classmethod
    def convert_folder(cls, directory, conversion, png_to_jpg=True, jpg_to_png=True):
        for root, _, files in os.walk(directory):
            for file in files:
                if conversion == "png_to_jpg" and file.endswith(".png") and png_to_jpg:
                    jpg_path = os.path.join(root, os.path.splitext(file)[0] + '.jpg')
                    png_path = os.path.join(root, file)
                    cls.png_to_jpg(png_path, jpg_path)
                elif conversion == "jpg_to_png" and file.endswith(".jpg") and jpg_to_png:
                    png_path = os.path.join(root, os.path.splitext(file)[0] + '.png')
                    jpg_path = os.path.join(root, file)
                    cls.jpg_to_png(jpg_path, png_path)


class PDFConverter:
    @staticmethod
    def pdf_to_png(pdf_path, png_path):
        pass

    @staticmethod
    def pdf_to_jpg(pdf_path, jpg_path):
        pass


if __name__ == "__main__":
    # print(sys.argv)
    args = sys.argv
    if len(args) < 2:
        print("""
        Please enter a directory name
        Example: python file.py directory_name
        """)
    else:
        try:
            # print(args[1].lower().strip())
            directory_name = args[1].lower().strip()
            if os.path.exists(directory_name):
                print("Directory exists. Converting files...")
                ImageConverter.convert_folder(directory_name, "png_to_jpg")
                ImageConverter.convert_folder(directory_name, "jpg_to_png")
            else:
                print("Invalid directory name")
        except Exception as e:
            logging.exception("Exception occurred")
            print("Invalid directory name")