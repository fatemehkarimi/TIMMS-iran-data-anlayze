from attr import attr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import dataset.datasetConst as dataConst
from data.codebook import Codebook


def main():
    codebook = Codebook()
    df = pd.read_excel('./dataset/valid.xlsx')
    df = df.drop(labels=dataConst.ID_FIELDS, axis=1)

    attr_list = codebook.get_attribute_list()
    attr_colnames = [attr.variable for attr in attr_list
                        if attr.variable in df.columns
                            and attr.level in [
                                dataConst.AttributeLevel.SCALE,
                                dataConst.AttributeLevel.ORDINAL,
                                dataConst.AttributeLevel.NOMINAL]]
        
    x = df[attr_colnames].to_numpy().reshape((-1, len(attr_colnames)))
    y = df['finalscore'].to_numpy()

    x_train, x_test, y_train, y_test = \
        train_test_split(x, y, test_size=0.2, random_state=0)

    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)

    model = LogisticRegression(
        solver='liblinear',
        C=0.05,
        multi_class='ovr',
        random_state=0
    ).fit(x_train, y_train)

    x_test = scaler.transform(x_test)
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