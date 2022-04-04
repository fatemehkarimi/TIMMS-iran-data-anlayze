import sys
import json
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import f_oneway
from scipy.stats import chi2_contingency
from data.codebook import Codebook
import dataset.datasetConst as dataConst

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


def calc_chi_square(col1, col2):
    contingency = pd.crosstab(col1, col2)
    stat, p, dof, expected = chi2_contingency(contingency)
    return p <= 0.05


def filter_correlated_attributes(correlations):
    result = {}
    for variable, corr in correlations.items():
        if abs(corr) >= 0.2:
            result[variable] = corr
    return result


def write_as_json(object, filename):
    with open(filename, 'w') as f:
        json.dump(object, f, indent=4)


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

    result3 = calc_score_level_correlation(
        df, attr_list,
        dataConst.AttributeLevel.NOMINAL,
        corr_method=calc_chi_square)

    result = {**result1, **result2, **result3}
    write_as_json(result, "result.json")
    write_as_json(
        filter_correlated_attributes(result),
        "correlated_attributes.json")


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