# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Output"""

# imports: library
import enum

NO_BREAK_SPACE: str = '\u00a0'

DISPLAY_WIDTH: int = 100
BLANK: str = ' ............ '


class Align(enum.Enum):
    """Enum of string alignments with formatter values"""
    LEFT = '<'
    CENTER = '^'
    RIGHT = '>'


class Formatting(enum.Enum):
    """Enum of formatting types"""
    REGULAR = enum.auto()
    WIDE = enum.auto()
    INDENTED = enum.auto()


class Spacing(enum.Enum):
    """Enum of spacing types"""
    CLOSE = enum.auto()
    APART = enum.auto()


# template creation ---------------------------------------------- #

def _template(filler: str = ' ', align: Align = Align.LEFT, width: int = -1) -> str:
    """Template"""

    if width == -1:
        width = DISPLAY_WIDTH

    filler_replace: dict[str, str] = {
        '{': '\{',
        '}': '\}',
    }

    template: str = ':'

    if filler in filler_replace:
        filler = filler_replace[filler]

    template += filler
    template += align.value

    if not isinstance(width, int):
        raise ValueError('Given width is not an integer')

    if not width > 0:
        raise ValueError('Illegal width parameter')

    template += str(width)

    return '{' + template + '}'


def _block_lines(text: str,
                 width: int = -1,
                 line_start_first: str = '',
                 line_start_all: str = ''
                 ) -> list[str]:
    """Block lines"""

    if width == -1:
        width = DISPLAY_WIDTH

    lines: list[str] = []

    line_build: str = _init_line(line_start_first, line_start_all)
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
            line_build = _init_line(''.ljust(len(line_start_first), ' '), line_start_all)
        else:
            line_build = _init_line('', line_start_all)

        if len(words) == 0:
            break

    return lines


def _init_line(line_start_first: str, line_start_all: str) -> str:
    """Init line"""

    line_build: str = ''

    if len(line_start_all) > 0:
        line_build += f'{line_start_all} '

    if len(line_start_first) > 0:
        line_build += f'{line_start_first} '

    return line_build


# displays ------------------------------------------------------- #

def section_title(title: str) -> None:
    """Section title"""

    title: str = title.upper()

    empty_line(2)
    center(''.ljust(len(title) + 10, '='))
    center('===  ' + title + '  ===')
    center(''.ljust(len(title) + 10, '='))


def words_table(list_regular: list[str], list_phonetic: list[str]) -> None:
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
        template += _template(' ', Align.LEFT, unit_width)
        template += ' '

    print(template.format(*list_regular))
    print(template.format(*list_phonetic))


def new_words_extension(data: list[str]):
    """New words extension"""

    if len(data) == 0:
        return

    empty_line(1)

    print_list: list[str] = _block_lines(data.pop(0), DISPLAY_WIDTH, '□ ', '')

    if len(data) > 0:
        for unit in data:
            print_list += _block_lines(unit, DISPLAY_WIDTH, '  ', '')

    for line in print_list:
        print(line)


def framed(parts: list[str], width: int) -> None:
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

        lines += _block_lines(part, width, '', '')

    center(''.ljust(width + 2, '-'))
    center('| '.ljust(width + 2, ' ') + ' |')
    for line in lines:
        center('| ' + line + ' |')
    center('| '.ljust(width + 2, ' ') + ' |')
    center(''.ljust(width + 2, '-'))


def numbered_sentence(number: int,
                      sentence: str,
                      formatting: Formatting = Formatting.REGULAR
                      ) -> None:
    """Numbered sentence"""

    line_start_first: str = f'{number}.'

    line_start_all: str = ''
    if formatting == Formatting.INDENTED:
        line_start_all = '  | '

    print_list: list[str] = _block_lines(sentence, DISPLAY_WIDTH, line_start_first, line_start_all)

    for line in print_list:
        print(line)


def general_message(message: str) -> None:
    """General message"""

    empty_line(1)
    filled_line('#')
    center(message, '#')
    filled_line('#')


def simple(text: str):
    """Simple"""

    print_list: list[str] = _block_lines(text, DISPLAY_WIDTH, '', '')

    for line in print_list:
        print(line)


def center(text: str, filler: str = ' ') -> None:
    """Center"""

    template: str = _template(filler, Align.CENTER, DISPLAY_WIDTH)
    text: str = ' ' + text + ' '
    print(template.format(text))


def value_pair_list(collection: list[list[str]],
                    formatting: Formatting = Formatting.REGULAR,
                    spacing: Spacing = Spacing.CLOSE,
                    ) -> None:
    """Value pair list"""

    if formatting == Formatting.REGULAR:
        longest_key = 1

        for pair in collection:
            longest_key = max(longest_key, len(pair[0]))

        template: str = '  ' + _template(' ', Align.LEFT, longest_key) + ' : {}'

    elif formatting == Formatting.WIDE:
        for pair in collection:
            pair[0] = pair[0] + ' '

        template: str = '  {0:.<46} : {1: <49}'

    else:
        raise ValueError('Illegal format parameter')

    if spacing == Spacing.CLOSE:
        empty_line(1)

    for pair in collection:
        if spacing == Spacing.APART:
            empty_line(1)
        print(template.format(pair[0], pair[1]))


# special displays ----------------------------------------------- #

def empty_line(count: int = 1) -> None:
    """Empty line"""
    for _ in range(1, count + 1):
        print('')


def filled_line(character: str, count: int = 1) -> None:
    """Filled line"""
    for _ in range(1, count + 1):
        print(_template(character, Align.CENTER, DISPLAY_WIDTH).format(''))


# message displays ----------------------------------------------- #

def warning(text: str) -> None:
    """Warning"""
    print(text)


def error(text: str) -> None:
    """Error"""
    print(text)
