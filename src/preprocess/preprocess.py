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

def detect_redundency_nominal(df, attr_list):
    nominal_columns = [
        attr.variable for attr in attr_list if attr.variable in df.columns]

    nominal_df = df[nominal_columns]
    correlations = nominal_df.corr()
    fig = plt.figure(figsize=(150, 150))
    ax = fig.add_subplot(111)
    cax = ax.matshow(correlations, vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0, len(nominal_df.columns), 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    plt.savefig('nominal_correlation.png')


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

    nominal_attr_list = []
    for attr in attr_list:
        if (attr.level == dataConst.AttrbuteLevel.NOMINAL
            and attr.variable not in dataConst.ID_FIELDS):
            nominal_attr_list.append(attr)
    
    detect_redundency_nominal(filtered_df, nominal_attr_list)

    validated_df = pd.concat([df[dataConst.ID_FIELDS], filtered_df], axis=1)
    validated_df.to_excel("valid.xlsx")


if __name__ == "__main__":
    main()
