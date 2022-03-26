from datetime import datetime
import pandas as pd
import numpy as np

OUTLIER_FACTOR = 1.5

def fill_missing_value(df, attr):
    if attr.variable not in df.columns:
        log_key_not_exist(attr)
        return df

    pd.to_numeric(df[attr.variable])
    min_range, max_range = get_outlier_range(df, attr)
    replace_outliers(df, attr, min_range, max_range, np.nan)


    
    return df


def get_outlier_range(df, attr):
    col_df = df[attr.variable]
    q1 = col_df.quantile(q=0.25)
    q3 = col_df.quantile(q=0.75)
    iqr = q3 - q1

    min_range = q1 - 1.5 * iqr
    max_range = q3 + 1.5 * iqr
    
    return min_range, max_range


def replace_outliers(df, attr, min_valid_value, max_valid_value, value):
    df.loc[
        lambda x : (x[attr.variable] < min_valid_value)
                    | (x[attr.variable] > max_valid_value),
        attr.variable] = value


def log_key_not_exist(attr):
    with open('preprocess_scale.log', 'a') as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            + ": " + 'key ' + attr.variable + '\tdoes not exists in dataframe\n')
