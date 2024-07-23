# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Output"""


NO_BREAK_SPACE: str = '\u00a0'

DISPLAY_WIDTH: int = 100
BLANK: str = ' ............ '


class CLIOutput:
    """CLI Output"""

    # constants ------------------------------------------------------ #

    ALIGN_LEFT: str = 'left'
    ALIGN_CENTER: str = 'center'
    ALIGN_RIGHT: str = 'right'

    FORMAT_REGULAR: str = 'regular'
    FORMAT_WIDE: str = 'wide'
    FORMAT_INDENTED: str = 'indented'

    SPACING_CLOSE: str = 'close'
    SPACING_APART: str = 'apart'

    # template creation ---------------------------------------------- #

    @classmethod
    def _template(cls, filler: str = ' ', align: str = 'left', width: int = -1) -> str:
        """Template"""

        if width == -1:
            width = DISPLAY_WIDTH

        filler_replace: dict[str, str] = {
            '{': '\{',
            '}': '\}'
        }

        template: str = ':'

        if filler in filler_replace:
            filler = filler_replace[filler]

        template += filler

        if align == cls.ALIGN_LEFT:
            template += '<'
        elif align == cls.ALIGN_CENTER:
            template += '^'
        elif align == cls.ALIGN_RIGHT:
            template += '>'
        else:
            raise ValueError('Incorrect alignment parameter')

        if not isinstance(width, int):
            raise ValueError('Given width is not an integer')

        if not width > 0:
            raise ValueError('Illegal width parameter')

        template += str(width)

        return '{' + template + '}'

    @classmethod
    def _block_lines(cls,
                     text: str,
                     width: int = -1,
                     line_start_first: str = '',
                     line_start_all: str = ''
                     ) -> list[str]:
        """Block lines"""

        if width == -1:
            width = DISPLAY_WIDTH

        lines: list[str] = []

        line_build: str = cls._init_line(line_start_first, line_start_all)
        line_start_length: int = len(line_build)

        words: list[str] = text.split(' ')

        while True:

            if len(words) != 0:
                if len(line_build + ' ' + words[0]) <= width:

                    if len(line_build) > line_start_length:
                        line_build += ' '

                    line_build += words.pop(0)
                    continue

            line_build = line_build.ljust(width, ' ')
            lines.append(line_build)

            # start new line
            if len(line_start_first) > 0:
                line_build = cls._init_line(''.ljust(len(line_start_first), ' '), line_start_all)
            else:
                line_build = cls._init_line('', line_start_all)

            if len(words) == 0:
                break

        return lines

    @classmethod
    def _init_line(cls, line_start_first: str, line_start_all: str) -> str:
        """Init line"""

        line_build: str = ''

        if len(line_start_all) > 0:
            line_build += f'{line_start_all} '

        if len(line_start_first) > 0:
            line_build += f'{line_start_first} '

        return line_build

    # displays ------------------------------------------------------- #

    @classmethod
    def section_title(cls, title: str) -> None:
        """Section title"""

        title: str = title.upper()

        cls.empty_line(2)
        cls.center(''.ljust(len(title) + 10, '='))
        cls.center('===  ' + title + '  ===')
        cls.center(''.ljust(len(title) + 10, '='))

    @classmethod
    def words_table(cls, list_regular: list[str], list_phonetic: list[str]) -> None:
        """Words table"""

        template: str = ''

        if len(list_regular) != len(list_phonetic):
            raise ValueError('Word lists are not equal length')

        unit_width: int = int(DISPLAY_WIDTH / len(list_regular)) - 3

        for word in list_regular:
            unit_width = max(unit_width, len(word))

        for word in list_phonetic:
            if (len(word) + 2) > unit_width:
                unit_width = len(word)

        for _ in range(1, len(list_regular) + 1):
            template += '| '
            template += cls._template(' ', 'left', unit_width)
            template += ' '

        print(template.format(*list_regular))
        print(template.format(*list_phonetic))

    @classmethod
    def new_words_extension(cls, data: list[str]):
        """New words extension"""

        if len(data) == 0:
            return

        cls.empty_line(1)

        print_list: list[str] = cls._block_lines(data.pop(0), DISPLAY_WIDTH, '□ ', '')

        if len(data) > 0:
            for unit in data:
                print_list += cls._block_lines(unit, DISPLAY_WIDTH, '  ', '')

        for line in print_list:
            print(line)

    @classmethod
    def framed(cls, parts: list[str], width: int) -> None:
        """Framed"""

        if width > DISPLAY_WIDTH:
            width = DISPLAY_WIDTH - 4

        lines = []

        for part in parts:

            if NO_BREAK_SPACE in part:
                to_pad: int = width - len(part)
                padding_right: int = to_pad // 2  # div
                size_with_right: int = len(part) + padding_right
                # padding_left = padding_right + (to_pad % 2) # same + mod

                lines.append(part.rjust(size_with_right, ' ').ljust(width, ' '))

                continue

            lines += cls._block_lines(part, width, '', '')

        cls.center(''.ljust(width + 2, '-'))
        cls.center('| '.ljust(width + 2, ' ') + ' |')
        for line in lines:
            cls.center('| ' + line + ' |')
        cls.center('| '.ljust(width + 2, ' ') + ' |')
        cls.center(''.ljust(width + 2, '-'))

    @classmethod
    def numbered_sentence(cls, number: int, sentence: str, formatting: str = '') -> None:
        """Numbered sentence"""

        if formatting == '':
            formatting = cls.FORMAT_REGULAR

        line_start_first: str = f'{number}.'

        if formatting == cls.FORMAT_INDENTED:
            line_start_all: str = '  | '
        else:
            line_start_all: str = ''

        print_list: list[str] = cls._block_lines(sentence, DISPLAY_WIDTH, line_start_first, line_start_all)

        for line in print_list:
            print(line)

    @classmethod
    def general_message(cls, message: str) -> None:
        """General message"""

        cls.empty_line(1)
        cls.filled_line('#')
        cls.center(message, '#')
        cls.filled_line('#')

    @classmethod
    def simple(cls, text: str):
        """Simple"""

        print_list: list[str] = cls._block_lines(text, DISPLAY_WIDTH, '', '')

        for line in print_list:
            print(line)

    @classmethod
    def center(cls, text: str, filler: str = ' ') -> None:
        """Center"""

        template: str = cls._template(filler, cls.ALIGN_CENTER, DISPLAY_WIDTH)
        text: str = ' ' + text + ' '
        print(template.format(text))

    @classmethod
    def value_pair_list(cls,
                        collection: list[list[str]],
                        formatting: str = '',
                        spacing: str = '',
                        ) -> None:
        """Value pair list"""

        if formatting == '':
            formatting = cls.FORMAT_REGULAR

        if spacing == '':
            spacing = cls.SPACING_CLOSE

        if formatting == cls.FORMAT_REGULAR:
            longest_key = 1

            for pair in collection:
                longest_key = max(longest_key, len(pair[0]))

            template: str = '  ' + cls._template(' ', cls.ALIGN_LEFT, longest_key) + ' : {}'

        elif formatting == cls.FORMAT_WIDE:
            for pair in collection:
                pair[0] = pair[0] + ' '

            template: str = '  {0:.<46} : {1: <49}'

        else:
            raise ValueError('Illegal format parameter')

        if spacing == cls.SPACING_CLOSE:
            cls.empty_line(1)

        for pair in collection:
            if spacing == cls.SPACING_APART:
                cls.empty_line(1)
            print(template.format(pair[0], pair[1]))

    # special displays ----------------------------------------------- #

    @classmethod
    def empty_line(cls, count: int = 1) -> None:
        """Empty line"""
        for _ in range(1, count + 1):
            print('')

    @classmethod
    def filled_line(cls, character: str, count: int = 1) -> None:
        """Filled line"""
        for _ in range(1, count + 1):
            print(cls._template(character, cls.ALIGN_CENTER, DISPLAY_WIDTH).format(''))

    # message displays ----------------------------------------------- #

    @classmethod
    def warning(cls, text: str) -> None:
        """Warning"""
        print(text)

    @classmethod
    def error(cls, text: str) -> None:
        """Error"""
        print(text)
