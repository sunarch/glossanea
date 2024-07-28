# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""
import logging
# imports: library
from typing import Any

# imports: dependencies
from jsonschema import Draft202012Validator

# imports: project
from glossanea.cli import output
from glossanea.structure import schema
from glossanea.structure.schema import ValidationResult

DATA_KEY: str = 'new_words'
DATA_KEY_NEW_WORDS_EXTENSION: str = 'new_words_extension'

SCHEMA = {
    "type": "object",
    "required": ["new_words"],
    "properties": {
        "new_words": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "regular": {"type": "string"},
                    "phonetic": {"type": "string"},
                    "search": {"type": "string"},
                },
            },
        },
    },
}

DATA_VALIDATOR = Draft202012Validator(SCHEMA)


def new_words_full(unit_data: dict[str, Any]) -> None:
    """Display new words section"""

    match schema.validate_unit_data(DATA_VALIDATOR, unit_data):
        case ValidationResult.OK:
            pass
        case _:
            msg: str = f'Data validation failed: {DATA_KEY}'
            output.empty_line()
            output.warning(msg)
            logging.warning(msg)
            return

    word_data: list[dict[str, str]] = unit_data[DATA_KEY]

    regular: list[str] = [item['regular'] for item in word_data]
    phonetic: list[str] = [item['phonetic'] for item in word_data]

    output.empty_line()
    output.words_table(regular, phonetic)


def new_words(unit_data: dict[str, Any]) -> None:
    """Display new words section"""

    match schema.validate_unit_data(DATA_VALIDATOR, unit_data):
        case ValidationResult.OK:
            pass
        case _:
            msg: str = f'Data validation failed: {DATA_KEY}'
            output.empty_line()
            output.warning(msg)
            logging.warning(msg)
            return

    word_data: list[dict[str, str]] = unit_data[DATA_KEY]

    regular: list[str] = [item['regular'] for item in word_data]

    output.empty_line()
    output.words_table(regular)
