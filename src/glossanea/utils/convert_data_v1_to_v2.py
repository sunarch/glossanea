#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import json

from glossanea.structure.unit import Unit
from glossanea.utils.data_file_loader import DataFileLoader


def convert_all():
    """Convert all data files"""

    for day_tuple in Unit.generator_day_tuples():
        file_path = Unit.build_path_day(day_tuple[0], day_tuple[1])
        print('')
        print('=>', 'Upgrading', f'{file_path + "  ":=<59}')
        convert_one(file_path)
    

def convert_one(arg_data_file_path):
    """Convert one data file"""

    data = None

    try:
        data = DataFileLoader.load(arg_data_file_path)
    except FileNotFoundError:
        raise RuntimeError('Given file does not exist.')

    try:
        if data['template'] == DataFileLoader.VERSIONS_DAY[1]:
            raise RuntimeError('Data file has already been converted to version "v2_day".')
        elif data['template'] != DataFileLoader.VERSIONS_DAY[0]:
            raise RuntimeError('Data file version is invalid.')
    except KeyError:
        print('Data file has no template identifier. Assuming version "v1_day".')

    file_path = DataFileLoader.build_full_path(arg_data_file_path)

    backup_file_path = ''.join([file_path.split('.json')[0], '_old_v1.json'])

    os.rename(file_path, backup_file_path)

    filled_template = None

    try:
        filled_template = _fill_template_v2_with_data_v1(data)
    except KeyError as ke:
        print(f'Content for {ke} is not present, will be left empty in the upgrade.')
        print(filled_template)

    with open(file_path, mode='wt', encoding='utf-8', newline='\r\n') as new_file:
        new_file.write(filled_template)


def _fill_template_v2_with_data_v1(arg_data):
    """Fill a v2 template with v1 data"""

    v2_item_count = 70

    template_path = DataFileLoader.build_full_path('templates/template_v2_day_formattable.json')

    template = None

    with open(template_path, mode='rt', encoding='utf-8', newline=None) as template_file:
        template = template_file.read()

    format_content = _build_format_content_list(arg_data, template)

    if len(format_content) != v2_item_count:
        raise RuntimeError(f'Data item count is {len(format_content)} instead of {v2_item_count}!')

    return template.format(*format_content)


def _build_format_content_list(arg_data, arg_template):
    """Build values list for template formatting"""

    definitions_available = True

    content = list()

    # TITLE ---------------------------------------------------------- #

    # 0: title
    content.append(json.dumps(arg_data['content']['title']))

    # NEW WORDS ------------------------------------------------------ #

    #  1: new_words > (1) > regular
    content.append(json.dumps(arg_data['content']['words'][0]))

    #  2: new_words > (1) > phonetic
    content.append(json.dumps(''))

    #  3: new_words > (1) > search
    content.append(json.dumps(''))

    #  4: new_words > (2) > regular
    content.append(json.dumps(arg_data['content']['words'][1]))

    #  5: new_words > (2) > phonetic
    content.append(json.dumps(''))

    #  6: new_words > (2) > search
    content.append(json.dumps(''))

    #  7: new_words > (3) > regular
    content.append(json.dumps(arg_data['content']['words'][2]))

    #  8: new_words > (3) > phonetic
    content.append(json.dumps(''))

    #  9: new_words > (3) > search
    content.append(json.dumps(''))

    # 10: new_words > (4) > regular
    content.append(json.dumps(arg_data['content']['words'][3]))

    # 11: new_words > (4) > phonetic
    content.append(json.dumps(''))

    # 12: new_words > (4) > search
    content.append(json.dumps(''))

    # 13: new_words > (5) > regular
    content.append(json.dumps(arg_data['content']['words'][4]))

    # 14: new_words > (5) > phonetic
    content.append(json.dumps(''))

    # 15: new_words > (5) > search
    content.append(json.dumps(''))

    # INTRO TEXT ----------------------------------------------------- #

    # 16: intro_text
    content.append(json.dumps(arg_data['content']['text']))

    # SAMPLE SENTENCES ----------------------------------------------- #

    # 17: sample_sentences > prompt
    content.append(json.dumps(''))

    # 18: sample_sentences > sentences > (1) > beginning
    content.append(json.dumps(arg_data['task_1_gaps']['data'][0]['question_before']))

    # 19: sample_sentences > sentences > (1) > answer
    content.append(json.dumps(arg_data['task_1_gaps']['data'][0]['answer']))

    # 20: sample_sentences > sentences > (1) > end
    content.append(json.dumps(arg_data['task_1_gaps']['data'][0]['question_after']))

    # 21: sample_sentences > sentences > (2) > beginning
    content.append(json.dumps(arg_data['task_1_gaps']['data'][1]['question_before']))

    # 22: sample_sentences > sentences > (2) > answer
    content.append(json.dumps(arg_data['task_1_gaps']['data'][1]['answer']))

    # 23: sample_sentences > sentences > (2) > end
    content.append(json.dumps(arg_data['task_1_gaps']['data'][1]['question_after']))

    # 24: sample_sentences > sentences > (3) > beginning
    content.append(json.dumps(arg_data['task_1_gaps']['data'][2]['question_before']))

    # 25: sample_sentences > sentences > (3) > answer
    content.append(json.dumps(arg_data['task_1_gaps']['data'][2]['answer']))

    # 26: sample_sentences > sentences > (3) > end
    content.append(json.dumps(arg_data['task_1_gaps']['data'][2]['question_after']))

    # 27: sample_sentences > sentences > (4) > beginning
    content.append(json.dumps(arg_data['task_1_gaps']['data'][3]['question_before']))

    # 28: sample_sentences > sentences > (4) > answer
    content.append(json.dumps(arg_data['task_1_gaps']['data'][3]['answer']))

    # 29: sample_sentences > sentences > (4) > end
    content.append(json.dumps(arg_data['task_1_gaps']['data'][3]['question_after']))

    # 30: sample_sentences > sentences > (5) > beginning
    content.append(json.dumps(arg_data['task_1_gaps']['data'][4]['question_before']))

    # 31: sample_sentences > sentences > (5) > answer
    content.append(json.dumps(arg_data['task_1_gaps']['data'][4]['answer']))

    # 32: sample_sentences > sentences > (5) > end
    content.append(json.dumps(arg_data['task_1_gaps']['data'][4]['question_after']))

    # 33: sample_sentences > sentences > (6) > beginning
    content.append(json.dumps(arg_data['task_1_gaps']['data'][5]['question_before']))

    # 34: sample_sentences > sentences > (6) > answer
    content.append(json.dumps(arg_data['task_1_gaps']['data'][5]['answer']))

    # 35: sample_sentences > sentences > (6) > end
    content.append(json.dumps(arg_data['task_1_gaps']['data'][5]['question_after']))

    # DEFINITIONS ---------------------------------------------------- #

    try:
        test_availability_1 = arg_data['task_2_definitions']['definitions']
        test_availability_2 = arg_data['task_2_definitions']['words']
    except KeyError:
        definitions_available = False

    if definitions_available:
        # 36: definitions > prompt
        content.append(json.dumps(''))

        # 37: definitions > definitions > (1) > text
        content.append(json.dumps(arg_data['task_2_definitions']['definitions'][0]))

        # 38: definitions > definitions > (2) > text
        content.append(json.dumps(arg_data['task_2_definitions']['definitions'][1]))

        # 39: definitions > definitions > (3) > text
        content.append(json.dumps(arg_data['task_2_definitions']['definitions'][2]))

        # 40: definitions > definitions > (4) > text
        content.append(json.dumps(arg_data['task_2_definitions']['definitions'][3]))

        # 41: definitions > definitions > (5) > text
        content.append(json.dumps(arg_data['task_2_definitions']['definitions'][4]))

        # 42: definitions > words > (a) > text
        content.append(json.dumps(arg_data['task_2_definitions']['words'][0]))

        # 43: definitions > words > (b) > text
        content.append(json.dumps(arg_data['task_2_definitions']['words'][1]))

        # 44: definitions > words > (c) > text
        content.append(json.dumps(arg_data['task_2_definitions']['words'][2]))

        # 45: definitions > words > (d) > text
        content.append(json.dumps(arg_data['task_2_definitions']['words'][3]))

        # 46: definitions > words > (e) > text
        content.append(json.dumps(arg_data['task_2_definitions']['words'][4]))

    else:
        # 36: definitions > prompt
        content.append(json.dumps(''))

        # 37: definitions > definitions > (1) > text
        content.append(json.dumps(''))

        # 38: definitions > definitions > (2) > text
        content.append(json.dumps(''))

        # 39: definitions > definitions > (3) > text
        content.append(json.dumps(''))

        # 40: definitions > definitions > (4) > text
        content.append(json.dumps(''))

        # 41: definitions > definitions > (5) > text
        content.append(json.dumps(''))

        # 42: definitions > words > (a) > text
        content.append(json.dumps(''))

        # 43: definitions > words > (b) > text
        content.append(json.dumps(''))

        # 44: definitions > words > (c) > text
        content.append(json.dumps(''))

        # 45: definitions > words > (d) > text
        content.append(json.dumps(''))

        # 46: definitions > words > (e) > text
        content.append(json.dumps(''))

    # unconditional part of definitions:

    # 47: definitions > answers > (1) > (2)
    content.append(json.dumps(''))

    # 48: definitions > answers > (2) > (2)
    content.append(json.dumps(''))

    # 49: definitions > answers > (3) > (2)
    content.append(json.dumps(''))

    # 50: definitions > answers > (4) > (2)
    content.append(json.dumps(''))

    # 51: definitions > answers > (5) > (2)
    content.append(json.dumps(''))

    # MATCHING ------------------------------------------------------- #

    # 52: matching > name
    content.append(json.dumps(''))

    # 53: matching > prompt
    content.append(json.dumps(''))

    # 54: matching > sentences > (1) > text
    content.append(json.dumps(''))

    # 55: matching > sentences > (2) > text
    content.append(json.dumps(''))

    # 56: matching > sentences > (3) > text
    content.append(json.dumps(''))

    # 57: matching > sentences > (4) > text
    content.append(json.dumps(''))

    # 58: matching > sentences > (5) > text
    content.append(json.dumps(''))

    # 59: matching > words > (a) > text
    content.append(json.dumps(''))

    # 60: matching > words > (b) > text
    content.append(json.dumps(''))

    # 61: matching > words > (c) > text
    content.append(json.dumps(''))

    # 62: matching > words > (d) > text
    content.append(json.dumps(''))

    # 63: matching > words > (e) > text
    content.append(json.dumps(''))

    # 64: matching > answers > (1) > (2)
    content.append(json.dumps(''))

    # 65: matching > answers > (2) > (2)
    content.append(json.dumps(''))

    # 66: matching > answers > (3) > (2)
    content.append(json.dumps(''))

    # 67: matching > answers > (4) > (2)
    content.append(json.dumps(''))

    # 68: matching > answers > (5) > (2)
    content.append(json.dumps(''))

    # OTHER ---------------------------------------------------------- #

    # 69: other_new_words > prompt
    content.append(json.dumps(''))

    return content
