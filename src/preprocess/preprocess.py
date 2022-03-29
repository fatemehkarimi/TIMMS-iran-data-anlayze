from matplotlib.pyplot import axis
import pandas as pd
import dataset.datasetConst as dataConst
from codebook import Codebook
import preprocess_ordinal as process_cat
import preprocess_scale as process_scale

def preprocess_ordinal_attrs(df, attr_list):
    for attr in attr_list:
        if attr.variable not in dataConst.ID_FIELDS:
            if attr.level == dataConst.AttrbuteLevel.ORDINAL:
                df = process_cat.fill_missing_value(df, attr)
    return df


def preprocess_scale_attrs(df, attr_list):
    for attr in attr_list:
        if attr.variable not in dataConst.ID_FIELDS:
            if attr.level == dataConst.AttrbuteLevel.SCALE:
                df = process_scale.fill_missing_value(df, attr)
    return df


def main():
    codebook = Codebook()
    attr_list = codebook.get_attribute_list()

    df = pd.read_excel(dataConst.data_file)
    filtered_df = df.drop(
        labels=dataConst.ID_FIELDS,
        axis=True
    )
    filtered_df = preprocess_ordinal_attrs(filtered_df, attr_list)
    filtered_df = preprocess_scale_attrs(filtered_df, attr_list)

    validated_df = pd.concat([df[dataConst.ID_FIELDS], filtered_df], axis=1)
    validated_df.to_excel("valid.xlsx")


if __name__ == "__main__":
    main()
