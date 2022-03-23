import pandas as pd
import dataset.datasetConst as dataConst
from codebook import Codebook
from preprocess_nominal import fill_missing_value

def main():
    codebook = Codebook()
    attribute_list = codebook.get_attribute_list()

    df = pd.read_excel(dataConst.data_file)

    for attr in attribute_list:
        if attr.level == dataConst.AttrbuteLevel.NOMINAL:
            fill_missing_value(df, attr)


if __name__ == "__main__":
    main()
