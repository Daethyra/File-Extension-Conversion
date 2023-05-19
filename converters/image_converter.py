from PIL import Image
import os

class ImageConverter:
    @staticmethod
    def png_to_jpg(png_path, jpg_path):
        img = Image.open(png_path)
        rgb_img = img.convert('RGB')
        rgb_img.save(jpg_path, 'JPEG')

    @staticmethod
    def jpg_to_png(jpg_path, png_path):
        img = Image.open(jpg_path)
        img.save(png_path, 'PNG')

    @classmethod
    def convert_folder(cls, directory, conversion):
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
