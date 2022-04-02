from warnings import filters
import pandas as pd
from codebook import Codebook
import dataset.datasetConst as dataConst
from preprocess_scale import ScalePreprocess
from preprocess_ordinal import OrdinalPreprocess
from preprocess_nominal import NominalPreprocess

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

def filter_correlated_attributes(df, attr_list, level, preprocessor):
    level_attrs = [attr for attr in attr_list 
        if (attr.level == level
            and attr.variable not in dataConst.ID_FIELDS)]

    return preprocessor.filter_correlated_columns(df, level_attrs)


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


    # visualize_correlation(
    #     filtered_df, attr_list,
    #     dataConst.AttributeLevel.SCALE,
    #     scale_preprocess)

    # visualize_correlation(
    #     filtered_df,
    #     attr_list,
    #     dataConst.AttributeLevel.ORDINAL,
    #     ordinal_preprocess)

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

    validated_df = pd.concat([df[dataConst.ID_FIELDS], filtered_df], axis=1)
    validated_df.to_excel("valid.xlsx")


if __name__ == "__main__":
    main()
