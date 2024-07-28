# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Tasks"""

# imports: library
import enum
import logging
from typing import Any, Callable

# imports: project
from glossanea.cli import output
from glossanea.cli import user_input
from glossanea.tasks import t_1_new_words_common as new_words


class TaskResult(enum.Enum):
    """Enum of task result options"""

    NOT_IMPLEMENTED = enum.auto()

    DATA_VALIDATION_FAILED = enum.auto()

    BACK_TO_PREVIOUS_TASK = enum.auto()
    JUMP_TO_NEXT_TASK = enum.auto()
    EXIT_TASK = enum.auto()

    SUBTASK_SKIP_TO_NEXT = enum.auto()
    SUBTASK_CORRECT_ANSWER = enum.auto()
    SUBTASK_WRONG_ANSWER = enum.auto()
    SUBTASK_RETRY = enum.auto()

    FINISHED = enum.auto()


class InputType(enum.Enum):
    """Enum of input types"""
    COMMAND = enum.auto()
    ANSWER = enum.auto()


class Command(enum.Enum):
    """Commands with default help values"""
    EMPTY = 'EMPTY'
    HELP = 'help'
    EXIT = 'quit'

    WORDS = 'words'
    SOLUTION = 'solution'

    PREVIOUS = 'previous'
    NEXT = 'next'
    JUMP = 'jump'


COMMAND_TEXTS: dict[str, Command] = {
    # only one option per starting letter (except typo options)
    'exit': Command.EXIT,
    'help': Command.HELP,
    'jump': Command.JUMP,
    'next': Command.NEXT,
    'previous': Command.PREVIOUS,
    'quit': Command.EXIT,  # alias
    'solution': Command.SOLUTION,
    'solve': Command.SOLUTION,  # alias
    'words': Command.WORDS,
}

COMMAND_PREFIXES: list[str] = ['cmd ', '/']


def get_answer(prompt: str) -> tuple[InputType, str]:
    """Get user input - answer"""

    input_text: str = input(prompt)

    for command_prefix in COMMAND_PREFIXES:
        if input_text.startswith(command_prefix):
            return InputType.COMMAND, input_text.lstrip(command_prefix)

    return InputType.ANSWER, input_text


def help_cmd_in_task() -> None:
    """Help with commands in task"""

    collection: list[list[str]] = [
        [Command.WORDS.value, 'Display New Words section again.'],
        [Command.SOLUTION.value, 'Display the answer hint (use sparingly!)'],
        [Command.NEXT.value, 'Move on to the next part of the task.'],
        [Command.JUMP.value, 'Leave task and move on to the next one.'],
        [Command.PREVIOUS.value, 'Leave task and jump back to the previous one.'],
        [Command.EXIT.value, 'Leave task an exit to top program level.']
    ]

    output.empty_line()
    output.simple('Within the task, the following commands are available:')
    output.value_pair_list(collection)


def answer_cycle(prompt: str,
                 l_pr_question: Callable[[], None],
                 answers: list[str],
                 l_pr_answer: Callable[[], None],
                 unit_data: dict[str, Any],
                 ) -> TaskResult:
    """Answer cycle"""

    while True:
        output.empty_line()
        a_type, a_content = get_answer(prompt)

        match a_type:
            case InputType.ANSWER:
                task_result = process_answer(a_content, answers, l_pr_answer)
            case InputType.COMMAND:
                task_result = process_command(a_content, answers, unit_data, l_pr_question)
            case _:
                error_msg: str = f'Unknown answer type: {a_type}'
                logging.error(error_msg)
                output.error(error_msg)
                task_result = TaskResult.SUBTASK_RETRY

        match task_result:
            case TaskResult.SUBTASK_RETRY | TaskResult.SUBTASK_WRONG_ANSWER:
                continue
            case _:
                return task_result


def process_answer(input_text: str,
                   answers: list[str],
                   l_pr_answer: Callable[[], None],
                   ) -> TaskResult:
    """Process an answer"""

    if input_text not in answers:
        output.warning('Incorrect, try again.')
        return TaskResult.SUBTASK_WRONG_ANSWER

    output.simple('Correct!')
    output.empty_line()
    l_pr_answer()
    user_input.wait_for_enter()

    return TaskResult.SUBTASK_CORRECT_ANSWER


# pylint: disable=too-many-return-statements
def process_command(input_text: str,
                    answers: list[str],
                    unit_data: dict[str, Any],
                    l_pr_question: Callable[[], None],
                    ) -> TaskResult:
    """Process a command"""

    command: Command = Command.EMPTY
    if input_text in COMMAND_TEXTS:
        command = COMMAND_TEXTS[input_text]
    else:
        for key, value in COMMAND_TEXTS.items():
            try:
                if key.index(input_text) == 0:
                    command = value
            except ValueError:
                pass

    match command:
        case Command.WORDS:
            new_words.new_words(unit_data)
            output.empty_line()
            l_pr_question()
            return TaskResult.SUBTASK_RETRY
        case Command.SOLUTION:
            output.simple('HINT: ' + ' / '.join([f'"{answer}"' for answer in answers]))
            return TaskResult.SUBTASK_RETRY
        case Command.NEXT:
            return TaskResult.SUBTASK_SKIP_TO_NEXT
        case Command.JUMP:
            return TaskResult.JUMP_TO_NEXT_TASK
        case Command.PREVIOUS:
            return TaskResult.BACK_TO_PREVIOUS_TASK
        case Command.EXIT:
            return TaskResult.EXIT_TASK
        case Command.HELP:
            help_cmd_in_task()
            return TaskResult.SUBTASK_RETRY
        case _:
            output.warning(f'Invalid command: {input_text}')
            return TaskResult.SUBTASK_RETRY
