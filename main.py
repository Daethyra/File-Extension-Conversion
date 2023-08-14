from converters.image_converter import ImageConverter
import os

def main():
    print("Welcome to the image converter!")
    print("1. Convert all PNG images in the current working directory to JPG.")
    print("2. Convert all JPG images in the current working directory to PNG.")
    print("3. Convert a specific PNG to JPG.")
    print("4. Convert a specific JPG to PNG.")
    print("5. Convert all PNG images in a specified directory to JPG.")
    print("6. Convert all JPG images in a specified directory to PNG.")
    choice = input("Enter the number of your choice: ")

    try:
        if choice == "1":
            ImageConverter.convert_folder(".", "png_to_jpg")
        elif choice == "2":
            ImageConverter.convert_folder(".", "jpg_to_png")
        elif choice in ["3", "4"]:
            filename = input("Enter the full path of the image file to convert: ")
            if not filename or not os.path.isfile(filename):
                print("Invalid file path!")
                return
            if choice == "3":
                new_filename = os.path.splitext(filename)[0] + ".jpg"
                ImageConverter.png_to_jpg(filename, new_filename)
            else:
                new_filename = os.path.splitext(filename)[0] + ".png"
                ImageConverter.jpg_to_png(filename, new_filename)
        elif choice in ["5", "6"]:
            directory = input("Enter the full path of the directory: ")
            if not directory or not os.path.isdir(directory):
                print("Invalid directory path!")
                return
            if choice == "5":
                ImageConverter.convert_folder(directory, "png_to_jpg")
            else:
                ImageConverter.convert_folder(directory, "jpg_to_png")
        else:
            print("Invalid choice!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
