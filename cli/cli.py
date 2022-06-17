# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from structure.user_interface import UserInterface

from structure.cycle import Cycle
from structure.unit import Unit

from cli.output import CLIOutput
from cli.user_input import CLIUserInput
from cli.day import CLIDay
# from cli.weekly_review import CLIWeeklyReview


class CLI(UserInterface):

    # constants
    CMD_HELP_ALIASES = ["h", "help"]
    CMD_START_ALIASES = ["s", "start",
                         "b", "begin"]
    CMD_EXIT_ALIASES = ["e", "exit",
                        "q", "quit"]
    CMD_NEXT_ALIASES = ["n", "next"]
    CMD_RANDOM_ALIASES = ["r", "random"]
    CMD_GOTO_ALIASES = ["g", "goto",
                        "j", "jump"]

    # General variables #
    _done = False
    _unit = None

    @classmethod
    def start(cls):
        cls._unit = Cycle.get_day_by_number(1, 1)
        cls.mainloop()

    @classmethod
    def mainloop(cls):

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
                    raise KeyError("Invalid command!")

            except KeyError as ke:
                CLIOutput.warning(str(ke))
                continue

            except ValueError as ve:
                CLIOutput.warning(str(ve))
                continue

            except IndexError as ie:
                CLIOutput.warning(str(ie))
                continue

        else:  # executes after while condition becomes false #
            pass

        # end of the Main Program Loop #

    # User Interface functions --------------------------------------- #

    @classmethod
    def cmd_exit(cls):

        cls._done = True

    @classmethod
    def cmd_help(cls):

        collection = [
            ["start",          "Start currently selected unit."],
            ["begin",          "Same as 'start'."],
            ["exit",           "Exit the program."],
            ["quit",           "Same as 'exit'."],
            ["q",              "Same as 'exit'."],
            ["next",           "Go to an start next unit."],
            ["goto WEEK",      "Change selected unit to the first day in WEEK."],
            ["goto WEEK UNIT", "Change selected unit to UNIT in WEEK."],
            ["jump",           "Same as 'goto'."],
            ["help",           "Display this help text."]
        ]

        CLIOutput.empty_line(1)
        CLIOutput.center("Glossanea help")
        CLIOutput.value_pair_list(collection, CLIOutput.FORMAT_WIDE, CLIOutput.SPACING_APART)

    @classmethod
    def cmd_start(cls):

        CLIDay.start(cls._unit)

    @classmethod
    def cmd_next(cls):

        week_no = cls._unit.get_week_no()
        unit_no = cls._unit.get_unit_no()

        try:
            prev_unit = cls._unit
            cls._unit = Cycle.get_next_unit(week_no, unit_no)
            del prev_unit
        except IndexError:
            raise

        # TODO: temporary skip of weekly review until implemented ˇˇˇˇ #
        week_no = cls._unit.get_week_no()
        unit_no = cls._unit.get_unit_no()

        if cls._unit.get_unit_type() == Unit.TYPE_WEEKLY_REVIEW:
            try:
                prev_unit = cls._unit
                cls._unit = Cycle.get_next_unit(week_no, unit_no)
                del prev_unit
            except IndexError:
                raise
        # END TODO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ #

        cls.cmd_start()

    @classmethod
    def cmd_goto(cls, arguments):

        arg_count = len(arguments)

        if arg_count == 1:
            try:
                week_no = int(arguments[0])
                prev_unit = cls._unit
                cls._unit = Cycle.get_first_day_by_week(week_no)
                del prev_unit
            except ValueError:
                raise

        elif arg_count == 2:
            try:
                week_no = int(arguments[0])
                day_no = int(arguments[1])
                prev_unit = cls._unit
                cls._unit = Cycle.get_day_by_number(week_no, day_no)
                del prev_unit
            except ValueError:
                raise

        else:
            raise ValueError("Wrong number of arguments!")

    @classmethod
    def cmd_random(cls, arguments):

        arg_count = len(arguments)
        prev_unit = cls._unit

        while True:
            # TODO: remove loop after Weekly Reviews are implemented

            try:
                if arg_count == 0:
                    cls._unit = Cycle.get_random_unit(None)
                else:
                    cls._unit = Cycle.get_random_unit(" ".join(arguments))
            except ValueError:
                raise

            if cls._unit.get_unit_type() == Unit.TYPE_DAY:
                break

        del prev_unit

        cls.cmd_start()

    # general displays ----------------------------------------------- #

    @classmethod
    def display_introduction(cls):
        CLIOutput.empty_line(1)
        CLIOutput.center("")  # TODO from migration: load from data
        CLIOutput.empty_line(1)

    # other ---------------------------------------------------------- #

    @classmethod
    def build_command_prompt(cls):

        week = cls._unit.get_week_no()
        day = cls._unit.get_unit_no()

        if day == Unit.WEEKLY_REVIEW_INDEX:
            day = "WR"

        return "Glossanea {0}/{1} $ ".format(week, day)
