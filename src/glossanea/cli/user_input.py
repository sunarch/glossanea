# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""User Input"""


class CLIUserInput:
    """CLI User Input"""

    # constants
    TYPE_COMMAND: str = 'command'
    TYPE_ANSWER: str = 'answer'

    @classmethod
    def _get_new(cls, prompt: str) -> str:
        """Get user input"""

        user_input: str = input(prompt)

        return user_input

    @classmethod
    def get_command(cls, prompt: str) -> tuple[str, list[str]]:
        """Get user input - top level command"""

        user_input: str = cls._get_new(prompt)

        input_elements: list[str] = user_input.split()

        if len(input_elements) < 1:
            raise ValueError('No command given!')

        command: str = input_elements.pop(0)

        return command, input_elements

    @classmethod
    def get_answer(cls, prompt: str) -> tuple[str, str]:
        """Get user input - answer"""

        user_input: str = cls._get_new(prompt)

        command_test: list[str] = user_input.split('cmd ')
        if len(command_test) == 2 and command_test[0] == '':
            answer_type: str = cls.TYPE_COMMAND
            content: str = command_test[1]
        else:
            answer_type: str = cls.TYPE_ANSWER
            content: str = user_input

        return answer_type, content

    @classmethod
    def wait_for_enter(cls) -> None:
        """Wait for the user to press ENTER"""

        _ = cls._get_new('Press ENTER to continue...')
