# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""CLI Unit"""
import logging
# imports: library
from typing import Callable

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

        task_name = task_list[task_index]

        if not hasattr(tasks, task_name):
            raise ValueError(f'Unrecognized task type: {task_name}')

        task_fn: Callable = getattr(tasks, task_name).task

        task_result = task_fn(unit_obj.unit_data)

        match task_result:

            case TaskResult.BACK_TO_PREVIOUS_TASK:
                task_index = max(0, task_index - 1)
                continue

            case TaskResult.JUMP_TO_NEXT_TASK:
                task_index += 1
                continue

            case TaskResult.EXIT_TASK:
                break

            case TaskResult.DATA_VALIDATION_FAILED:
                msg: str = "Failed to validate task data: "
                msg += f'Week {unit_obj.week_number} / Day {unit_obj.unit_number}'
                msg += f' / {task_name}'
                output.empty_line()
                output.warning(msg)
                logging.warning(msg)
                task_index += 1
                continue

            case TaskResult.NOT_IMPLEMENTED | TaskResult.FINISHED:
                task_index += 1
                continue

            case _:
                raise ValueError(f'Unhandled task result: {task_result}')
