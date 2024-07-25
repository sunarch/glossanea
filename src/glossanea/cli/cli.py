# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""CLI"""

# imports: library
import enum
import random

# imports: project
from glossanea import version
from glossanea.cli import cli_unit
from glossanea.cli import output
from glossanea.cli import user_input
from glossanea.structure import data
from glossanea.structure import unit
from glossanea.structure.unit import Unit


class Command(enum.Enum):
    """Commands with default help values"""
    EMPTY = 'EMPTY'
    HELP = 'help'
    EXIT = 'quit'

    START = 'start'
    NEXT = 'next'
    RANDOM = 'random'
    GOTO = 'jump'


COMMAND_TEXTS: dict[str, Command] = {
    # only one option per starting letter (except typo options)
    'begin': Command.START,  # alias
    'exit': Command.EXIT,
    'goto': Command.GOTO,
    'help': Command.HELP,
    'jump': Command.GOTO,  # alias
    'next': Command.NEXT,
    'quit': Command.EXIT,  # alias
    'random': Command.RANDOM,
    'ransom': Command.RANDOM,  # typo option
    'start': Command.START,
}


def mainloop() -> None:
    """CLI main loop"""

    unit_obj: Unit = Unit(unit.MIN_WEEK_NUMBER, unit.MIN_DAY_NUMBER)

    display_introduction()

    while True:

        try:
            command_text, arguments = user_input.get_command(
                build_command_prompt(unit_obj.week_number, unit_obj.unit_number_display))
        except ValueError as ve:
            output.warning(str(ve))
            continue

        command: Command = Command.EMPTY
        if command_text in COMMAND_TEXTS:
            command = COMMAND_TEXTS[command_text]
        else:
            for key, value in COMMAND_TEXTS.items():
                try:
                    if key.index(command_text) == 0:
                        command = value
                except ValueError:
                    pass

        try:
            match command:
                # UI commands with zero arguments #
                case Command.EXIT:
                    break
                case Command.START:
                    cli_unit.run(unit_obj)
                case Command.HELP:
                    cmd_help()
                case Command.NEXT:
                    unit_obj = get_next_unit(unit_obj)
                    # TODO: temporary skip of weekly review until implemented
                    while unit_obj.is_weekly_review:
                        unit_obj = get_next_unit(unit_obj)
                    cli_unit.run(unit_obj)
                # UI commands with variable arguments #
                case Command.RANDOM:
                    unit_obj = get_random_unit(''.join(arguments))
                    # TODO: temporary skip of weekly review until implemented
                    while unit_obj.is_weekly_review:
                        unit_obj = get_random_unit(''.join(arguments))
                # UI commands with one or more arguments #
                case Command.GOTO:
                    unit_obj = get_specific_unit(unit_obj, arguments)
                # other inputs #
                case _:
                    raise KeyError('Invalid command!')

        except KeyError as exc:
            output.warning(str(exc))
            continue

        except ValueError as exc:
            output.warning(str(exc))
            continue

        except IndexError as exc:
            output.warning(str(exc))
            continue

    # else:  # executes after while condition becomes false #
    #     pass


# User Interface functions ------------------------------------------- #

def cmd_help() -> None:
    """Help with commands"""

    collection: list[list[str]] = [
        [Command.START.value, 'Start currently selected unit.'],
        [Command.EXIT.value, 'Exit the program.'],
        [Command.NEXT.value, 'Go to an start next unit.'],
        [f'{Command.GOTO.value} WEEK', 'Change to the unit of the first day in WEEK.'],
        [f'{Command.GOTO.value} WEEK UNIT', 'Change to UNIT in WEEK.'],
        [Command.RANDOM.value, 'Go to a random unit.'],
        [Command.HELP.value, 'Display this help text.']
    ]

    output.empty_line(1)
    output.center('Glossanea help')
    output.value_pair_list(collection, formatting=output.Formatting.WIDE)


def get_specific_unit(current_unit: Unit, arguments) -> Unit:
    """Create an instance of a specific unit"""

    if len(arguments) < 1:
        raise ValueError('No arguments given!')

    max_arguments: int = 2
    if len(arguments) > max_arguments:
        raise ValueError(f'Too many arguments: {len(arguments)} > {max_arguments}')

    week_number: int = unit.MIN_WEEK_NUMBER
    if len(arguments) >= 1:
        try:
            week_number = int(arguments[0])
        except ValueError as exc:
            raise ValueError from exc
    _ = unit.validate_week_number(week_number)

    unit_number: int = unit.MIN_DAY_NUMBER
    if len(arguments) == 2:
        try:
            unit_number = int(arguments[1])
        except ValueError as exc:
            if arguments[1].upper() == 'WR':
                unit_number = unit.WEEKLY_REVIEW_INDEX
            else:
                raise ValueError(f'Not a valid number: {arguments[1]}') from exc
    _ = unit.validate_unit_number(unit_number)

    # TODO: temporary skip of weekly review until implemented
    if unit_number == unit.WEEKLY_REVIEW_INDEX:
        output.simple('Weekly Reviews are not yet implemented!')
        output.empty_line(1)
        user_input.wait_for_enter()
        return current_unit

    return Unit(week_number, unit_number)


def get_next_unit(current_unit: Unit) -> Unit:
    """Create an instance of the next unit"""

    next_week_no: int = current_unit.week_number
    if current_unit.is_weekly_review:
        next_week_no += 1

    next_unit_no: int = (current_unit.unit_number + 1) % unit.UNITS_PER_WEEK

    if next_week_no > unit.MAX_WEEK_NUMBER:
        output.simple('End of units reached!')
        output.empty_line(1)
        user_input.wait_for_enter()
        return Unit(unit.MIN_WEEK_NUMBER, unit.MIN_DAY_NUMBER)

    return Unit(next_week_no, next_unit_no)


def get_random_unit(unit_type: str) -> Unit:
    """Create an instance of a random unit"""

    week_number: int = random.randint(unit.MIN_WEEK_NUMBER, unit.MAX_WEEK_NUMBER)

    match unit_type:
        case '':
            unit_number = random.randint(unit.MIN_DAY_NUMBER, unit.UNITS_PER_WEEK)
            if unit_number == unit.UNITS_PER_WEEK:
                unit_number = unit.WEEKLY_REVIEW_INDEX
        case 'day':
            unit_number = random.randint(unit.MIN_DAY_NUMBER, unit.MAX_DAY_NUMBER)
        case 'WR':
            unit_number = unit.WEEKLY_REVIEW_INDEX
        case _:
            raise ValueError('Incorrect unit type.')

    return Unit(week_number, unit_number)


# general displays --------------------------------------------------- #

def display_introduction() -> None:
    """Display introduction"""

    file_subpath: str = 'introduction.txt'
    intro_lines: list[str] = data.load_text_file_lines(file_subpath)

    output.empty_line(1)
    for line in intro_lines:
        output.center(line.rstrip())
    output.empty_line(1)


# other -------------------------------------------------------------- #

def build_command_prompt(week_number: int, unit_number_display: str) -> str:
    """Build command prompt"""

    return f'{version.PROGRAM_NAME.capitalize()} {week_number}/{unit_number_display} $ '
