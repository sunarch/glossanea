# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Tasks"""

# imports: library
import enum
from typing import Callable

# imports: project
from glossanea.cli import output
from glossanea.cli import user_input
from glossanea.cli.user_input import InputType
from glossanea.tasks.t_1_new_words_common import new_words


class TaskResult(enum.Enum):
    """Enum of task result options"""

    NOT_IMPLEMENTED = enum.auto()
    HIDDEN = enum.auto()

    BACK_TO_PREVIOUS_TASK = enum.auto()
    JUMP_TO_NEXT_TASK = enum.auto()
    EXIT_TASK = enum.auto()

    SUBTASK_SKIP_TO_NEXT = enum.auto()
    SUBTASK_CORRECT_ANSWER = enum.auto()

    FINISHED = enum.auto()


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

    output.empty_line(1)
    output.simple('Within the task, the following commands are available:')
    output.value_pair_list(collection)


def answer_cycle(prompt: str,
                 l_pr_question: Callable[[], None],
                 answers: list[str],
                 l_pr_answer: Callable[[], None],
                 data_for_new_words: list[dict[str, str]],
                 ) -> TaskResult:
    """Answer cycle"""

    while True:
        output.empty_line(1)
        a_type, a_content = user_input.get_answer(prompt)

        match a_type:

            case InputType.ANSWER:

                if a_content not in answers:
                    output.warning('Incorrect, try again.')
                    continue

                output.empty_line(1)
                l_pr_answer()
                output.empty_line(1)
                output.simple('Correct!')

                return TaskResult.SUBTASK_CORRECT_ANSWER

            case InputType.COMMAND:

                command: Command = Command.EMPTY
                if a_content in COMMAND_TEXTS:
                    command = COMMAND_TEXTS[a_content]
                else:
                    for key, value in COMMAND_TEXTS.items():
                        try:
                            if key.index(a_content) == 0:
                                command = value
                        except ValueError:
                            pass

                match command:
                    case Command.WORDS:
                        new_words(data_for_new_words, False)
                        output.empty_line(1)
                        l_pr_question()
                    case Command.SOLUTION:
                        print('HINT: ' + ' / '.join([f'"{answer}"' for answer in answers]))
                        continue
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
                    case _:
                        output.warning(f'Invalid command: {a_content}')

            case _:
                raise ValueError(f'Unknown answer type: {a_type}')
