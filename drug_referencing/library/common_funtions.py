"""
Module for common reusable functions
"""

import os
import csv
import json
import datetime
import re
import sys
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("app_logs")

logging.basicConfig(
        format="%(levelname)s | %(asctime)s | %(message)s",
        handlers=[
            RotatingFileHandler(
                './drug_referencing.log',
                backupCount=10),
            logging.StreamHandler(sys.stdout)
        ],
        level=logging.INFO)


def get_data_folder(file_typology):
    """
    Construct path to data folder

    Inputs:
    - file_typology (str) : subfolder to inspect

    Output:
    - (str) : absolute path to data directory
    """
    # If no typology given, analyse data folder
    if not file_typology:
        return os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))) + "/data"
    # Construct absolute path to data folder
    return (
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        + "/data/"
        + file_typology
    )


def get_files(path, extension):
    """
    Retrieve all files within a directory
    and subdirectories with a given extension

    Inputs:
    - path (str) : Path of the directory to inspect
    - extension (str) : File extension to consider

    Output:
    - file_path (str) : absolute path to files
    """
    # Loop over all files recursively
    for root_path, dirs, files in os.walk(path):  # noqa # pylint: disable=unused-variable
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root_path, file)
                yield file_path


def extract_csv(file):
    """
    Extract CSV data into a list of rows

    Inputs:
    - file (str) : file to open

    Output:
    - rows_list (list) : List of rows
    """
    rows_list = []  # List of rows

    with open(file, newline="", encoding="utf-8") as csv_file:
        # Read rows as a dictionary
        # First row considered as column names
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            if any(rowdata.strip() for rowdata in row):
                rows_list.append(row)

    return rows_list


def format_date(input_date, input_pattern=None):
    """
    Format most date formats into a standard one

    Inputs:
    - input_date (str) : date to format
    - input_pattern (list) : list of patterns to cast

    Output:
    - (str) : Date with format DD-MM-YYYY
    """
    list_patterns = []

    if input_pattern:
        list_patterns.append(input_pattern)
    else:
        list_patterns = [
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%m-%d-%Y",
            "%m/%d/%Y",
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%d %B %Y",
            "%Y %B %d",
        ]

    for pattern in list_patterns:
        try:
            return (
                datetime.datetime.strptime(input_date, pattern)
                .date()
                .strftime("%d-%m-%Y")
            )
        except:  # noqa # pylint: disable=bare-except
            pass

    return None


def rm_invalid_unicode(input_text):
    """
    Remove invalid unicode symbols

    Inputs:
    - input_text (str) : Text to cleanse

    Output:
    - (str) : Same text with all invalid unicode cleansed
    """
    return re.sub(r"(\\[a-zA-Z0-9]{3})", "", input_text)


def write_logs(log_text, severity="DEBUG"):
    """
    Function to write logs in file and stdout

    Inputs:
    - log_text (str) : text to log
    - severity (str) : log level
    """
    # If the log level wanted is not implemented
    # Log an error
    if severity not in [
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL"
    ]:
        logging.error("The logging level %s is not implemented", severity)
    if severity == "DEBUG":
        logging.debug(log_text)
    elif severity == "INFO":
        logging.info(log_text)
    elif severity == "WARNING":
        logging.warning(log_text)
    elif severity == "ERROR":
        logging.error(log_text)
    elif severity == "CRITICAL":
        logging.critical(log_text)


def export_to_json(data, file, data_encoding='utf-8'):
    """
    Function to write data in a JSON file

    Inputs:
    - data (str) : data to export
    - severity (str) : file to write
    - data_encoding (str) : text encoding
    """
    with open(file,
              "w",
              encoding=data_encoding) as output_file:
        json.dump(data,
                  output_file,
                  ensure_ascii=False,
                  indent=4)
