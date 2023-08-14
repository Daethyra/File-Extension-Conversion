import logging
from datetime import datetime

def setup_logging():
    """
    Setup logging configuration.
    Each log file is named with the creation time for easy identification.
    """
    log_filename = datetime.now().strftime('converter_%Y%m%d_%H%M%S.log')
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
