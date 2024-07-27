# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""CLI Unit"""

# imports: library
from typing import Any, Callable

# imports: project
from glossanea import tasks
from glossanea.tasks import TaskResult
from glossanea.cli import output
from glossanea.structure.unit import Unit


def run(unit_obj: Unit) -> None:
    """Run Unit"""

    task_list: list[str] = unit_obj.task_names
    task_index: int = 0
    while True:

        if task_index < 0:
            raise IndexError(f'Step index out of bounds: {task_index}')

        if task_index >= len(task_list):
            break

        if not hasattr(tasks, task_list[task_index]):
            raise ValueError(f'Unrecognized task type: {task_list[task_index]}')

        if not hasattr(unit_obj, task_list[task_index]):
            raise ValueError(f'No data property for task type: {task_list[task_index]}')

        task_fn: Callable = getattr(tasks, task_list[task_index]).task
        task_data: Any = getattr(unit_obj, task_list[task_index])

        task_result = task_fn(task_data, unit_obj.new_words, unit_obj.new_words_extension)

        match task_result:

            case TaskResult.BACK_TO_PREVIOUS_TASK:
                task_index = max(0, task_index - 1)
                if task_index == 0:
                    output.general_message('This is the first task: Starting from the beginning.')
                continue

            case TaskResult.JUMP_TO_NEXT_TASK:
                task_index += 1
                continue

            case TaskResult.EXIT_TASK:
                break

            case TaskResult.NOT_IMPLEMENTED | TaskResult.FINISHED:
                task_index += 1
                continue

            case _:
                raise ValueError(f'Unhandled task result: {task_result}')
