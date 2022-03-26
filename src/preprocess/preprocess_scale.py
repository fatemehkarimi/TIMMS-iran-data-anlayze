from datetime import datetime
import pandas as pd
import numpy as np
from scipy import stats

OUTLIER_FACTOR = 1.5
ALMOST_NULL_ATTRIBUTE_RATIO = 0.3

def fill_missing_value(df, attr):
    if attr.variable not in df.columns:
        log_key_not_exist(attr)
        return df

    if is_attr_too_null(df, attr):
        df = df.drop(labels=[attr.variable], axis=1)
        log_attr_removed(attr)
        return df

    pd.to_numeric(df[attr.variable])
    min_range, max_range = get_outlier_range(df, attr)
    replace_outliers(df, attr, min_range, max_range, np.nan)
    
    surrogate_value = df[attr.variable].dropna().median()
    if has_normal_dist(df, attr):
        surrogate_value = df[attr.variable].dropna().mean()
    
    df[attr.variable] = df[attr.variable].fillna(surrogate_value)
    return df


def is_attr_too_null(df, attr):
    num_nulls = df[attr.variable].isna().sum()
    if num_nulls / len(df.index) >= ALMOST_NULL_ATTRIBUTE_RATIO:
        return True
    return False


def get_outlier_range(df, attr):
    col_df = df[attr.variable]
    q1 = col_df.quantile(q=0.25)
    q3 = col_df.quantile(q=0.75)
    iqr = q3 - q1

    min_range = q1 - OUTLIER_FACTOR * iqr
    max_range = q3 + OUTLIER_FACTOR * iqr
    
    return min_range, max_range


def replace_outliers(df, attr, min_valid_value, max_valid_value, value):
    df.loc[
        lambda x : (x[attr.variable] < min_valid_value)
                    | (x[attr.variable] > max_valid_value),
        attr.variable] = value


def has_normal_dist(df, attr):
    k2, p = stats.normaltest(df[attr.variable].to_numpy(), nan_policy='omit')
    if p <= 0.05:
        return False
    return True


def log_key_not_exist(attr):
    with open('preprocess_scale.log', 'a') as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            + ": " + 'key ' + attr.variable + '\tdoes not exists in dataframe\n')


def log_attr_removed(attr):
    with open("preprocess_nominal.log", "a") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            + ": " + "attribute " + attr.variable + "\tremoved\n")
