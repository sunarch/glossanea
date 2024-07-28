# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Data schema"""

# imports: library
import enum
import logging
from typing import Any

# imports: dependencies
from jsonschema import ValidationError, SchemaError, Draft202012Validator


class ValidationResult(enum.Enum):
    """Data validation """

    OK = enum.auto()

    VALIDATION_FAILED = enum.auto()
    VERSION_INCORRECT = enum.auto()


def _validate_schema(data_validator: Draft202012Validator) -> bool:
    """Validate data schema"""

    try:
        data_validator.check_schema(data_validator.schema)
    except SchemaError:
        return False

    return True


def validate_unit_data(data_validator: Draft202012Validator,
                       data: dict | list,
                       ) -> ValidationResult:
    """Validate unit data"""

    assert _validate_schema(data_validator), "Failed to validate unit data schema"

    try:
        data_validator.validate(data)
    except ValidationError:
        logging.warning('Validation Error(s):')
        for error in data_validator.iter_errors(data):
            logging.warning(error.message)
        return ValidationResult.VALIDATION_FAILED

    return ValidationResult.OK


def subschema_prompt_list(minimum_items: int) -> dict[str, Any]:
    """Subschema for tasks with string list prompts"""

    return {
        "type": "array",
        "minItems": minimum_items,
        "items": {"type": "string"},
    }


def subschema_items_task() -> dict[str, Any]:
    """Subschema for multiple WR tasks"""

    return {
        "type": "object",
        "properties": {
            "task_number": {
                "type": "integer",
                "minimum": 1,
            },
            "prompt": {"type": "string"},
            "scoring": {"type": "string"},
            "items": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "question": {"type": "string"},
                        "answer": {"type": "string"},
                        "accept": {
                            "type": "array",
                            "minItems": 0,
                            "items": {"type": "string"},
                        },
                    },
                },
            },
        },
    }
