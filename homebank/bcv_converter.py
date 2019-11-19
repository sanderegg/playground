#!/bin/python

""" Converts a postfinance exported CSV file to HomeBank compatible file

    Usage python3 postfinance_converter.py --input path/to/inputs.csv --output path/to/put/the/output
:return: error code
"""

import argparse
import csv
import logging
import sys
from datetime import datetime
from enum import IntEnum
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ExitCode(IntEnum):
    SUCCESS = 0
    FAIL = 1

def convert_entry(input: List[str]) -> List[str]:
    # expected format
    # Transaction
    # date 	format must be DD-MM-YY
    # payment 	from 0=none to 10=FI fee
    # info 	a string
    # payee 	a payee name
    # memo 	a string
    # amount 	a number with a '.' or ',' as decimal separator, ex: -24.12 or 36,75
    # category 	a full category name (category, or category:subcategory)
    # tags 	tags separated by space
    # tag is mandatory since v4.5
    # file:///usr/share/doc/homebank-data/help/index.html

    date = datetime.strptime(input[0], '%d.%m.%Y')
    amount = 0.0
    if input[2]:
        amount = amount - float(input[2].replace("'", ""))
    if input[3]:
        amount = amount + float(input[3].replace("'", ""))
    output = [
        date.strftime('%y-%m-%d'), 
        "0",
        "",
        " ".join(input[1].split()),
        "",
        "{:.2f}".format(amount),
        "Bill",
        ""
    ]
    return output

def is_entry(row) -> bool:
    if not row:
        return False
    try:
        datetime.strptime(row[0], '%d-%m-%Y')
        return True
    except ValueError:
        return False


def convert_file(input_file: Path, output_file: Path):
    with Path(input_file).open('r', encoding='iso-8859-1') as input_fp,\
        Path(output_file).open('w', newline='', encoding='utf-8') as output_fp:

        soup = BeautifulSoup(input_fp, features="html.parser")
        csvwriter = csv.writer(output_fp, delimiter=';')
        for operation in soup.find_all('tbody'):
            row = [cell.string.strip() for cell in operation.find_all('td') if cell.string]
            converted_row = convert_entry(row)
            csvwriter.writerow(converted_row)
            

def main(args = None) -> int:
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--input", help="input file to convert", type=Path, required=True)
        parser.add_argument("--output", help="output file", type=Path, required=True)
        options = parser.parse_args(args)
        convert_file(options.input, options.output)
        return ExitCode.SUCCESS
    except: #pylint: disable=bare-except
        log.exception("Unexpected error:")
        return ExitCode.FAIL


if __name__ == "__main__":
    sys.exit(main())
