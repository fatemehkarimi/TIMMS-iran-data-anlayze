from cProfile import label
import pandas as pd
from codebook import Codebook
import dataset.datasetConst as dataConst
from preprocess_scale import ScalePreprocess
from preprocess_ordinal import OrdinalPreprocess
from preprocess_nominal import NominalPreprocess
import matplotlib.pyplot as plt
import numpy as np

def preprocess_by_level(df, attr_list, level, preprocessor):
    for attr in attr_list:
        if attr.variable not in dataConst.ID_FIELDS:
            if attr.level == level:
                df = preprocessor.fill_missing_value(df, attr)
    return df


def visualize_correlation_scale(df, attr_list):
    scale_columns = [
        attr.variable for attr in attr_list if attr.variable in df.columns]
    scale_df = df[scale_columns]
    correlations = scale_df.corr(method='pearson')
    plot_correlation(correlations, 'scale_correlation.png', scale_columns)


def visualize_correlation_ordinal(df, attr_list):
    ordinal_columns = [
        attr.variable for attr in attr_list if attr.variable in df.columns]
    ordinal_df = df[ordinal_columns]
    correlations = ordinal_df.corr(method='spearman')
    plot_correlation(correlations, 'ordinal_correlation.png')


def plot_correlation(correlations, filename, labels=None):
    fig = plt.figure(figsize=(10.41, 7.29))
    ax = fig.add_subplot(111)
    cax = ax.matshow(correlations, vmin=-1, vmax=1)
    fig.colorbar(cax)
    if labels:
        ticks = np.arange(0, len(labels), 1)
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.set_xticklabels(labels)
        ax.set_yticklabels(labels)
    plt.savefig(filename)


def main():
    codebook = Codebook()
    attr_list = codebook.get_attribute_list()

    df = pd.read_excel(dataConst.data_file)
    filtered_df = df.drop(
        labels=dataConst.ID_FIELDS,
        axis=True
    )

    filtered_df = preprocess_by_level(
        filtered_df,
        attr_list,
        dataConst.AttrbuteLevel.ORDINAL,
        OrdinalPreprocess())

    filtered_df = preprocess_by_level(
        filtered_df,
        attr_list,
        dataConst.AttrbuteLevel.SCALE,
        ScalePreprocess())

    filtered_df = preprocess_by_level(
        filtered_df,
        attr_list,
        dataConst.AttrbuteLevel.NOMINAL,
        NominalPreprocess()
    )

    scale_attr_list = []
    ordinal_attr_list = []
    for attr in attr_list:
        if (attr.level == dataConst.AttrbuteLevel.SCALE
            and attr.variable not in dataConst.ID_FIELDS):
            scale_attr_list.append(attr)
        elif (attr.level == dataConst.AttrbuteLevel.ORDINAL
            and attr.variable not in dataConst.ID_FIELDS):
            ordinal_attr_list.append(attr)
    
    visualize_correlation_scale(filtered_df, scale_attr_list)
    visualize_correlation_ordinal(filtered_df, ordinal_attr_list)

    validated_df = pd.concat([df[dataConst.ID_FIELDS], filtered_df], axis=1)
    validated_df.to_excel("valid.xlsx")


if __name__ == "__main__":
    main()
