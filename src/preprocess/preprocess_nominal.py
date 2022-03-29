import numpy as np
import pandas as pd
from preprocess_level import LevelPreprocess
from preprocess_scale import ALMOST_NULL_ATTRIBUTE_RATIO

ALMOST_NULL_ATTRIBUTE_RATIO = 0.5

class NominalPreprocess(LevelPreprocess):
    def fill_missing_value(self, df, attr):
        if attr.variable not in df.columns:
            self.log_key_not_exist(attr)
            return df

        pd.to_numeric(df[attr.variable])

        self.replace_out_range_values(df, attr, np.nan)
        if self.is_attr_too_null(df, attr):
            df = df.drop(labels=[attr.variable], axis=1)
            return df

        mod = self.get_mod(df, attr)
        df[attr.variable] = df[attr.variable].fillna(mod)
        return df

    def replace_out_range_values(self, df, attr, value):
        df.loc[lambda x :
                    (x[attr.variable] > attr.get_max_range())
                        | (x[attr.variable] < attr.get_min_range()),
                attr.variable] = value

    def is_attr_too_null(self, df, attr):
        num_null = df[attr.variable].isna().sum()
        if num_null / len(df.index) >= ALMOST_NULL_ATTRIBUTE_RATIO:
            return True
        return False

    def get_mod(self, df, attr):
        max_count = 0
        max_value = 0

        for i in range(attr.get_min_range(), attr.get_max_range() + 1):
            sub_df = df.loc[lambda x: x[attr.variable] == i]
            if max_count < len(sub_df.index):
                max_count = len(sub_df.index)
                max_value = i

        return max_value
