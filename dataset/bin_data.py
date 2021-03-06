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

"""Bins continuous data into 10 evenly-spaced intervals"""
import argparse
import numpy as np
import os
import pandas as pd
import standardize_data as sd

__version__ = '0.1'
__author__ = 'Abien Fred Agarap'

column_names = sd.col_names
columns_to_save = list(column_names)
columns_to_save.remove('dst_ip_add')
columns_to_save.remove('src_ip_add')
cols_to_std = sd.cols_to_std
cols_to_std.append('service')
cols_to_std.append('flag')


def bin_data(path, write_path, num_chunks, binning):
    """Method for binning the dataset"""

    # get the list of files found in PATH
    files = sd.list_files(path=path)

    df = pd.DataFrame()

    for file in files:
        # append the data from CSV files to the dataframe
        df = df.append(pd.read_csv(filepath_or_buffer=file, names=column_names))
        print('appending : {}'.format(file))

    # remove dst_ip_add and src_ip_add features
    df = df.drop(labels=['dst_ip_add', 'src_ip_add'], axis=1)

    for index in range(len(cols_to_std)):
        if int(binning) == 0:
            # bucket binning
            bins = np.linspace(df[cols_to_std[index]].min(), df[cols_to_std[index]].max(), 10)
            df[cols_to_std[index]] = np.digitize(df[cols_to_std[index]], bins, right=True)
            print('min : {}, max : {}'.format(df[cols_to_std[index]].min(), df[cols_to_std[index]].max()))

        if int(binning) == 1:
            # decile binning
            df[cols_to_std[index]] = pd.qcut(df[cols_to_std[index]], 10, labels=False, duplicates='drop')
            print('min : {}, max : {}'.format(df[cols_to_std[index]].min(), df[cols_to_std[index]].max()))

    for id, df_i in enumerate(np.array_split(df, num_chunks)):
        # split and save the dataframe to CSV files
        df_i.to_csv(path_or_buf=os.path.join(write_path, '{id}.csv'.format(id=id)), columns=columns_to_save,
                    header=None, index=False)
        print('Saving CSV file : {path}'.format(path=os.path.join(write_path, '{id}'.format(id=id))))


def parse_args():
    parser = argparse.ArgumentParser(
        description='Module for binning the Kyoto University 2013 dataset')
    group = parser.add_argument_group('Arguments')
    group.add_argument('-d', '--dataset', required=True, type=str,
                       help='path of the dataset to be binned')
    group.add_argument('-w', '--write_path', required=True, type=str,
                       help='path where the binned dataset will be stored')
    group.add_argument('-n', '--num_chunks', required=True, type=int,
                       help='number of chunks of CSV files to save')
    group.add_argument('-b', '--binning', action='store',
                       help='set to 0 for bucket binning; set 1 for decile binning')
    args = vars(parser.parse_args())
    return args


if __name__ == '__main__':
    # parse arguments
    args = parse_args()

    # main method
    bin_data(args['dataset'], args['write_path'], args['num_chunks'], args['binning'])
