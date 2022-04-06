from dataclasses import dataclass
import sys
import json
import argparse
import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2, f_classif
from data.codebook import Codebook
import dataset.datasetConst as dataConst


def find_top_categorical_features(df, attr_list, target):
    categorical_colnames = [attr.variable for attr in attr_list
                            if attr.variable in df.columns
                                and (attr.level == dataConst.AttributeLevel.NOMINAL
                                or attr.level == dataConst.AttributeLevel.ORDINAL)]
    x = df[categorical_colnames]
    y = df[target]
    selector = SelectKBest(chi2, k=len(categorical_colnames) // 3)
    x_new = selector.fit_transform(x, y)
    cols = selector.get_support(indices=True)
    top_categorical_features = x.iloc[:, cols]
    top_attributes = []
    for attr_name in top_categorical_features.columns:
        top_attributes.append(attr_name)
    return top_attributes


def find_top_scale_features(df, attr_list, target):
    scale_colnames = [attr.variable for attr in attr_list
                        if attr.variable in df.columns
                            and (attr.level == dataConst.AttributeLevel.SCALE)]
    x = df[scale_colnames]
    y = df[target]
    selector = SelectKBest(f_classif, k=len(scale_colnames) // 3)
    x_new = selector.fit_transform(x, y)
    cols = selector.get_support(indices=True)
    top_scale_features = x.iloc[:, cols]
    top_attributes = []
    for attr_name in top_scale_features.columns:
        top_attributes.append(attr_name)
    return top_attributes


def write_as_json(object, filename):
    with open(filename, 'w') as f:
        json.dump(object, f, indent=4)

def main(args):
    codebook = Codebook()
    attr_list = codebook.get_attribute_list()
    df = pd.read_excel(args.file)
    df = df.drop(labels=dataConst.ID_FIELDS, axis=1)

    top_categorical = find_top_categorical_features(df, attr_list, args.target)
    top_scale = find_top_scale_features(df, attr_list, args.target)

    result = {
        "categorical": top_categorical,
        "scale": top_scale
    }

    write_as_json(result, args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='find most correlated attributes to student scores')
    args = parser.add_argument(
        '--file',
        help='data file')

    args = parser.add_argument(
        '--output',
        help='output file'
    )

    args = parser.add_argument(
        '--target',
        help='target attribute to find correlation with'
    )
    args = parser.parse_args()
    if not args.file or not args.output or not args.target:
        parser.print_help()
        sys.exit(1)
    main(args)