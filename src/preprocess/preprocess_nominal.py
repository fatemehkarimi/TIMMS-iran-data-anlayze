import pandas as pd
from preprocess.preprocess_level import LevelPreprocess
from preprocess.preprocess_scale import ALMOST_NULL_ATTRIBUTE_RATIO

ALMOST_NULL_ATTRIBUTE_RATIO = 0.5

class NominalPreprocess(LevelPreprocess):
    def fill_missing_value(self, df, attr):
        pd.to_numeric(df[attr.variable])

        if self.is_attr_too_null(df, attr):
            df = df.drop(labels=[attr.variable], axis=1)
            return df

        


    def is_attr_too_null(self, df, attr):
        num_null = len(
            df.loc[lambda x :
                    (x[attr.variable] > attr.get_max_range())
                        | (x[attr.variable] < attr.get_min_range())].index)

        num_null += df[attr.variable].isna().sum()
        if num_null / len(df.index) >= ALMOST_NULL_ATTRIBUTE_RATIO:
            return True
        return False
