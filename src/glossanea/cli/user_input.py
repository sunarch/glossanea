# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""User Input"""

# imports: library
import enum


class InputType(enum.Enum):
    """Enum of input types"""
    COMMAND = enum.auto()
    ANSWER = enum.auto()


def get_command(prompt: str) -> tuple[str, list[str]]:
    """Get user input - top level command"""

    user_input: str = input(prompt)

    input_elements: list[str] = user_input.split()

    if len(input_elements) < 1:
        raise ValueError('No command given!')

    command: str = input_elements.pop(0)

    return command, input_elements


def get_answer(prompt: str) -> tuple[InputType, str]:
    """Get user input - answer"""

    user_input: str = input(prompt)

    command_test: list[str] = user_input.split('cmd ')
    if len(command_test) == 2 and command_test[0] == '':
        answer_type: InputType = InputType.COMMAND
        content: str = command_test[1]
    else:
        answer_type: InputType = InputType.ANSWER
        content: str = user_input

    return answer_type, content


def wait_for_enter() -> None:
    """Wait for the user to press ENTER"""

    _ = input('Press ENTER to continue...')
