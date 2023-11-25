import pytest
import os
import json
import csv
import xml.etree.ElementTree as ET
from odf.opendocument import load as load_odt
from ..src.text_converter import TextConverter, convert_text
from io import StringIO

# Helper Functions for Test Data Creation
def create_json_file(path, data):
    with open(path, 'w') as file:
        json.dump(data, file)

def create_csv_file(path, data):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data[0].keys())
        for row in data:
            writer.writerow(row.values())

def create_xml_file(path, data):
    root = ET.Element("root")
    for item in data:
        child = ET.SubElement(root, "child", attrib=item)
    tree = ET.ElementTree(root)
    tree.write(path)

def create_odt_file(path, text):
    doc = opendocument.Text()
    para = P(text)
    doc.text.addElement(para)
    doc.save(path)

# Test Cases for Successful Conversions
@pytest.fixture
def setup_files(tmp_path):
    # Create dummy files for each format
    json_path = tmp_path / "test.json"
    csv_path = tmp_path / "test.csv"
    xml_path = tmp_path / "test.xml"
    odt_path = tmp_path / "test.odt"

    # Dummy data
    data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
    create_json_file(json_path, data)
    create_csv_file(csv_path, data)
    create_xml_file(xml_path, [{"name": "John"}, {"name": "Jane"}])
    create_odt_file(odt_path, "Sample text")

    return json_path, csv_path, xml_path, odt_path

def test_convert_json_to_csv(setup_files, tmp_path):
    json_path, _, _, _ = setup_files
    output_path = tmp_path / "output.csv"
    convert_text(str(json_path), str(output_path))
    assert os.path.exists(output_path)

def test_convert_csv_to_json(setup_files, tmp_path):
    _, csv_path, _, _ = setup_files
    output_path = tmp_path / "output.json"
    convert_text(str(csv_path), str(output_path))
    assert os.path.exists(output_path)

def test_convert_odt_to_txt(setup_files, tmp_path):
    _, _, _, odt_path = setup_files
    output_path = tmp_path / "output.txt"
    convert_text(str(odt_path), str(output_path))
    assert os.path.exists(output_path)

def test_convert_xml_to_json(setup_files, tmp_path):
    _, _, xml_path, _ = setup_files
    output_path = tmp_path / "output.json"
    convert_text(str(xml_path), str(output_path))
    assert os.path.exists(output_path)

# Test Cases for Failure Cases
def test_unsupported_input_format(tmp_path):
    unsupported_path = tmp_path / "unsupported.format"
    output_path = tmp_path / "output.csv"
    with pytest.raises(ValueError):
        convert_text(str(unsupported_path), str(output_path))

def test_unsupported_output_format(setup_files, tmp_path):
    json_path, _, _, _ = setup_files
    output_path = tmp_path / "unsupported.format"
    with pytest.raises(ValueError):
        convert_text(str(json_path), str(output_path))

# Test Cases for Edge Cases
def test_nonexistent_input_file(tmp_path):
    nonexistent_path = tmp_path / "nonexistent.json"
    output_path = tmp_path / "output.csv"
    with pytest.raises(FileNotFoundError):
        convert_text(str(nonexistent_path), str(output_path))

def test_invalid_file_path():
    invalid_path = "/invalid/path/to/file.json"
    with pytest.raises(ValueError):
        convert_text(invalid_path, "output.csv")

# Utility Function Tests
def test_supported_conversions():
    expected_output = "Supported file formats and conversions:\n" \
                      "JSON: can be converted to CSV or JSON\n" \
                      "CSV: can be converted to JSON or CSV (no conversion needed)\n" \
                      "ODT: can be converted to plain text\n" \
                      "XML: can be converted to JSON"
    assert TextConverter.supported_conversions() == expected_output
