# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Main"""

# imports: library
from argparse import ArgumentParser
from enum import Enum

# imports: dependencies
import libmonty_logging
import libmonty_logging.message as logging_message

# imports: project
from glossanea import version
from glossanea.gui.gui import GUI
from glossanea.cli.cli import CLI
from glossanea.utils import convert_data_v1_to_v2
import glossanea.config.app as app_config


class UserInterfaceType(Enum):
    """User Interface Type"""

    CLI = 'cli'
    GUI = 'gui'
    DEFAULT = 'gui'


def main() -> None:
    """Main"""

    libmonty_logging.apply_default_console_and_file(
        version.PROGRAM_NAME,
        version.__version__
    )

    logging_message.program_header(version.PROGRAM_NAME)

    parser = ArgumentParser(prog=version.PROGRAM_NAME)

    parser.add_argument('--version',
                        help='Display version',
                        action='store_true',
                        dest='version')

    user_interface_group = parser.add_mutually_exclusive_group(required=False)
    user_interface_group.add_argument('--gui',
                                      help='[Default] Start with Graphical User Interface',
                                      action='store_const', const=UserInterfaceType.GUI,
                                      default=UserInterfaceType.DEFAULT,
                                      dest='user_interface')
    user_interface_group.add_argument('--cli',
                                      help='Start with Command Line Interface',
                                      action='store_const', const=UserInterfaceType.CLI,
                                      default=UserInterfaceType.DEFAULT,
                                      dest='user_interface')

    subparsers = parser.add_subparsers(help='Subcommands')

    parser_dev = subparsers.add_parser('dev', help='Glossanea developer options')

    parser_dev.add_argument('--convert-data-v1-to-v2',
                            help='Upgrade all data files',
                            action='store_true',
                            dest='convert_data_v1_to_v2')

    args = parser.parse_args()

    if args.version:
        print(f'{version.PROGRAM_NAME} {version.__version__}')
        return

    try:
        if args.convert_data_v1_to_v2:
            convert_data_v1_to_v2.convert_all()
            return
    except AttributeError:
        pass

    if args.user_interface == UserInterfaceType.GUI:
        ui = GUI
    elif args.user_interface == UserInterfaceType.CLI:
        ui = CLI
    else:
        raise ValueError(f'Unrecognized "user interface" argument {args.user_interface}')

    app_config.check_data_dir_path()

    # start User Interface
    ui.start()


if __name__ == '__main__':
    main()
