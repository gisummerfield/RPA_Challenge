import logging
import os

"""
Config file for the project logger.
"""

log_file_path = os.path.join("output", 'Scraper.log')
logging.basicConfig(filename=log_file_path,
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger('log')
