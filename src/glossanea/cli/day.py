# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Day"""

# imports: library
from typing import Any, Callable

# imports: project
from glossanea.cli import output
from glossanea.structure.day import Day
from glossanea import tasks


def run(day: Day) -> None:
    """Run Day"""

    task_list: list[tuple[Callable, list[Any]]] = [
        (tasks.title, [day.title]),
        (tasks.new_words, [day.new_words]),
        (tasks.intro_text, [day.intro_text]),
        (tasks.sample_sentences, [day.sample_sentences,
                                  day.new_words_extension,
                                  day.new_words]),
        (tasks.definitions, [day.definitions,
                             day.new_words]),
        (tasks.matching, [day.matching,
                          day.new_words]),
        (tasks.other_new_words, [day.other_new_words]),
    ]

    task_index: int = 0
    while True:

        if task_index < 0:
            raise IndexError(f'Step index out of bounds: {task_index}')

        if task_index >= len(task_list):
            break

        task_function: Callable = task_list[task_index][0]
        task_arguments: list[Any] = task_list[task_index][1]
        task_result: tasks.TaskResult = task_function(*task_arguments)

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

            case tasks.TaskResult.NOT_IMPLEMENTED | tasks.TaskResult.FINISHED:
                task_index += 1
                continue

            case _:
                raise ValueError(f'Unhandled task result: {task_result}')
