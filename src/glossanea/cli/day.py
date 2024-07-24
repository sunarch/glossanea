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


class CLIDay:
    """CLI Day"""

    # General variables #
    _unit_finished: bool = False

    @classmethod
    def start(cls, day: Day) -> None:
        """Start / main loop"""

        task_list: list[tuple[Callable, list[Any]]] = [
            (tasks.title, [day.get_title()]),
            (tasks.new_words, [day.get_new_words()]),
            (tasks.intro_text, [day.get_intro_text()]),
            (tasks.sample_sentences, [day.get_sample_sentences(),
                                      day.get_new_words_extension(),
                                      day.get_new_words()]),
            (tasks.definitions, [day.get_definitions(),
                                 day.get_new_words()]),
            (tasks.matching, [day.get_matching(),
                              day.get_new_words()]),
            (tasks.other_new_words, [day.get_other_new_words()]),
        ]

        task_index: int = 0
        cls._unit_finished = False
        while not cls._unit_finished:

            if task_index < 0:
                raise IndexError(f'Step index out of bounds: {task_index}')

            if task_index >= len(task_list):
                cls._unit_finished = True
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
                    cls._unit_finished = True
                    break

                case tasks.TaskResult.NOT_IMPLEMENTED | tasks.TaskResult.FINISHED:
                    task_index += 1
                    continue

                case _:
                    raise ValueError(f'Unhandled task result: {task_result}')
