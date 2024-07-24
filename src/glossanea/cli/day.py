# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Day"""

# imports: library
import enum
from typing import Any, Callable

# imports: project
from glossanea.cli import output
from glossanea.cli.output import CLIOutput
from glossanea.cli.user_input import CLIUserInput
from glossanea.structure.day import Day


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


class CLIDay:
    """CLI Day"""

    # constants
    INTRO_TEXT_WIDTH: int = 60

    ACTION_EXIT: str = 'exit'
    ACTION_TITLE: str = 'title'
    ACTION_NEW_WORDS: str = 'new words'
    ACTION_INTRO_TEXT: str = 'intro text'
    ACTION_SAMPLE_SENTENCES: str = 'sample sentences'
    ACTION_DEFINITIONS: str = 'definitions'
    ACTION_MATCHING: str = 'matching'
    ACTION_OTHER_NEW_WORDS: str = 'other new words'

    # General variables #
    _next_action: str | None = None
    _day: Day | None = None

    @classmethod
    def start(cls, day) -> None:
        """Start"""

        cls._day = day
        cls.mainloop()

    @classmethod
    def mainloop(cls) -> None:
        """Main loop"""

        cls._next_action = 'title'

        while cls._next_action != cls.ACTION_EXIT:

            if cls._next_action == cls.ACTION_TITLE:
                cls._next_action = cls.ACTION_NEW_WORDS
                cls.title()

            elif cls._next_action == cls.ACTION_NEW_WORDS:
                cls._next_action = cls.ACTION_INTRO_TEXT
                cls.new_words()
                CLIOutput.empty_line(1)
                CLIUserInput.wait_for_enter()

            elif cls._next_action == cls.ACTION_INTRO_TEXT:
                cls._next_action = cls.ACTION_SAMPLE_SENTENCES
                cls.intro_text()
                CLIOutput.empty_line(1)
                CLIUserInput.wait_for_enter()

            elif cls._next_action == cls.ACTION_SAMPLE_SENTENCES:
                cls._next_action = cls.ACTION_DEFINITIONS
                cls.sample_sentences()

            elif cls._next_action == cls.ACTION_DEFINITIONS:
                cls._next_action = cls.ACTION_MATCHING
                cls.definitions()

            elif cls._next_action == cls.ACTION_MATCHING:
                cls._next_action = cls.ACTION_OTHER_NEW_WORDS
                cls.matching()

            elif cls._next_action == cls.ACTION_OTHER_NEW_WORDS:
                cls._next_action = cls.ACTION_EXIT
                cls.other_new_words()

            else:
                raise KeyError('Unknown action request.')

# day displays ------------------------------------------------------- #

    @classmethod
    def title(cls) -> None:
        """Display title"""

        CLIOutput.empty_line(1)
        CLIOutput.center(cls._day.get_title())

    @classmethod
    def new_words(cls, display_in_full=True) -> None:
        """Display new words section"""

        regular: list[str] = []
        phonetic: list[str] = []

        for unit in cls._day.get_new_words():
            regular.append(unit['regular'])
            phonetic.append(unit['phonetic'])

        if display_in_full:
            CLIOutput.section_title('NEW WORDS')
            CLIOutput.empty_line(1)

        CLIOutput.empty_line(1)
        CLIOutput.words_table(regular, phonetic)

    @classmethod
    def intro_text(cls) -> None:
        """Display intro text"""

        parts: list[str] = cls._day.get_intro_text()

        CLIOutput.empty_line(2)
        CLIOutput.framed(parts, cls.INTRO_TEXT_WIDTH)

# task answer cycle -------------------------------------------------- #

    @classmethod
    def _answer_cycle(cls,
                      prompt: str,
                      l_pr_question: Callable[[], None],
                      answers: list[str],
                      l_pr_answer: Callable[[], None],
                      prev_action: str,
                      l_prev_msg: Callable[[], None],
                      l_next_msg: Callable[[], None],
                      ):
        """Answer cycle"""

        while True:
            CLIOutput.empty_line(1)
            a_type, a_content = CLIUserInput.get_answer(prompt)

            if a_type not in {CLIUserInput.TYPE_ANSWER, CLIUserInput.TYPE_COMMAND}:
                raise ValueError('Unknown answer type.')

            if a_type == CLIUserInput.TYPE_ANSWER:

                if a_content not in answers:
                    CLIOutput.warning('Incorrect, try again.')
                    continue

                CLIOutput.empty_line(1)
                l_pr_answer()
                CLIOutput.empty_line(1)
                CLIOutput.simple('Correct!')

                return True

            if a_type == CLIUserInput.TYPE_COMMAND:

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

                if command == Command.WORDS:
                    cls.new_words(False)
                    CLIOutput.empty_line(1)
                    l_pr_question()
                elif command == Command.SOLUTION:
                    print('HINT: ' + ' / '.join([f'"{answer}"' for answer in answers]))
                    continue
                elif command == Command.NEXT:
                    return True
                elif command == Command.JUMP:
                    l_next_msg()
                    return False
                elif command == Command.PREVIOUS:
                    l_prev_msg()
                    cls._next_action = prev_action
                    return False
                elif command == Command.EXIT:
                    cls._next_action = cls.ACTION_EXIT
                    return False
                elif command == Command.HELP:
                    cls.help_cmd_in_task()
                else:
                    CLIOutput.warning('Invalid command.')

# tasks -------------------------------------------------------------- #

    @classmethod
    def sample_sentences(cls):
        """Display 'sample sentences' task"""

        data: dict[str, Any] = cls._day.get_sample_sentences()

        CLIOutput.section_title('SAMPLE SENTENCES')

        CLIOutput.empty_line(1)
        CLIOutput.simple(data['prompt'])

        CLIOutput.empty_line(1)

        for sentence in data['sentences']:
            CLIOutput.numbered_sentence(sentence['id'],
                                        sentence['beginning'] + output.BLANK + sentence['end'],
                                        output.Formatting.INDENTED)

        new_words_extension: list[str] = cls._day.get_new_words_extension()

        CLIOutput.new_words_extension(new_words_extension)

        CLIOutput.empty_line(1)

        for sentence in data['sentences']:

            prompt: str = f'{sentence["id"]}. '

            def l_pr_question() -> None:
                """l_pr_question"""
                return CLIOutput.numbered_sentence(sentence['id'],
                                                   sentence['beginning'] + output.BLANK + sentence['end'])

            answers: list[str] = [sentence['answer']]

            full_answer: str = sentence['answer']
            if len(sentence['beginning']) > 0:
                full_answer = f'{sentence["beginning"]} {full_answer}'
            if len(sentence['end']) > 0:
                if sentence['end'] not in ['.', '!', '?', '?!', '!?']:
                    full_answer += ' '
                full_answer += sentence['end']

            def l_pr_answer() -> None:
                """l_pr_answer"""
                return CLIOutput.simple(full_answer)

            prev_action: str = cls.ACTION_SAMPLE_SENTENCES

            def l_prev_msg() -> None:
                """l_prev_msg"""
                return CLIOutput.general_message('This is the first task: Starting from the beginning.')

            def l_next_msg() -> None:
                """l_next_msg"""
                return None

            # answer cycle

            cls.new_words(False)
            CLIOutput.empty_line(1)
            l_pr_question()

            if not cls._answer_cycle(prompt, l_pr_question, answers, l_pr_answer, prev_action, l_prev_msg, l_next_msg):
                return

            # return after answer cycle returns

    @classmethod
    def definitions(cls):
        """Display 'definitions' task"""

        # skip until data files are complete
        return

        data: dict[str, Any] = cls._day.get_definitions()

        CLIOutput.section_title('DEFINITIONS')

        CLIOutput.empty_line(1)
        CLIOutput.simple(data['prompt'])

        CLIOutput.empty_line(1)
        for definition in data['definitions']:
            CLIOutput.numbered_sentence(definition['id'], definition['text'], output.Formatting.INDENTED)

        def l_words() -> list[None]:
            """l_words"""
            return [CLIOutput.numbered_sentence(word['id'], word['text'], output.Formatting.INDENTED)
                    for word in data['words']]

        for definition in data['definitions']:

            prompt: str = f'{definition["id"]}. '

            def l_pr_question() -> None:
                """l_pr_question"""
                return CLIOutput.numbered_sentence(definition['id'], definition['text'])

            answers: list[str] = []
            answer_id: str = [
                value
                for (item_id, value) in data['answers']
                if item_id == definition['id']
            ][0]
            answers.append(answer_id)
            answer_text: str = [
                item['text']
                for item in data['words']
                if item['id'] == answer_id
            ][0]
            answers.append(answer_text)

            def l_pr_answer() -> None:
                """l_pr_answer"""
                return CLIOutput.numbered_sentence(answer_id, answer_text)

            prev_action: str = cls.ACTION_SAMPLE_SENTENCES

            def l_prev_msg() -> None:
                """l_prev_msg"""
                return None

            def l_next_msg() -> None:
                """l_next_msg"""
                return None

            # answer cycle

            CLIOutput.empty_line(2)
            l_words()
            CLIOutput.empty_line(1)
            l_pr_question()

            if not cls._answer_cycle(prompt, l_pr_question, answers, l_pr_answer, prev_action, l_prev_msg, l_next_msg):
                return

            # return after answer cycle returns

    @classmethod
    def matching(cls) -> None:
        """Display 'matching' task"""

        # skip until data files are complete
        return

        data: dict[str, Any] = cls._day.get_matching()

        CLIOutput.section_title(data['name'])

        CLIOutput.empty_line(1)
        CLIOutput.simple(data['prompt'])

        CLIOutput.empty_line(1)
        for sentence in data['sentences']:
            CLIOutput.numbered_sentence(sentence['id'], sentence['text'], output.Formatting.INDENTED)

        def l_words() -> list[None]:
            """l_words"""
            return [CLIOutput.numbered_sentence(word['id'], word['text'], output.Formatting.INDENTED)
                    for word in data['words']]

        for sentence in data['sentences']:

            prompt: str = f'{definition["id"]}. '

            def l_pr_question() -> None:
                """l_pr_question"""
                return CLIOutput.numbered_sentence(sentence['id'], sentence['text'])

            answers: list[str] = []
            answer_id: str = [
                value
                for (item_id, value) in data['answers']
                if item_id == sentence['id']
            ][0]
            answers.append(answer_id)
            answer_text: str = [
                item['text']
                for item in data['words']
                if item['id'] == answer_id
            ][0]
            answers.append(answer_text)

            def l_pr_answer() -> None:
                """l_pr_answer"""
                return CLIOutput.numbered_sentence(answer_id, answer_text)

            prev_action: str = cls.ACTION_SAMPLE_SENTENCES

            def l_prev_msg() -> None:
                """l_prev_msg"""
                return None

            def l_next_msg() -> None:
                """l_next_msg"""
                return None

            # answer cycle

            CLIOutput.empty_line(2)
            l_words()
            CLIOutput.empty_line(1)
            l_pr_question()

            if not cls._answer_cycle(prompt, l_pr_question, answers, l_pr_answer, prev_action, l_prev_msg, l_next_msg):
                return

            # return after answer cycle returns

    @classmethod
    def other_new_words(cls) -> None:
        """Display other new words section"""

        data: dict[str, str] = cls._day.get_other_new_words()

        CLIOutput.section_title('OTHER NEW WORDS:')

        CLIOutput.empty_line(1)
        CLIOutput.simple(data['prompt'])

        CLIOutput.empty_line(1)
        _, _ = CLIUserInput.get_answer('')

        CLIOutput.empty_line(1)

# helper ------------------------------------------------------------- #

    @classmethod
    def help_cmd_in_task(cls) -> None:
        """Help cmd in task"""

        collection: list[list[str]] = [
            [Command.WORDS.value, 'Display New Words section again.'],
            [Command.SOLUTION.value, 'Display the answer hint (use sparingly!)'],
            [Command.NEXT.value, 'Move on to the next part of the task.'],
            [Command.JUMP.value, 'Leave task and move on to the next one.'],
            [Command.PREVIOUS.value, 'Leave task and jump back to the previous one.'],
            [Command.EXIT.value, 'Leave task an exit to top program level.']
        ]

        CLIOutput.empty_line(1)
        CLIOutput.simple('Within the task, the following commands are available:')
        CLIOutput.value_pair_list(collection)
