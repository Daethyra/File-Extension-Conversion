import os
from typing import List
from converters.image_converter import ImageConverter
from converters.text_converter import TextConverter, convert_file
from loguru import logger


def setup_logging() -> None:
    """
    Sets up logging for the application.
    """
    logger.add("converter.log", level="INFO", format="{time}:{level}: {message}")


setup_logging()


def print_menu() -> None:
    """
    Prints the main menu for the file converter program.
    """
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                    File Converter                         ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print("║ 1. Convert PNG to JPG.                                    ║")
    print("║ 2. Convert JPG to PNG.                                    ║")
    print("║ 3. Convert JSON to CSV.                                   ║")
    print("║ 4. Convert CSV to JSON.                                   ║")
    print("║ 5. Convert ODT to plain text.                             ║")
    print("║ 6. Convert XML to JSON.                                   ║")
    print("║                                                            ║")
    print("║ Enter 'q' to quit.                                        ║")
    print("║ Note: You can enter either a specific file or a directory  ║")
    print("║ path when prompted.                                       ║")
    print("║                                                            ║")
    print("║ Hint:                                                     ║")
    print("║ - To convert a single file, enter the full path to the     ║")
    print("║   file including the file name and extension.             ║")
    print("║ - To convert all files in a directory, enter the full path ║")
    print("║   to the directory.                                       ║")
    print("║ - Converted files will be saved in the same directory as  ║")
    print("║   the original file with a new extension.                 ║")
    print("╚══════════════════════════════════════════════════════════╝")


def convert_files(paths: List[str], conversion_type: str) -> None:
    """
    Converts multiple files of the same type in batch.

    Args:
        paths: A list of file paths to convert.
        conversion_type: The type of conversion to perform.
    """
    if conversion_type == "png_to_jpg":
        new_extension = ".jpg"
        converter_class = ImageConverter
    elif conversion_type == "jpg_to_png":
        new_extension = ".png"
        converter_class = ImageConverter
    elif conversion_type == "json_to_csv":
        new_extension = ".csv"
        converter_class = TextConverter
    elif conversion_type == "csv_to_json":
        new_extension = ".json"
        converter_class = TextConverter
    elif conversion_type == "odt_to_txt":
        new_extension = ".txt"
        converter_class = TextConverter
    elif conversion_type == "xml_to_json":
        new_extension = ".json"
        converter_class = TextConverter
    else:
        raise ValueError("Invalid conversion type!")

    for path in paths:
        if os.path.isfile(path):
            new_filename = os.path.splitext(path)[0] + new_extension
            converter = converter_class(path, new_filename)
            converter.convert()
            logger.info(f"Converted {path} to {new_filename}.")
            print(f"Conversion of {path} to {new_filename} successful.")
        elif os.path.isdir(path):
            for file in os.listdir(path):
                if file.lower().endswith(new_extension):
                    input_path = os.path.join(path, file)
                    output_path = os.path.join(path, os.path.splitext(file)[0] + new_extension)
                    converter = converter_class(input_path, output_path)
                    converter.convert()
            logger.info(f"{conversion_type.upper()} conversion in the specified directory is complete.")
            print(f"{conversion_type.upper()} conversion in the specified directory is complete.")
        else:
            print(f"{path} is not a valid file or directory.")


def main() -> None:
    """
    Runs the file converter program.
    """
    print_menu()
    choice = input("Enter the number of your choice: ")

    while choice != 'q':
        try:
            path = input("Enter the path of the file or directory to convert: ")

            if not os.path.exists(path):
                print("Invalid path!")
                continue

            # Convert relative path to absolute path
            path = os.path.abspath(path)

            if choice == "1":
                conversion_type = "png_to_jpg"
            elif choice == "2":
                conversion_type = "jpg_to_png"
            elif choice == "3":
                conversion_type = "json_to_csv"
            elif choice == "4":
                conversion_type = "csv_to_json"
            elif choice == "5":
                conversion_type = "odt_to_txt"
            elif choice == "6":
                conversion_type = "xml_to_json"
            else:
                print("Invalid choice!")
                continue

            if os.path.isfile(path):
                convert_files([path], conversion_type)
            elif os.path.isdir(path):
                paths = [os.path.join(path, file) for file in os.listdir(path)]
                convert_files(paths, conversion_type)
            else:
                print(f"{path} is not a valid file or directory.")

            # Ask user if they want to continue
            while True:
                response = input("Do you want to continue? (y/n): ").lower()
                if response in ["y", "yes"]:
                    break
                elif response in ["n", "no", "q", "quit", "exit", "\x1b", "\x03"]:
                    choice = "q"
                    break

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            print(f"An error occurred: {str(e)}")

        if choice != "q":
            print_menu()
            choice = input("Enter the number of your choice: ")


if __name__ == "__main__":
    main()