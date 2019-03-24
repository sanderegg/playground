import logging
from pathlib import Path

import pytest

import postfinance_converter

logger = logging.getLogger(__name__)

@pytest.fixture
def input(tmpdir) -> Path:
    input_text = r'''2019-03-23;"ACHAT/SERVICE
            DU 23.03.2019
            CARTE NO XXXX9607
            Weissenbühl Apotheke
            Bern
            ";;-18.10;2019-03-23;9252.34'''
    input_file = tmpdir / "input.csv"
    input_file.write_text(input_text, encoding='iso-8859-1')
    yield input_file

@pytest.fixture
def output(tmpdir) -> Path:
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
    output_text = r'''19-03-23;0;;ACHAT/SERVICE DU 23.03.2019 CARTE NO XXXX9607 Weissenbühl Apotheke Bern;;-18.10;Bill;
'''
    output_file = tmpdir / "output.csv"
    output_file.write_text(output_text, encoding='utf-8')
    yield output_file


def test_converter(input: Path, output: Path, tmpdir: Path):
    output_result_file = tmpdir / "resulting_output.csv"
    postfinance_converter.convert_file(input, output_result_file)
    assert output_result_file.exists()

    assert output.read_text(encoding='utf-8') == output_result_file.read_text(encoding='utf-8')
