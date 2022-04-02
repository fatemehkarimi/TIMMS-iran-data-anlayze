import argparse
import sys
import json
import pandas as pd
import dataset.datasetConst as dataConst
import numpy as np
from scipy.stats import f_oneway
import matplotlib.pyplot as plt
from data.codebook import Codebook

def plot_correlation(correlation, filename, labels=None):
    fig = plt.figure(figsize=(10.41, 7.29))
    ax = fig.add_subplot(111)
    cax = ax.matshow(correlation, vmin=-1, vmax=1)
    fig.colorbar(cax)
    if labels:
        ticks = np.arange(0, len(labels), 1)
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.set_xticklabels(labels)
        ax.set_yticklabels(labels)
    plt.savefig(filename)


def calc_score_nominal_correlation(df, attr_list):
    col_names = [attr.variable for attr in attr_list
                    if attr.level == dataConst.AttributeLevel.NOMINAL
                    and attr.variable in df.columns
                    and attr.variable not in dataConst.ID_FIELDS]

    result = {}
    for col in col_names:
        tmp_df = df[[col, dataConst.Fields.FINAL_SCORE]]
        category_group_list = \
            tmp_df.groupby(dataConst.Fields.FINAL_SCORE)[col].apply(list)
        stat, p = f_oneway(*category_group_list)
        if p <= 0.05:
            result[col] = 1
        else:
            result[col] = 0
    return result


def calc_score_level_correlation(df, attr_list, level, corr_method):
    col_names = [attr.variable for attr in attr_list
                if attr.variable not in dataConst.ID_FIELDS
                and attr.variable in df.columns
                and attr.level == level]

    result = {}
    for col in col_names:
        tmp_df = df[[col, dataConst.Fields.FINAL_SCORE]]
        corr = tmp_df.corr(method=corr_method)
        result[col] = corr.iloc[0, 1]
    return result


def main(args):
    codebook = Codebook()
    attr_list = codebook.get_attribute_list()
    df = pd.read_excel(args.file)

    result1 = calc_score_level_correlation(
        df,
        attr_list, dataConst.AttributeLevel.SCALE,
        'spearman')

    result2 = calc_score_level_correlation(
        df, attr_list,
        dataConst.AttributeLevel.ORDINAL,
        'spearman')

    result3 = calc_score_nominal_correlation(df, attr_list)

    result = {**result1, **result2, **result3}
    with open('result.json', 'w') as f:
        json.dump(result, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='find most correlated attributes to student scores')
    args = parser.add_argument(
        '--file',
        help='data file')
    args = parser.parse_args()
    if not args.file:
        parser.print_help()
        sys.exit(1)
    main(args)