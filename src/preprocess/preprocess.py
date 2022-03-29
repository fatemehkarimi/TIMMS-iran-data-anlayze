import pandas as pd
from codebook import Codebook
from preprocess_scale import ScalePreprocess
from preprocess_ordinal import OrdinalPreprocess
import dataset.datasetConst as dataConst


def preprocess_by_level(df, attr_list, level, preprocessor):
    for attr in attr_list:
        if attr.variable not in dataConst.ID_FIELDS:
            if attr.level == level:
                df = preprocessor.fill_missing_value(df, attr)
    return df


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

    validated_df = pd.concat([df[dataConst.ID_FIELDS], filtered_df], axis=1)
    validated_df.to_excel("valid.xlsx")


if __name__ == "__main__":
    main()
