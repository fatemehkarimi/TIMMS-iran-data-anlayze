from matplotlib.pyplot import axis
import pandas as pd
import dataset.datasetConst as dataConst
from codebook import Codebook
from preprocess_categoral import fill_missing_value

def preprocess_nominal_attrs(df, attr_list):
    bad_nominal_labels = dataConst.ID_FIELDS

    filtered_df = df.drop(
        labels=bad_nominal_labels,
        axis=True
    )

    for attr in attr_list:
        if (
            attr.variable not in bad_nominal_labels 
            and (attr.level == dataConst.AttrbuteLevel.NOMINAL
            or attr.level == dataConst.AttrbuteLevel.ORDINAL)
        ):
            filtered_df = fill_missing_value(filtered_df, attr)

    filtered_df = pd.concat([df[bad_nominal_labels], filtered_df], axis=1)
    return filtered_df


def main():
    codebook = Codebook()
    attr_list = codebook.get_attribute_list()

    df = pd.read_excel(dataConst.data_file)
    df = preprocess_nominal_attrs(df, attr_list)
    df.to_excel("valid.xlsx")


if __name__ == "__main__":
    main()
