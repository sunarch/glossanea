# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Day"""

# imports: library
from typing import Any, Callable

# imports: project
from glossanea.cli.output import CLIOutput
from glossanea.cli.user_input import CLIUserInput
from glossanea.structure.day import Day


class CLIDay:
    """CLI Day"""

    # constants
    INTRO_TEXT_WIDTH: int = 60

    CMD_HELP_ALIASES: list[str] = ['h', 'help']
    CMD_WORDS_ALIASES: list[str] = ['w', 'words']
    CMD_HINT_ALIASES: list[str] = ['hint']
    CMD_SKIP_ALIASES: list[str] = ['s', 'skip']
    CMD_EXIT_ALIASES: list[str] = [
        'e', 'exit',
        'q', 'quit',
    ]
    CMD_NEXT_ALIASES: list[str] = ['n', 'next']
    CMD_PREV_ALIASES: list[str] = ['p', 'prev']

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

                if a_content in cls.CMD_WORDS_ALIASES:
                    cls.new_words(False)
                    CLIOutput.empty_line(1)
                    l_pr_question()
                elif a_content in cls.CMD_HINT_ALIASES:
                    print('HINT: ' + ' / '.join([f'"{answer}"' for answer in answers]))
                    continue
                elif a_content in cls.CMD_SKIP_ALIASES:
                    return True
                elif a_content in cls.CMD_NEXT_ALIASES:
                    l_next_msg()
                    return False
                elif a_content in cls.CMD_PREV_ALIASES:
                    l_prev_msg()
                    cls._next_action = prev_action
                    return False
                elif a_content in cls.CMD_EXIT_ALIASES:
                    cls._next_action = cls.ACTION_EXIT
                    return False
                elif a_content in cls.CMD_HELP_ALIASES:
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
                                        sentence['beginning'] + CLIOutput.BLANK + sentence['end'],
                                        CLIOutput.FORMAT_INDENTED)

        new_words_extension: list[str] = cls._day.get_new_words_extension()

        CLIOutput.new_words_extension(new_words_extension)

        CLIOutput.empty_line(1)

        for sentence in data['sentences']:

            prompt: str = f'{sentence["id"]}. '

            def l_pr_question() -> None:
                """l_pr_question"""
                return CLIOutput.numbered_sentence(sentence['id'],
                                                   sentence['beginning'] + CLIOutput.BLANK + sentence['end'],
                                                   CLIOutput.FORMAT_REGULAR)

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
            CLIOutput.numbered_sentence(definition['id'], definition['text'], CLIOutput.FORMAT_INDENTED)

        def l_words() -> list[None]:
            """l_words"""
            return [CLIOutput.numbered_sentence(word['id'], word['text'], CLIOutput.FORMAT_INDENTED)
                    for word in data['words']]

        for definition in data['definitions']:

            prompt: str = f'{definition["id"]}. '

            def l_pr_question() -> None:
                """l_pr_question"""
                return CLIOutput.numbered_sentence(definition['id'], definition['text'], CLIOutput.FORMAT_REGULAR)

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
                return CLIOutput.numbered_sentence(answer_id, answer_text, CLIOutput.FORMAT_REGULAR)

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
            CLIOutput.numbered_sentence(sentence['id'], sentence['text'], CLIOutput.FORMAT_INDENTED)

        def l_words() -> list[None]:
            """l_words"""
            return [CLIOutput.numbered_sentence(word['id'], word['text'], CLIOutput.FORMAT_INDENTED)
                    for word in data['words']]

        for sentence in data['sentences']:

            prompt: str = f'{definition["id"]}. '

            def l_pr_question() -> None:
                """l_pr_question"""
                return CLIOutput.numbered_sentence(sentence['id'], sentence['text'], CLIOutput.FORMAT_REGULAR)

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
                return CLIOutput.numbered_sentence(answer_id, answer_text, CLIOutput.FORMAT_REGULAR)

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
            ['words', 'Display New Words section again.'],
            ['hint', 'Display the answer hint (use sparingly!)'],
            ['skip', 'Move on to the next part of the task.'],
            ['next', 'Leave task and move on to the next one.'],
            ['prev', 'Leave task and jump back to the previous one.'],
            ['exit', 'Leave task an exit to top program level.']
        ]

        CLIOutput.empty_line(1)
        CLIOutput.simple('Within the task, the following commands are available:')
        CLIOutput.value_pair_list(collection, CLIOutput.FORMAT_REGULAR, CLIOutput.SPACING_CLOSE)
