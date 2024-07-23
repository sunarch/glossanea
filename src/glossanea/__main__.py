# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Main"""

# imports: library
from argparse import ArgumentParser

# imports: dependencies
import libmonty_logging
import libmonty_logging.message as logging_message

# imports: project
from glossanea import version
from glossanea.cli.cli import CLI
from glossanea.utils import convert_data_v1_to_v2
import glossanea.config.app as app_config


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

    ui = CLI

    app_config.check_data_dir_path()

    # start User Interface
    ui.start()


if __name__ == '__main__':
    main()
