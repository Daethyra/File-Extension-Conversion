from converters.image_converter import ImageConverter
import os

def print_menu():
    print("Welcome to the image converter!")
    print("1. Convert PNG to JPG.")
    print("2. Convert JPG to PNG.")
    print("Enter 'q' to quit.")
    print("Note: You can enter either a specific file or a directory path when prompted.")

def main():
    print_menu()
    choice = input("Enter the number of your choice: ")

    while choice != 'q':
        try:
            path = input("Enter the full path of the image file or directory to convert: ")

            if not os.path.exists(path):
                print("Invalid path!")
                continue

            if choice == "1":
                if os.path.isfile(path):
                    new_filename = os.path.splitext(path)[0] + ".jpg"
                    ImageConverter.png_to_jpg(path, new_filename)
                    print(f"Converted {path} to {new_filename}.")
                elif os.path.isdir(path):
                    ImageConverter.convert_folder(path, "png_to_jpg")
                    print("PNG to JPG conversion in the specified directory is complete.")
            elif choice == "2":
                if os.path.isfile(path):
                    new_filename = os.path.splitext(path)[0] + ".png"
                    ImageConverter.jpg_to_png(path, new_filename)
                    print(f"Converted {path} to {new_filename}.")
                elif os.path.isdir(path):
                    ImageConverter.convert_folder(path, "jpg_to_png")
                    print("JPG to PNG conversion in the specified directory is complete.")
            else:
                print("Invalid choice!")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        print_menu()
        choice = input("Enter the number of your choice: ")

if __name__ == "__main__":
    main()
