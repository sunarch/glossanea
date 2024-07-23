# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""CLI"""

# imports: project
from glossanea.structure.cycle import Cycle
from glossanea.structure.unit import Unit
from glossanea.files.data import data_file_path
from glossanea.cli import output
from glossanea.cli.output import CLIOutput
from glossanea.cli.user_input import CLIUserInput
from glossanea.cli.day import CLIDay
# from glossanea.cli.weekly_review import CLIWeeklyReview


class CLI:
    """CLI"""

    # constants
    CMD_HELP_ALIASES: list[str] = ['h', 'help']
    CMD_START_ALIASES: list[str] = [
        's', 'start',
        'b', 'begin',
    ]
    CMD_EXIT_ALIASES: list[str] = [
        'e', 'exit',
        'q', 'quit',
    ]
    CMD_NEXT_ALIASES: list[str] = ['n', 'next']
    CMD_RANDOM_ALIASES: list[str] = ['r', 'random']
    CMD_GOTO_ALIASES: list[str] = [
        'g', 'goto',
        'j', 'jump',
    ]

    # General variables #
    _done: bool = False
    _unit: Unit | None = None

    @classmethod
    def start(cls) -> None:
        """Start"""

        cls._unit = Cycle.get_day_by_number(1, 1)
        cls.mainloop()

    @classmethod
    def mainloop(cls) -> None:
        """Main loop"""

        # Introduction #
        cls.display_introduction()

        # Main Program Loop #

        while not cls._done:

            try:
                command, arguments = CLIUserInput.get_command(cls.build_command_prompt())
            except ValueError as ve:
                CLIOutput.warning(str(ve))
                continue

            # UI function invocations #
            try:
                # UI commands with zero arguments #

                if command in cls.CMD_HELP_ALIASES:
                    cls.cmd_help()

                elif command in cls.CMD_START_ALIASES:
                    cls.cmd_start()

                elif command in cls.CMD_NEXT_ALIASES:
                    cls.cmd_next()

                elif command in cls.CMD_EXIT_ALIASES:
                    cls.cmd_exit()

                # UI commands with variable arguments #

                elif command in cls.CMD_RANDOM_ALIASES:
                    cls.cmd_random(arguments)

                # UI commands with one or more arguments #

                elif command in cls.CMD_GOTO_ALIASES:
                    cls.cmd_goto(arguments)

                # other inputs #
                else:
                    raise KeyError('Invalid command!')

            except KeyError as exc:
                CLIOutput.warning(str(exc))
                continue

            except ValueError as exc:
                CLIOutput.warning(str(exc))
                continue

            except IndexError as exc:
                CLIOutput.warning(str(exc))
                continue

        # else:  # executes after while condition becomes false #
        #     pass

        # end of the Main Program Loop #

    # User Interface functions --------------------------------------- #

    @classmethod
    def cmd_exit(cls) -> None:
        """Command: exit"""

        cls._done = True

    @classmethod
    def cmd_help(cls) -> None:
        """Command: help"""

        collection: list[list[str]] = [
            ['start', 'Start currently selected unit.'],
            ['begin', 'Same as "start".'],
            ['exit', 'Exit the program.'],
            ['quit', 'Same as "exit".'],
            ['q', 'Same as "exit".'],
            ['next', 'Go to an start next unit.'],
            ['goto WEEK', 'Change selected unit to the first day in WEEK.'],
            ['goto WEEK UNIT', 'Change selected unit to UNIT in WEEK.'],
            ['jump', 'Same as "goto".'],
            ['help', 'Display this help text.']
        ]

        CLIOutput.empty_line(1)
        CLIOutput.center('Glossanea help')
        CLIOutput.value_pair_list(collection, output.Formatting.WIDE, output.Spacing.APART)

    @classmethod
    def cmd_start(cls) -> None:
        """Command: start"""

        CLIDay.start(cls._unit)

    @classmethod
    def cmd_next(cls) -> None:
        """Command: next"""

        week_number: int = cls._unit.get_week_no()
        unit_number: int = cls._unit.get_unit_no()

        try:
            prev_unit: Unit = cls._unit
            cls._unit = Cycle.get_next_unit(week_number, unit_number)
            del prev_unit
        except IndexError as exc:
            raise IndexError from exc

        # TODO: temporary skip of weekly review until implemented ˇˇˇˇ #
        week_number: int = cls._unit.get_week_no()
        unit_number: int = cls._unit.get_unit_no()

        if cls._unit.get_unit_type() == Unit.TYPE_WEEKLY_REVIEW:
            try:
                prev_unit: Unit = cls._unit
                cls._unit = Cycle.get_next_unit(week_number, unit_number)
                del prev_unit
            except IndexError as exc:
                raise IndexError from exc
        # END_TODO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ #

        cls.cmd_start()

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

            if cls._unit.get_unit_type() == Unit.TYPE_DAY:
                break

        del prev_unit

        cls.cmd_start()

    # general displays ----------------------------------------------- #

    @classmethod
    def display_introduction(cls):
        """Display introduction"""

        path: str = data_file_path('introduction.txt')
        CLIOutput.empty_line(1)
        with open(path, 'r', encoding='UTF-8') as fh_intro:
            for line in fh_intro.readlines():
                CLIOutput.center(line.rstrip())
        CLIOutput.empty_line(1)

    # other ---------------------------------------------------------- #

    @classmethod
    def build_command_prompt(cls):
        """Build command prompt"""

        week: int = cls._unit.get_week_no()
        day: int | str = cls._unit.get_unit_no()

        if day == Unit.WEEKLY_REVIEW_INDEX:
            day = 'WR'

        return f'Glossanea {week}/{day} $ '
