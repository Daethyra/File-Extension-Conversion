import unittest
import logging
from pathlib import Path

# Relative imports of test modules
from .tests.test_image_converter import ImageConverterTests
from .tests.test_text_converter import TextConverterTests
from .tests.test_main import MainModuleTests

def setup_logging():
    """
    Sets up logging for the test results.
    """
    log_file_path = Path(__file__).parent / 'test_results.log'
    logging.basicConfig(filename=log_file_path, 
                        level=logging.INFO, 
                        format='%(asctime)s:%(levelname)s:%(message)s')

def create_test_suite():
    """
    Creates a unified test suite combining all tests from the three modules.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(ImageConverterTests))
    test_suite.addTest(unittest.makeSuite(TextConverterTests))
    test_suite.addTest(unittest.makeSuite(MainModuleTests))

    return test_suite

def configure_test_runner():
    """
    Configures a test runner that executes the test suite.
    """
    return unittest.TextTestRunner(verbosity=2)

def main():
    """
    Main function to run the test suite.
    """
    setup_logging()
    suite = create_test_suite()
    runner = configure_test_runner()
    test_result = runner.run(suite)

    if not test_result.wasSuccessful():
        logging.error(f"Number of failed tests: {len(test_result.failures)}")
        for test, traceback in test_result.failures:
            logging.error(f"{test.id()}: {traceback}")

if __name__ == '__main__':
    main()
