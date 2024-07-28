# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Data schema"""

# imports: library
import logging
from typing import Any

# imports: dependencies
from jsonschema import ValidationError, SchemaError, Draft202012Validator

# imports: project
from glossanea.structure.exceptions import DataError


def validate_unit_data(data: dict | list) -> None:
    """Validate unit data"""

    try:
        DATA_VALIDATOR.validate(data)
    except ValidationError as exc:
        logging.warning('Validation Error(s):')
        for error in DATA_VALIDATOR.iter_errors(data):
            logging.warning(error.message)
        raise DataError('Failed to validate unit data file by schema') from exc
    except SchemaError:
        assert False


def subschema_wr_task(question_key: str) -> dict[str, Any]:
    """Subschema for multiple WR tasks"""

    return {
        "type": "object",
        "properties": {
            "task_number": {"type": "integer"},
            "prompt": {"type": "string"},
            "scoring": {"type": "string"},
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        question_key: {"type": "string"},
                        "answer": {"type": "string"},
                        "accept": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                },
            },
        },
    }


SCHEMA = {
    "type": "object",
    "required": ["version", "title", "intro_text"],
    "properties": {
        "version": {
            "type": "integer",
            "minimum": 1,
        },
        "title": {
            "type": "string",
        },
        "new_words": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "regular": {"type": "string"},
                    "phonetic": {"type": "string"},
                    "search": {"type": "string"},
                },
            },
        },
        "new_words_extension": {
            "type": "array",
            "items": {"type": "string"},
        },
        "intro_text": {
            "type": "array",
            "items": {"type": "string"},
        },
        "sample_sentences": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "sentences": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "beginning": {"type": "string"},
                            "answer": {"type": "string"},
                            "end": {"type": "string"},
                        },
                    },
                },
            },
        },
        "definitions": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "definitions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "text": {"type": "string"},
                        },
                    },
                    "minItems": 5,
                    "maxItems": 5,
                },
                "words": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "text": {"type": "string"},
                        },
                    },
                    "minItems": 5,
                    "maxItems": 5,
                },
                "answers": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 2,
                        "maxItems": 2,
                    },
                    "minItems": 5,
                    "maxItems": 5,
                },
            },
        },
        "matching": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "prompt": {"type": "string"},
                "sentences": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "text": {"type": "string"},
                        },
                    },
                    "minItems": 5,
                    "maxItems": 5,
                },
                "words": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "text": {"type": "string"},
                        },
                    },
                    "minItems": 5,
                    "maxItems": 5,
                },
                "answers": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 2,
                        "maxItems": 2,
                    },
                    "minItems": 5,
                    "maxItems": 5,
                },
            },
        },
        "other_new_words": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
            },
        },
        "wr_before_the_test": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "words": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "after_text": {"type": "string"},
            },
        },
        "wr_definitions": subschema_wr_task('definition'),
        "wr_word_combinations": {
            "type": "object",
            "properties": {
                "task_number": {"type": "integer"},
                "prompt": {"type": "string"},
                "scoring": {"type": "string"},
                "extra_words": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "answer_before": {"type": "string"},
                            "accept_before": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "word": {"type": "string"},
                            "answer_after": {"type": "string"},
                            "accept_after": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                    },
                },
            },
        },
        "wr_skeletons": subschema_wr_task('word'),
        "wr_substitution": subschema_wr_task('sentence'),
        "wr_translation": subschema_wr_task('sentence'),
        "wr_sit_back_and_relax": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "label_like": {"type": "string"},
                "label_do_not_like": {"type": "string"},
                "label_people": {"type": "string"},
                "people": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "like": {"type": "string"},
                            "do_not_like": {"type": "string"},
                        },
                    },
                },
            },
        },
        "wr_word_formation": {
            "type": "object",
            "properties": {
                "groups": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
        },
        "wr_usage": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "word": {"type": "string"},
                            "sentences": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                    },
                },
            },
        },
        "wr_extra_cards": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
}

DATA_VALIDATOR = Draft202012Validator(SCHEMA)
