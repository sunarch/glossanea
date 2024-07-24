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
    _task_index: int = 0
    _day: Day | None = None

    @classmethod
    def start(cls, day) -> None:
        """Start"""

        cls._day = day
        cls.mainloop()

    @classmethod
    def mainloop(cls) -> None:
        """Main loop"""

        task_list: list[tuple[Callable, list[Any]]] = [
            (tasks.title, [cls._day.get_title()]),
            (tasks.new_words, [cls._day.get_new_words()]),
            (tasks.intro_text, [cls._day.get_intro_text()]),
            (tasks.sample_sentences, [cls._day.get_sample_sentences(),
                                      cls._day.get_new_words_extension(),
                                      cls._day.get_new_words()]),
            (tasks.definitions, [cls._day.get_definitions(),
                                 cls._day.get_new_words()]),
            (tasks.matching, [cls._day.get_matching(),
                              cls._day.get_new_words()]),
            (tasks.other_new_words, [cls._day.get_other_new_words()]),
        ]

        cls._task_index = 0
        cls._unit_finished = False
        while not cls._unit_finished:

            if cls._task_index < 0:
                raise IndexError(f'Step index out of bounds: {cls._task_index}')

            if cls._task_index >= len(task_list):
                cls._unit_finished = True
                break

            task_function: Callable = task_list[cls._task_index][0]
            task_arguments: list[Any] = task_list[cls._task_index][1]
            task_result: tasks.TaskResult = task_function(*task_arguments)

            match task_result:

                case tasks.TaskResult.BACK_TO_PREVIOUS_TASK:
                    cls._task_index = max(0, cls._task_index - 1)
                    if cls._task_index == 0:
                        output.general_message('This is the first task: Starting from the beginning.')
                    continue

                case tasks.TaskResult.JUMP_TO_NEXT_TASK:
                    cls._task_index += 1
                    continue

                case tasks.TaskResult.EXIT_TASK:
                    cls._unit_finished = True
                    break

                case tasks.TaskResult.NOT_IMPLEMENTED | tasks.TaskResult.FINISHED:
                    cls._task_index += 1
                    continue

                case _:
                    raise ValueError(f'Unhandled task result: {task_result}')
