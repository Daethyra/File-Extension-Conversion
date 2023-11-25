import pytest
import os
from PIL import Image
from ..src.image_converter import ImageConverter, convert_image

# Test data setup
@pytest.fixture
def setup_images(tmp_path):
    """
    Setup fixture to create dummy images in different formats.
    """
    bmp_path = tmp_path / "test.bmp"
    jpg_path = tmp_path / "test.jpg"
    png_path = tmp_path / "test.png"

    # Create a simple image in BMP, JPG, PNG formats
    img = Image.new("RGB", (100, 100), color="red")
    img.save(bmp_path, "BMP")
    img.save(jpg_path, "JPEG")
    img.save(png_path, "PNG")

    return bmp_path, jpg_path, png_path

# Test Cases for Successful Conversions
def test_convert_bmp_to_jpg(setup_images, tmp_path):
    bmp_path, _, _ = setup_images
    output_path = tmp_path / "output.jpg"
    convert_image(str(bmp_path), str(output_path))
    assert os.path.exists(output_path)

def test_convert_bmp_to_png(setup_images, tmp_path):
    bmp_path, _, _ = setup_images
    output_path = tmp_path / "output.png"
    convert_image(str(bmp_path), str(output_path))
    assert os.path.exists(output_path)

def test_copy_jpg(setup_images, tmp_path):
    _, jpg_path, _ = setup_images
    output_path = tmp_path / "copy.jpg"
    convert_image(str(jpg_path), str(output_path))
    assert os.path.exists(output_path)

def test_copy_png(setup_images, tmp_path):
    _, _, png_path = setup_images
    output_path = tmp_path / "copy.png"
    convert_image(str(png_path), str(output_path))
    assert os.path.exists(output_path)

# Test Cases for Failure Cases
def test_unsupported_input_format(setup_images, tmp_path):
    _, _, _ = setup_images
    output_path = tmp_path / "output.unknown"
    with pytest.raises(ValueError):
        convert_image("unsupported.format", str(output_path))

def test_unsupported_output_format(setup_images, tmp_path):
    bmp_path, _, _ = setup_images
    output_path = tmp_path / "output.unknown"
    with pytest.raises(ValueError):
        convert_image(str(bmp_path), str(output_path))

def test_same_input_output_path(setup_images):
    bmp_path, _, _ = setup_images
    with pytest.raises(ValueError):
        convert_image(str(bmp_path), str(bmp_path))

# Test Cases for Edge Cases
def test_nonexistent_input_file(tmp_path):
    nonexistent_path = tmp_path / "nonexistent.bmp"
    output_path = tmp_path / "output.jpg"
    with pytest.raises(FileNotFoundError):
        convert_image(str(nonexistent_path), str(output_path))

def test_invalid_file_path():
    invalid_path = "/invalid/path/to/file.bmp"
    with pytest.raises(ValueError):
        convert_image(invalid_path, "output.jpg")

# Utility Function Tests
def test_supported_conversions():
    expected_output = "Supported file formats and conversions:\n" \
                      "JPEG: can be converted to JPEG (no conversion needed)\n" \
                      "PNG: can be converted to PNG (no conversion needed)\n" \
                      "BMP: can be converted to JPEG or PNG"
    assert ImageConverter.supported_conversions() == expected_output
