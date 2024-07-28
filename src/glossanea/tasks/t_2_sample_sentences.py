# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: library
from typing import Any

# imports: dependencies
from jsonschema import Draft202012Validator

# imports: project
from glossanea.cli import output
from glossanea.tasks._common import TaskResult, answer_cycle, validate_unit_data_on_task
from glossanea.tasks import t_1_new_words_common as new_words

DATA_KEY: str = 'sample_sentences'
TITLE: str = 'sample sentences'.upper()

SCHEMA = {
    "type": "object",
    "required": ["sample_sentences", "new_words_extension"],
    "properties": {
        "sample_sentences": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "sentences": {
                    "type": "array",
                    "minItems": 1,
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
        "new_words_extension": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
}

DATA_VALIDATOR = Draft202012Validator(SCHEMA)


@validate_unit_data_on_task(data_validator=DATA_VALIDATOR)
def task(unit_data: dict[str, Any]) -> TaskResult:
    """Display 'sample sentences' task"""

    task_data: dict[str, Any] = unit_data[DATA_KEY]
    new_words_extension: list[str] = unit_data[new_words.DATA_KEY_NEW_WORDS_EXTENSION]

    output.section_title(TITLE)

    output.empty_line()
    output.simple(task_data['prompt'])

    output.empty_line()

    for sentence in task_data['sentences']:
        output.numbered_sentence(sentence['id'],
                                 sentence['beginning'] + output.BLANK + sentence['end'],
                                 output.Formatting.INDENTED)

    output.new_words_extension(new_words_extension)

    output.empty_line()

    for sentence in task_data['sentences']:

        prompt: str = f'{sentence["id"]}. '

        def l_pr_question() -> None:
            """l_pr_question"""
            return output.numbered_sentence(sentence['id'],
                                            sentence['beginning'] + output.BLANK + sentence['end'])

        answers: list[str] = [sentence['answer']]

        full_answer: str = sentence['answer']
        if len(sentence['beginning']) > 0:
            full_answer = f'{sentence["beginning"]} {full_answer}'
        if len(sentence['end']) > 0:
            if sentence['end'] not in ['.', '!', '?', '?!', '!?']:
                full_answer += ' '
            full_answer += sentence['end']

        def l_pr_answer() -> None:
            """l_pr_answer"""
            return output.simple(full_answer)

        # answer cycle

        new_words.new_words(unit_data)
        output.empty_line()
        l_pr_question()

        task_result: TaskResult = answer_cycle(prompt,
                                               l_pr_question,
                                               answers,
                                               l_pr_answer,
                                               unit_data)
        match task_result:
            case TaskResult.SUBTASK_CORRECT_ANSWER | TaskResult.SUBTASK_SKIP_TO_NEXT:
                continue
            case _:
                return task_result

    return TaskResult.FINISHED
