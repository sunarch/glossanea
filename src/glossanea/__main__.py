#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# imports: library
from argparse import ArgumentParser
import configparser
from enum import Enum
import logging
import logging.config
import pkg_resources

# imports: project
from glossanea import version
from glossanea.gui.gui import GUI
from glossanea.cli.cli import CLI
from glossanea.utils import convert_data_v1_to_v2


class UserInterfaceType(Enum):
    CLI = 'cli'
    GUI = 'gui'
    DEFAULT = 'gui'


def main() -> None:

    logger_config_name = 'data/logger.ini'

    if not pkg_resources.resource_exists(__name__, logger_config_name):
        logging.error('logger config does not exist')
        return

    logger_config = pkg_resources.resource_stream(__name__, logger_config_name)
    logger_config_str = logger_config.read().decode('UTF-8')
    logger_config_parser = configparser.ConfigParser()
    logger_config_parser.read_string(logger_config_str)
    logging.config.fileConfig(logger_config_parser)

    logging.info(version.program_name)
    logging.info('-' * len(version.program_name))

    parser = ArgumentParser(prog=version.program_name)

    parser.add_argument('--version',
                        help='Display version',
                        action='store_const', const=True, default=False,
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
                            action='store_const', const=True, default=False,
                            dest='convert_data_v1_to_v2')

    args = parser.parse_args()

    if args.version:
        print(f'{version.program_name} {version.__version__}')
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

    ui.start()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------- #
