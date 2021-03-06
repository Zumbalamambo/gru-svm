# Copyright 2017 Abien Fred Agarap. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""
Converts the original Kyoto University dataset
 Text files to CSV files
"""

__version__ = '0.1'
__author__ = 'Abien Fred Agarap'

import argparse
import csv
import os
from os import walk


def convert_txt_to_csv(txt_path, csv_path):
    data = []  # list to store the filenames under the subdirectories of the <path>
    csv_data = []  # list to store the converted CSV files

    for (dirpath, dirnames, filenames) in walk(txt_path):
        ''' Append to the list the filenames under the subdirectories of the <path> '''
        data.extend(os.path.join(dirpath, filename) for filename in filenames)

    # Create the <csv_path> if it does not exist
    os.makedirs(csv_path) if not os.path.exists(csv_path) else print('CSV folder exists')

    for month in range(12):
        ''' Create the subdirectories under the <csv_path> if it does not exist '''
        if next(walk(csv_path))[1].__len__() == 12:
            print('Folders exist')
            break
        print('Creating subdirectories.')
        # get the dirpath from the generator object <walk> (index 0)
        # then joins the dirpath with the month number
        os.makedirs(os.path.join(next(walk(csv_path))[0], '0' + str(month + 1) if month < 9 else str(month + 1)))

    for index in range(len(data)):
        ''' Store the processed CSV filename to <csv_data> list '''
        csv_data.append(os.path.join(csv_path, data[index].split(path)[1].replace('txt', 'csv')))

    for index in range(len(data)):
        ''' Reading the text files delimited with tab, and converts it to CSV '''
        try:
            print('Processing: {}'.format(data[index]))
            in_csv = csv.reader(open(data[index], 'r'), delimiter='\t')
            out_csv = csv.writer(open(csv_data[index], 'x'))
            out_csv.writerows(in_csv)
        except FileNotFoundError:
            print('File not found: {}'.format(data[index]))


def parse_args():
    parser = argparse.ArgumentParser(
        description='Module for converting the Kyoto University 2013 honeypot system dataset TXT to CSV')
    group = parser.add_argument_group('Arguments')
    group.add_argument('-t', '--txt_path', required=True, type=str,
                       help='path of the dataset in TXT format')
    group.add_argument('-c', '--csv_path', required=True, type=str,
                       help='path where the dataset in CSV format will be stored')
    args = vars(parser.parse_args())
    return args


if __name__ == '__main__':
    args = parse_args()

    convert_txt_to_csv(args['txt_path'], args['csv_path'])
