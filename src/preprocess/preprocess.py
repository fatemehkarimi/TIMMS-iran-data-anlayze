from warnings import filters
import pandas as pd
import dataset.datasetConst as dataConst
from data.codebook import Codebook
from preprocess_scale import ScalePreprocess
from preprocess_ordinal import OrdinalPreprocess
from preprocess_nominal import NominalPreprocess

import matplotlib.pyplot as plt
from scipy.stats import f_oneway


def fill_null_values(df, attr_list, level, preprocessor):
    level_attrs = [attr for attr in attr_list 
        if (attr.level == level
            and attr.variable not in dataConst.ID_FIELDS)]

    df = preprocessor.fill_missing_value(df, level_attrs)
    return df


def visualize_correlation(df, attr_list, level, preprocessor):
    level_attrs = [attr for attr in attr_list 
        if (attr.level == level
            and attr.variable not in dataConst.ID_FIELDS)]
    
    preprocessor.visualize_correlation(df, level_attrs)


def visualize_nominal_scale_correlatin(df, attr_list):
    nominal_attr = [attr for attr in attr_list
                    if attr.level == dataConst.AttributeLevel.NOMINAL
                        and attr not in dataConst.ID_FIELDS]
    scale_attr = [attr for attr in attr_list
                    if attr.level == dataConst.AttributeLevel.SCALE
                        and attr not in dataConst.ID_FIELDS]
    nom_colname = [attr.variable for attr in nominal_attr
                    if attr.variable in df.columns]
    scale_colname = [attr.variable for attr in scale_attr
                    if attr.variable in df.columns]

    corr_matrix = []
    for i in nom_colname:
        result = []
        for j in scale_colname:
            tmp_df = df[[i, j]]
            category_group_list = tmp_df.groupby(i)[j].apply(list)
            stat, p = f_oneway(*category_group_list)
            if p <= 0.05:
                result.append(1)
            else:
                result.append(0)
        corr_matrix.append(result)

    fig = plt.figure(figsize=(10.41, 7.29))
    ax = fig.add_subplot(111)
    cax = ax.matshow(corr_matrix, vmin=-1, vmax=1)
    fig.colorbar(cax)
    plt.savefig("nominal_scale_correlation.png")


def filter_correlated_attributes(df, attr_list, level, preprocessor):
    level_attrs = [attr for attr in attr_list 
        if (attr.level == level
            and attr.variable not in dataConst.ID_FIELDS)]

    return preprocessor.filter_correlated_columns(df, level_attrs)


def filter_correlated_nominal_scale_attributes(df, attr_list):
    nominal_attr = [attr for attr in attr_list
                    if attr.level == dataConst.AttributeLevel.NOMINAL
                        and attr not in dataConst.ID_FIELDS]
    scale_attr = [attr for attr in attr_list
                    if attr.level == dataConst.AttributeLevel.SCALE
                        and attr not in dataConst.ID_FIELDS]
    nom_colname = [attr.variable for attr in nominal_attr
                    if attr.variable in df.columns]
    scale_colname = [attr.variable for attr in scale_attr
                    if attr.variable in df.columns]

    redundent_attrs = set()
    for i in nom_colname:
        for j in scale_colname:
            tmp_df = df[[i, j]]
            category_group_list = tmp_df.groupby(i)[j].apply(list)
            stat, p = f_oneway(*category_group_list)
            if p <= 0.05:
                redundent_attrs.add(i)
    return df.drop(labels=list(redundent_attrs), axis=1)


def replace_final_score_values(df):
    for score_field in dataConst.SCORE_FIELDS:
        df.loc[lambda x : x[score_field] == 'A', score_field] = 5
        df.loc[lambda x : x[score_field] == 'B', score_field] = 4
        df.loc[lambda x : x[score_field] == 'C', score_field] = 3
        df.loc[lambda x : x[score_field] == 'D', score_field] = 2
        df.loc[lambda x : x[score_field] == 'E', score_field] = 1
    return df


def main():
    codebook = Codebook()
    attr_list = codebook.get_attribute_list()

    df = pd.read_excel(dataConst.data_file)
    filtered_df = df.drop(
        labels=dataConst.ID_FIELDS,
        axis=True
    )

    scale_preprocess = ScalePreprocess()
    nominal_preprocess = NominalPreprocess()
    ordinal_preprocess = OrdinalPreprocess()

    filtered_df = fill_null_values(
        filtered_df,
        attr_list,
        dataConst.AttributeLevel.ORDINAL,
        ordinal_preprocess)

    filtered_df = fill_null_values(
        filtered_df,
        attr_list,
        dataConst.AttributeLevel.SCALE,
        scale_preprocess)

    filtered_df = fill_null_values(
        filtered_df,
        attr_list,
        dataConst.AttributeLevel.NOMINAL,
        nominal_preprocess)

    filtered_df = filter_correlated_attributes(
        filtered_df,
        attr_list,
        dataConst.AttributeLevel.ORDINAL,
        ordinal_preprocess)

    filtered_df = filter_correlated_attributes(
        filtered_df,
        attr_list,
        dataConst.AttributeLevel.SCALE,
        scale_preprocess)

    # visualize_correlation(
        # df, attr_list, dataConst.AttributeLevel.NOMINAL, nominal_preprocess)

    # filtered_df = filter_correlated_attributes(
    #     filtered_df,
    #     attr_list,
    #     dataConst.AttributeLevel.NOMINAL,
    #     nominal_preprocess)

    # visualize_nominal_scale_correlatin(filtered_df, attr_list)
    # filtered_df = filter_correlated_nominal_scale_attributes(filtered_df, attr_list)

    filtered_df = replace_final_score_values(filtered_df)

    validated_df = pd.concat([df[dataConst.ID_FIELDS], filtered_df], axis=1)
    validated_df.to_excel("valid.xlsx")


if __name__ == "__main__":
    main()
