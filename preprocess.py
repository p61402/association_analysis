#!/usr/bin/env python
# coding: utf-8

import pandas as pd


def generate_dataframe(file_name='data.txt', num_of_items=10, num_of_transactions=101):
    with open(file_name, 'r') as f:
        raw_data = f.readlines()

    df = pd.DataFrame(0, index=range(1, num_of_transactions),
                      columns=[i for i in range(num_of_items)])

    for line in raw_data:
        a = line.split()
        df.at[int(a[0]), int(a[2])] = 1

    return df
