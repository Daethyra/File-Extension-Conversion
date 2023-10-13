import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from io import StringIO
from converters.image_converter import convert_image
from converters.text_converter import convert_text
from main import convert_files, convert_extension, main


class TestConverters(unittest.TestCase):
    """
    This class contains unit tests for the file conversion functions.
    """
    @classmethod
    def setUpClass(cls):
        """
        This method sets up the test environment before all test cases are run.
        """
        cls.test_dir = tempfile.mkdtemp()
        cls.test_file = os.path.join(cls.test_dir, "test_file.txt")
        with open(cls.test_file, "w") as f:
            f.write("This is a test file.")

    def test_convert_text(self):
        """
        This method tests that the convert_text function correctly converts a text file to a new format.
        """
        new_filename = os.path.splitext(self.test_file)[0] + ".csv"
        convert_text(self.test_file, new_filename)
        self.assertTrue(os.path.exists(new_filename))
        with open(new_filename, "r") as f:
            contents = f.read()
        self.assertEqual(contents, "This is a test file.")

    def test_convert_image(self):
        """
        This method tests that the convert_image function correctly converts an image file to a new format.
        """
        test_image = "test_image.png"
        test_image_path = os.path.join(self.test_dir, test_image)
        with open(test_image_path, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0fIDATx\x9c\xec\xfd\x07\x00\x02\x81\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x03\x00\x00\x00\xfc\xfd\x7f\x00\x00\x00\x00IEND\xaeB`\x82")
        new_filename = os.path.splitext(test_image_path)[0] + ".jpg"
        convert_image(test_image_path, new_filename, "png_to_jpg")
        self.assertTrue(os.path.exists(new_filename))

    @classmethod
    def tearDownClass(cls):
        """
        This method tears down the test environment after all test cases are run.
        """
        os.remove(cls.test_file)
        os.rmdir(cls.test_dir)


class TestMain(unittest.TestCase):
    """
    This class contains unit tests for the main file conversion functions.
    """
    @classmethod
    def setUpClass(cls):
        """
        This method sets up the test environment before all test cases are run.
        """
        cls.test_dir = tempfile.mkdtemp()
        cls.test_file = os.path.join(cls.test_dir, "test_file.txt")
        with open(cls.test_file, "w") as f:
            f.write("This is a test file.")

    def test_convert_files_single_file(self):
        """
        This method tests that the convert_files function correctly converts a single file.
        """
        new_filename = os.path.splitext(self.test_file)[0] + ".csv"
        convert_files([self.test_file], "json_to_csv")
        self.assertTrue(os.path.exists(new_filename))

    def test_convert_files_directory(self):
        """
        This method tests that the convert_files function correctly converts all files in a directory.
        """
        test_file2 = os.path.join(self.test_dir, "test_file2.txt")
        with open(test_file2, "w") as f:
            f.write("This is another test file.")
        new_filename1 = os.path.splitext(self.test_file)[0] + ".csv"
        new_filename2 = os.path.splitext(test_file2)[0] + ".csv"
        convert_files([self.test_dir], "json_to_csv")
        self.assertTrue(os.path.exists(new_filename1))
        self.assertTrue(os.path.exists(new_filename2))

    def test_convert_extension(self):
        """
        This method tests that the convert_extension function correctly returns the file extension for a given conversion type.
        """
        self.assertEqual(convert_extension("png_to_jpg"), ".jpg")
        self.assertEqual(convert_extension("jpg_to_png"), ".png")
        self.assertEqual(convert_extension("json_to_csv"), ".csv")
        self.assertEqual(convert_extension("csv_to_json"), ".json")
        self.assertEqual(convert_extension("odt_to_txt"), ".txt")
        self.assertEqual(convert_extension("xml_to_json"), ".json")

    @patch("builtins.input", side_effect=["1", self.test_file, "n"])
    @patch("converters.text_converter.logging")
    def test_main(self, mock_logging, mock_input):
        """
        This method tests that the main function correctly converts a single file.
        """
        with patch("sys.stdout", new=StringIO()) as fake_output:
            main()
            self.assertIn("Conversion of", fake_output.getvalue())
        mock_logging.info.assert_called_once_with("Conversion of %s to %s successful.", self.test_file, os.path.splitext(self.test_file)[0] + ".csv")

    @patch("builtins.input", side_effect=["1", self.test_file, "n"])
    @patch("converters.text_converter.logging")
    @patch("main.convert_files")
    def test_main_mocked(self, mock_convert_files, mock_logging, mock_input):
        """
        This method tests that the main function correctly calls the convert_files function.
        """
        main()
        mock_convert_files.assert_called_once_with([self.test_file], "json_to_csv")

    @patch("builtins.input", side_effect=["1", self.test_file, "n"])
    @patch("converters.text_converter.logging")
    @patch("main.convert_files")
    def test_main_mocked_exception(self, mock_convert_files, mock_logging, mock_input):
        """
        This method tests that the main function correctly handles an exception raised by the convert_files function.
        """
        mock_convert_files.side_effect = Exception("Test exception")
        with patch("sys.stdout", new=StringIO()) as fake_output:
            main()
            self.assertIn("Error:", fake_output.getvalue())

    def tearDown(self):
        """
        This method tears down the test environment after each test case is run.
        """
        os.remove(self.test_file)
        test_file2 = os.path.join(self.test_dir, "test_file2.txt")
        os.remove(test_file2)

    @classmethod
    def tearDownClass(cls):
        """
        This method tears down the test environment after all test cases are run.
        """
        os.rmdir(cls.test_dir)


if __name__ == "__main__":
    unittest.main()