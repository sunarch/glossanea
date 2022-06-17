# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

class CLIUserInput:

    # constants
    TYPE_COMMAND = "command"
    TYPE_ANSWER = "answer"

    @classmethod
    def _get_new(cls, prompt):
        """Get user input"""

        user_input = input(prompt)

        return user_input

    @classmethod
    def get_command(cls, prompt):
        """Get user input - top level command"""

        user_input = cls._get_new(prompt)

        input_elements = user_input.split()

        if len(input_elements) < 1:
            raise ValueError("No command given!")

        command = input_elements.pop(0)

        return command, input_elements

    @classmethod
    def get_answer(cls, prompt):
        """Get user input - answer"""

        user_input = cls._get_new(prompt)
        
        command_test = user_input.split("cmd ")
        if len(command_test) == 2 and command_test[0] == "":
            answer_type = cls.TYPE_COMMAND
            content = command_test[1]
        else:
            answer_type = cls.TYPE_ANSWER
            content = user_input
        
        return answer_type, content

    @classmethod
    def wait_for_enter(cls):
        """Wait for the user to press ENTER"""

        user_input = cls._get_new("Press ENTER to continue...")

        return
