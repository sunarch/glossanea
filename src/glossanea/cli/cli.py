# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""CLI"""

# imports: library
import enum

# imports: project
from glossanea.structure.cycle import Cycle
from glossanea.structure import unit
from glossanea.structure.unit import Unit
from glossanea.files.data import data_file_path
from glossanea.cli import output
from glossanea.cli import user_input
from glossanea.cli.unit import run as run_unit


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


class CLI:
    """CLI"""

    # General variables #
    _unit: Unit | None = None

    @classmethod
    def start(cls) -> None:
        """Start / main loop"""

        cls._unit = Cycle.get_day_by_number(1, 1)

        # Introduction #
        display_introduction()

        # Main Program Loop #

        while True:

            try:
                command_text, arguments = user_input.get_command(build_command_prompt(cls._unit.week_number,
                                                                                      cls._unit.unit_number))
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

            # UI function invocations #
            try:

                match command:
                    # UI commands with zero arguments #
                    case Command.EXIT:
                        break
                    case Command.START:
                        run_unit(cls._unit)
                    case Command.HELP:
                        cls.cmd_help()
                    case Command.NEXT:
                        cls.cmd_next()
                    # UI commands with variable arguments #
                    case Command.RANDOM:
                        cls.cmd_random(arguments)
                    # UI commands with one or more arguments #
                    case Command.GOTO:
                        cls.cmd_goto(arguments)
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

        # end of the Main Program Loop #

    # User Interface functions --------------------------------------- #

    @classmethod
    def cmd_help(cls) -> None:
        """Command: help"""

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

    @classmethod
    def cmd_next(cls) -> None:
        """Command: next"""

        week_number: int = cls._unit.week_number
        unit_number: int = cls._unit.unit_number

        try:
            prev_unit: Unit = cls._unit
            cls._unit = Cycle.get_next_unit(week_number, unit_number)
            del prev_unit
        except IndexError as exc:
            raise IndexError from exc

        # TODO: temporary skip of weekly review until implemented ˇˇˇˇ #
        week_number: int = cls._unit.week_number
        unit_number: int = cls._unit.unit_number

        if cls._unit.unit_type == unit.UnitType.WEEKLY_REVIEW:
            try:
                prev_unit: Unit = cls._unit
                cls._unit = Cycle.get_next_unit(week_number, unit_number)
                del prev_unit
            except IndexError as exc:
                raise IndexError from exc
        # END_TODO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ #

        run_unit(cls._unit)

    @classmethod
    def cmd_goto(cls, arguments):
        """Command: goto"""

        if len(arguments) == 1:
            try:
                week_number: int = int(arguments[0])
                prev_unit: Unit = cls._unit
                cls._unit = Cycle.get_first_day_by_week(week_number)
                del prev_unit
            except ValueError as exc:
                raise ValueError from exc

        elif len(arguments) == 2:
            try:
                week_number: int = int(arguments[0])
                day_number: int = int(arguments[1])
                prev_unit: Unit = cls._unit
                cls._unit = Cycle.get_day_by_number(week_number, day_number)
                del prev_unit
            except ValueError as exc:
                raise ValueError from exc

        else:
            raise ValueError('Wrong number of arguments!')

    @classmethod
    def cmd_random(cls, arguments: list[str]):
        """Command: random"""

        prev_unit: Unit = cls._unit

        while True:
            # TODO: remove loop after Weekly Reviews are implemented

            try:
                if len(arguments) == 0:
                    cls._unit = Cycle.get_random_unit(None)
                else:
                    cls._unit = Cycle.get_random_unit(' '.join(arguments))
            except ValueError as exc:
                raise ValueError from exc

            if cls._unit.unit_type == unit.UnitType.DAY:
                break

        del prev_unit

        run_unit(cls._unit)


# general displays ----------------------------------------------- #

def display_introduction():
    """Display introduction"""

    path: str = data_file_path('introduction.txt')
    output.empty_line(1)
    with open(path, 'r', encoding='UTF-8') as fh_intro:
        for line in fh_intro.readlines():
            output.center(line.rstrip())
    output.empty_line(1)


# other -------------------------------------------------------------- #

def build_command_prompt(week_number: int, unit_number: int):
    """Build command prompt"""

    if unit_number == unit.WEEKLY_REVIEW_INDEX:
        unit_number_display: str = 'WR'
    else:
        unit_number_display: str = f'{unit_number}'

    return f'Glossanea {week_number}/{unit_number_display} $ '
