#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

class CLIOutput:

    # constants ------------------------------------------------------ #

    DISPLAY_WIDTH = 100
    BLANK = ' ............ '
    
    ALIGN_LEFT = 'left'
    ALIGN_CENTER = 'center'
    ALIGN_RIGHT = 'right'
    
    FORMAT_REGULAR = 'regular'
    FORMAT_WIDE = 'wide'
    FORMAT_INDENTED = 'indented'
    
    SPACING_CLOSE = 'close'
    SPACING_APART = 'apart'

    # template creation ---------------------------------------------- #

    @classmethod
    def _template(cls, filler=' ', align='left', width=-1):

        if width == -1:
            width = cls.DISPLAY_WIDTH

        filler_replace = {
            '{': '\{',
            '}': '\}'
        }

        template = ':'

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
    def _block_lines(cls, text, width=-1, line_start_first='', line_start_all=''):

        if width == -1:
            width = cls.DISPLAY_WIDTH

        lines = list()

        line_build = cls._init_line(line_start_first, line_start_all)
        line_start_length = len(line_build)

        words = text.split(' ')

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
    def _init_line(cls, line_start_first, line_start_all):

        line_build = ''

        if len(line_start_all) > 0:
            line_build += f'{line_start_all} '

        if len(line_start_first) > 0:
            line_build += f'{line_start_first} '

        return line_build

    # displays ------------------------------------------------------- #

    @classmethod
    def section_title(cls, title):

        title = title.upper()

        cls.empty_line(2)
        cls.center(''.ljust(len(title) + 10, '='))
        cls.center('===  ' + title + '  ===')
        cls.center(''.ljust(len(title) + 10, '='))

    @classmethod
    def words_table(cls, list_regular, list_phonetic):

        template = ''

        if len(list_regular) != len(list_phonetic):
            raise ValueError('Word lists are not equal length')

        unit_width = int(cls.DISPLAY_WIDTH / len(list_regular)) - 3

        for word in list_regular:
            if len(word) > unit_width:
                unit_width = len(word)

        for word in list_phonetic:
            if (len(word) + 2) > unit_width:
                unit_width = len(word)

        for i in range(1, len(list_regular) + 1):
            template += '| '
            template += cls._template(' ', 'left', unit_width)
            template += ' '

        print(template.format(*list_regular))
        print(template.format(*list_phonetic))

    @classmethod
    def new_words_extension(cls, data):

        if len(data) == 0:
            return

        cls.empty_line(1)

        print_list = cls._block_lines(data.pop(0), cls.DISPLAY_WIDTH, '□ ', '')

        if len(data) > 0:
            for unit in data:
                print_list += cls._block_lines(unit, cls.DISPLAY_WIDTH, '  ', '')

        for line in print_list:
            print(line)

    @classmethod
    def framed(cls, parts, width):

        if width > cls.DISPLAY_WIDTH:
            width = cls.DISPLAY_WIDTH - 4

        lines = list()

        for part in parts:

            if '\u00a0' in part:
                to_pad = width - len(part)
                padding_right = to_pad // 2  # div
                size_with_right = len(part) + padding_right
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
    def numbered_sentence(cls, number, sentence, formatting=''):

        if formatting == '':
            formatting = cls.FORMAT_REGULAR

        line_start_first = '{}.'.format(number)

        if formatting == cls.FORMAT_INDENTED:
            line_start_all = '  | '
        else:
            line_start_all = ''

        print_list = cls._block_lines(sentence, cls.DISPLAY_WIDTH, line_start_first, line_start_all)

        for line in print_list:
            print(line)

    @classmethod
    def general_message(cls, message):
        cls.empty_line(1)
        cls.filled_line('#')
        cls.center(message, '#')
        cls.filled_line('#')

    @classmethod
    def simple(cls, text):
        print_list = cls._block_lines(text, cls.DISPLAY_WIDTH, '', '')

        for line in print_list:
            print(line)

    @classmethod
    def center(cls, text, filler=' '):
        template = cls._template(filler, cls.ALIGN_CENTER, cls.DISPLAY_WIDTH)
        text = ' ' + text + ' '
        print(template.format(text))

    @classmethod
    def value_pair_list(cls, collection, formatting='', spacing=''):
        
        if formatting == '':
            formatting = cls.FORMAT_REGULAR
            
        if spacing == '':
            spacing = cls.SPACING_CLOSE
        
        if formatting == cls.FORMAT_REGULAR:
            longest_key = 1
            
            for pair in collection:
                if len(pair[0]) > longest_key:
                    longest_key = len(pair[0])
            
            template = '  ' + cls._template(' ', cls.ALIGN_LEFT, longest_key) + ' : {}'
        
        elif formatting == cls.FORMAT_WIDE:
            for pair in collection:
                pair[0] = pair[0] + ' '
        
            template = '  {0:.<46} : {1: <49}'
        
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
    def empty_line(cls, count=1):
        for i in range(1, count + 1):
            print('')
    
    @classmethod
    def filled_line(cls, character, count=1):
        for i in range(1, count + 1):
            print(cls._template(character, cls.ALIGN_CENTER, cls.DISPLAY_WIDTH).format(''))

    # message displays ----------------------------------------------- #

    @classmethod
    def warning(cls, text):
        print(text)

    @classmethod
    def error(cls, text):
        print(text)
