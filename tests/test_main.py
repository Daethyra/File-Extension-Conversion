import pytest
from unittest.mock import patch, MagicMock
from ..main import *
import os

# Test Menu Display
def test_print_menu(capsys):
    main.print_menu()
    captured = capsys.readouterr()
    assert "File Converter" in captured.out

# File Conversion Tests
@patch('main.input', side_effect=['1', '/path/to/pngfile.png', 'n'])
@patch('main.convert_files')
def test_convert_single_file(mock_convert_files, mock_input):
    with patch('os.path.exists', return_value=True), \
         patch('os.path.isfile', return_value=True):
        main.main()
        mock_convert_files.assert_called_once()

@patch('main.input', side_effect=['1', '/path/to/directory', 'n'])
@patch('main.convert_files')
def test_convert_batch_files(mock_convert_files, mock_input):
    with patch('os.listdir', return_value=['file1.png', 'file2.png']), \
         patch('os.path.exists', return_value=True), \
         patch('os.path.isdir', return_value=True):
        main.main()
        assert mock_convert_files.call_count == 1

# User Input Handling
@patch('main.input', side_effect=['7', 'q'])
def test_invalid_choice(mock_input, capsys):
    main.main()
    captured = capsys.readouterr()
    assert "Invalid choice!" in captured.out

@patch('main.input', side_effect=['1', '/invalid/path.png', 'n'])
def test_invalid_file_path(mock_input, capsys):
    with patch('os.path.exists', return_value=False):
        main.main()
        captured = capsys.readouterr()
        assert "Invalid path!" in captured.out

# Error Handling Tests
def test_unsupported_conversion_type():
    with pytest.raises(ValueError):
        main.convert_extension("unsupported_type")

@patch('main.input', side_effect=['1', '/nonexistent/path.png', 'n'])
def test_nonexistent_path_handling(mock_input, capsys):
    with patch('os.path.exists', return_value=False):
        main.main()
        captured = capsys.readouterr()
        assert "Invalid path!" in captured.out
