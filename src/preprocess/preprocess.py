from matplotlib.pyplot import axis
import pandas as pd
import dataset.datasetConst as dataConst
from codebook import Codebook
from preprocess_nominal import fill_missing_value

def main():
    codebook = Codebook()
    attribute_list = codebook.get_attribute_list()

    df = pd.read_excel(dataConst.data_file)

    bad_nominal_labels = ['IDCNTRY', 'IDBOOK', 'IDSCHOOL', 'IDCLASS', 'IDSTUD']

    filtered_df = df.drop(
        labels=bad_nominal_labels,
        axis=True
    )

    for attr in attribute_list:
        if attr.level == dataConst.AttrbuteLevel.NOMINAL \
            and attr.variable not in bad_nominal_labels:
            fill_missing_value(filtered_df, attr)


if __name__ == "__main__":
    main()
