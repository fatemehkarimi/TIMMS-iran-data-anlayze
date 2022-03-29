from datetime import datetime
import pandas as pd

from preprocess_level import LevelPreprocess

ALMOST_NULL_ATTRIBUTE_RATIO = 0.2

class OrdinalPreprocess(LevelPreprocess):
    def fill_missing_value(self, df, attr):
        pd.to_numeric(df[attr.variable])

        if self.is_attr_too_null(df, attr):
            df = df.drop(labels=[attr.variable], axis=1)
            self.log_attr_removed(attr)
        else:
            med = self.get_data_median_for(df, attr)
            self.replace_invalid_values(df, attr, med)

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


    def get_data_median_for(self, df, attr):
        valid_df = df.loc[
            lambda x : (x[attr.variable] <= attr.get_max_range())
                        | (x[attr.variable] >= attr.get_min_range())]
        med = valid_df[attr.variable].median()
        return med


    def replace_invalid_values(self, df, attr, surrogate_value):
        df[attr.variable] = df[attr.variable].fillna(surrogate_value)
        df.loc[
            lambda x : (x[attr.variable] < attr.get_min_range())
                        | (x[attr.variable] > attr.get_max_range()),
            attr.variable] = surrogate_value


    def log_attr_removed(self, attr):
        with open("preprocess_nominal.log", "a") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                + ": " + "attribute " + attr.variable + "\tremoved\n")