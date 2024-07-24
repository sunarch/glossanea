# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""CLI Unit"""

# imports: project
from glossanea.cli import output
from glossanea.structure import unit
from glossanea import tasks


def run(day: unit.Unit) -> None:
    """Run Unit"""

    task_list: list[str] = day.data_keys
    task_index: int = 0
    while True:

        if task_index < 0:
            raise IndexError(f'Step index out of bounds: {task_index}')

        if task_index >= len(task_list):
            break

        match task_list[task_index]:
            case unit.KEY_DATA_VERSION:
                task_result = tasks.TaskResult.HIDDEN

            case unit.KEY_TITLE:
                task_result = tasks.title(day.title)
            case unit.KEY_INTRO_TEXT:
                task_result = tasks.intro_text(day.intro_text)

            case unit.KEY_NEW_WORDS:
                task_result = tasks.new_words(day.new_words)
            case unit.KEY_NEW_WORDS_EXTENSION:
                task_result = tasks.TaskResult.HIDDEN
            case unit.KEY_SAMPLE_SENTENCES:
                task_result = tasks.sample_sentences(day.sample_sentences,
                                                     day.new_words_extension,
                                                     day.new_words)
            case unit.KEY_DEFINITIONS:
                task_result = tasks.definitions(day.definitions,
                                                day.new_words)
            case unit.KEY_MATCHING:
                task_result = tasks.matching(day.matching,
                                             day.new_words)
            case unit.KEY_OTHER_NEW_WORDS:
                task_result = tasks.other_new_words(day.other_new_words)
            case _:
                raise ValueError(f'Unrecognized task type: {task_list[task_index]}')

        match task_result:

            case tasks.TaskResult.BACK_TO_PREVIOUS_TASK:
                task_index = max(0, task_index - 1)
                if task_index == 0:
                    output.general_message('This is the first task: Starting from the beginning.')
                continue

            case tasks.TaskResult.JUMP_TO_NEXT_TASK:
                task_index += 1
                continue

            case tasks.TaskResult.EXIT_TASK:
                break

            case tasks.TaskResult.NOT_IMPLEMENTED | tasks.TaskResult.HIDDEN | tasks.TaskResult.FINISHED:
                task_index += 1
                continue

            case _:
                raise ValueError(f'Unhandled task result: {task_result}')
