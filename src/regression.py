from attr import attr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import dataset.datasetConst as dataConst
from data.codebook import Codebook


def normalize_categorical(df, attr_list):
    col_names = [attr.variable for attr in attr_list]
    input = df[col_names].to_numpy().reshape((-1, len(col_names)))
    scaler = OneHotEncoder()
    transformed = scaler.fit_transform(input)
    return transformed.toarray()


def main():
    codebook = Codebook()
    df = pd.read_excel('./dataset/valid.xlsx')
    # df = df.drop(labels=dataConst.ID_FIELDS, axis=1)

    attr_list = codebook.get_attribute_list()
    attr_colnames = [attr.variable for attr in attr_list
                        if attr.variable in df.columns
                            and attr.level in [
                                dataConst.AttributeLevel.SCALE,
                                dataConst.AttributeLevel.ORDINAL,
                                dataConst.AttributeLevel.NOMINAL]]

    nominal_attr_list = [attr for attr in attr_list
                            if attr.variable in df.columns
                                and attr.level == dataConst.AttributeLevel.NOMINAL]

    ordinal_attr_list = [attr for attr in attr_list
                            if attr.variable in df.columns
                                and attr.level == dataConst.AttributeLevel.ORDINAL]

    scale_col_names = [attr.variable for attr in attr_list
                            if attr.variable in df.columns
                                and attr.level == dataConst.AttributeLevel.SCALE]
    
    x_categorical = normalize_categorical(
        df, nominal_attr_list + ordinal_attr_list)

    x_scale = df[scale_col_names].to_numpy().reshape((-1, len(scale_col_names)))
    scaler = MinMaxScaler()
    x_scale = scaler.fit_transform(x_scale)

    x = np.concatenate((x_categorical, x_scale), axis=1)
    y = df['finalscore'].to_numpy()

    x_train, x_test, y_train, y_test = \
        train_test_split(x, y, test_size=0.1, random_state=0)
    
    # x_train = x
    # y_train = y
    # x_test = x
    # y_test = y

    # scaler = StandardScaler()

    model = LogisticRegression(
        solver='liblinear',
        C=0.05,
        multi_class='ovr',
        random_state=0
    ).fit(x_train, y_train)

    # x_test = scaler.transform(x_test)
    y_pred = model.predict(x_test)

    print(model.score(x_train, y_train))
    print(model.score(x_test, y_test))

    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(8, 8))

    ax.imshow(cm)
    ax.grid(False)
    ax.set_xlabel('Predicted outputs', fontsize=12, color='black')
    ax.set_ylabel('Actual outputs', fontsize=12, color='black')
    ax.xaxis.set(ticks=range(len(model.classes_)))
    ax.yaxis.set(ticks=range(len(model.classes_)))
    for i in range(len(model.classes_)):
        for j in range(len(model.classes_)):
            ax.text(j, i, cm[i, j], ha='center', va='center', color='white')
    plt.savefig('result.png')
    




if __name__  == "__main__":
    main()