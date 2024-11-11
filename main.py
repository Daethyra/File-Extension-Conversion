import os
from typing import List
from loguru import logger
from src.image_converter import convert_image
from src.text_converter import convert_text


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
    print("""\
╔══════════════════════════════════════════════════════════╗
║                    File Converter                         ║
╠══════════════════════════════════════════════════════════╣
║ 1. Convert PNG to JPG                                    ║
║ 2. Convert JPG to PNG                                    ║
║ 3. Convert JSON to CSV                                   ║
║ 4. Convert CSV to JSON                                   ║
║ 5. Convert ODT to plain text                            ║
║ 6. Convert XML to JSON                                   ║
║ 7. Convert PNG to WebP                                   ║
║ 8. Convert JPG to WebP                                   ║
║ 9. Convert WebP to PNG                                   ║
║ 10. Convert WebP to JPG                                  ║
║                                                          ║
║ Enter 'q' to quit.                                       ║
║ Note: You can enter either a specific file or a directory║
║ path when prompted.                                      ║
╚══════════════════════════════════════════════════════════╝
    """)


def convert_files(paths: List[str], conversion_type: str) -> None:
    """
    Converts multiple files of the same type in batch.

    Args:
        paths: A list of file paths to convert.
        conversion_type: The type of conversion to perform.
    """
    for path in paths:
        if os.path.isfile(path):
            new_filename = os.path.splitext(path)[0] + convert_extension(conversion_type)
            if any(conv in conversion_type for conv in ['png', 'jpg', 'webp']):
                convert_image(path, new_filename, conversion_type)
            else:
                convert_text(path, new_filename)
            logger.info(f"Converted {path} to {new_filename}.")
            print(f"Conversion of {path} to {new_filename} successful.")
        elif os.path.isdir(path):
            input_ext = get_input_extension(conversion_type)
            # Filter files by input extension before processing
            files_to_convert = [
                file for file in os.listdir(path) 
                if file.lower().endswith(input_ext.lower())
            ]
            
            if not files_to_convert:
                print(f"No {input_ext} files found in directory {path}")
                continue
                
            for file in files_to_convert:
                input_path = os.path.join(path, file)
                output_path = os.path.join(path, os.path.splitext(file)[0] + convert_extension(conversion_type))
                try:
                    if any(conv in conversion_type for conv in ['png', 'jpg', 'webp']):
                        convert_image(input_path, output_path, conversion_type)
                    else:
                        convert_text(input_path, output_path)
                    logger.info(f"Converted {input_path} to {output_path}.")
                    print(f"Conversion of {input_path} to {output_path} successful.")
                except Exception as e:
                    logger.error(f"Error converting {input_path}: {str(e)}")
                    print(f"Error converting {input_path}: {str(e)}")
                    continue
            logger.info(f"{conversion_type.upper()} conversion in the specified directory is complete.")
            print(f"{conversion_type.upper()} conversion in the specified directory is complete.")
        else:
            print(f"{path} is not a valid file or directory.")


def get_input_extension(conversion_type: str) -> str:
    """
    Returns the input file extension for the specified conversion type.

    Args:
        conversion_type: The type of conversion.

    Returns:
        str: The input file extension for the specified conversion type.
    """
    extensions = {
        'png_to_jpg': '.png',
        'jpg_to_png': '.jpg',
        'json_to_csv': '.json',
        'csv_to_json': '.csv',
        'odt_to_txt': '.odt',
        'xml_to_json': '.xml',
        'png_to_webp': '.png',
        'jpg_to_webp': '.jpg',
        'webp_to_png': '.webp',
        'webp_to_jpg': '.webp'
    }
    return extensions.get(conversion_type, '')


def convert_extension(conversion_type: str) -> str:
    """
    Returns the file extension for the specified conversion type.

    Args:
        conversion_type: The type of conversion.

    Returns:
        str: The file extension for the specified conversion type.
    """
    if conversion_type == "png_to_jpg":
        return ".jpg"
    elif conversion_type == "jpg_to_png":
        return ".png"
    elif conversion_type == "json_to_csv":
        return ".csv"
    elif conversion_type == "csv_to_json":
        return ".json"
    elif conversion_type == "odt_to_txt":
        return ".txt"
    elif conversion_type == "xml_to_json":
        return ".json"
    else:
        raise ValueError("Invalid conversion type!")


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

        except ValueError as e:
            logger.error(f"An error occurred: {str(e)}")
            print(f"An error occurred: {str(e)}")

        if choice != "q":
            print_menu()
            choice = input("Enter the number of your choice: ")


if __name__ == "__main__":
    main()