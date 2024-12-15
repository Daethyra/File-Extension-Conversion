# Formaverter

## Description
Formaverter (Format Converter) is a Python tool that allows you to convert images between different formats using the Pillow library. It supports conversions between JPG, PNG, BMP, and WebP formats.

## Features
- Convert images between JPG, PNG, BMP, and WebP formats
- Batch conversion of multiple images
- Simple command-line interface
- Skips conversion if the input and output formats are the same

## Installation
To install Formaverter, you need Python 3.13 or later. You can install it using pip:

`pip install formaverter`

## Usage

### Using main.py directly as a CLI tool (Recommended)

If you've cloned the repository or downloaded the source code, you can use the `main.py` file directly:

1. Navigate to the directory containing `main.py`
2. Run the following command:

   `python main.py <input_path> <output_path> <output_format>`

   The arguments are the same as described above.

Example:

`python main.py ./input_image.jpg ./output_image.png png`

For batch conversion:

`python main.py ./input_directory ./output_directory png`

Note: When using `main.py` directly, make sure you have all the required dependencies installed in your Python environment.

### Using the Formaverter package

You can use the Formaverter package directly from the command line:

`python -m image_converter <input_path> <output_path> <output_format>`

- `<input_path>`: Path to the input image file or directory
- `<output_path>`: Path to save the converted image(s)
- `<output_format>`: Desired output format (jpg, png, bmp, or webp)

Example:

`python -m image_converter ./input_image.jpg ./output_image.png png`

For batch conversion, provide a directory as the input path:

`python -m image_converter ./input_directory ./output_directory png`

### Using Formaverter in your own projects

You can also import and use Formaverter in your own Python projects. Here's how:

1. First, make sure you've installed Formaverter:

   `pip install formaverter`

2. In your Python script, import the necessary functions:

   ```python
   from formaverter import convert_image, ImageConverter
   ```

To convert a single image using the straightforward `convert_image` function:

```python
convert_image('path/to/input/image.jpg', 'path/to/output/image.png', 'png')
```

To use the ImageConverter class directly:

```python
converter = ImageConverter('path/to/input/image.jpg', 'path/to/output/image.png', 'png')
converter.convert()
```

For batch conversion, you can use the collect_images function and loop through the results:

```python
from formaverter import collect_images, convert_image
```

```python
input_directory = 'path/to/input/directory'
output_directory = 'path/to/output/directory'
output_format = 'png'

image_files = collect_images(input_directory)

for input_path in image_files:
    filename = os.path.basename(input_path)
    name, _ = os.path.splitext(filename)
    output_path = os.path.join(output_directory, f"{name}.{output_format}")
    convert_image(input_path, output_path, output_format)
```

This allows you to integrate Formaverter's functionality into your own Python scripts or larger projects, giving you more control over the conversion process.

## Dependencies
- Pillow >= 11.0.0

## Development
To set up the development environment:

1. Clone the repository
2. Install PDM if you haven't already: `pip install pdm`
3. Install dependencies: `pdm install`
4. Run tests: ex. `python -m unittest .\tests\test_image_converter.py`

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the GNU Affero General Public License. See the LICENSE file for details.

## Author
Daethyra <109057945+Daethyra@users.noreply.github.com>

## Version
2.0.0
