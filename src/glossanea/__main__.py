# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Main"""

# imports: library
from argparse import ArgumentParser, Namespace

# imports: dependencies
import libmonty_logging
import libmonty_logging.message as logging_message

# imports: project
from glossanea import version
from glossanea.cli.cli import CLI
from glossanea.files import config


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

    args: Namespace = parser.parse_args()

    if args.version:
        print(f'{version.PROGRAM_NAME} {version.__version__}')
        return

    config.check_data_dir_path()

    # start User Interface
    CLI.start()


if __name__ == '__main__':
    main()
