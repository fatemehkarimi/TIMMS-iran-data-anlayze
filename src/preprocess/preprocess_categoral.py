import pandas as pd

ALMOST_NULL_ATTRIBUTE_RATIO = 0.2

def fill_missing_value(df, attr):
    pd.to_numeric(df[attr.variable])

    if is_attr_too_null(df, attr):
        df = df.drop(labels=[attr.variable], axis=1)
        log_attr_removed(attr)
    else:
        med = get_data_median_for(df, attr)
        replace_invalid_values(df, attr, med)

    return df

def is_attr_too_null(df, attr):
    null_df = df.loc[lambda x : x[attr.variable] > attr.get_max_range()]
    if len(null_df.index) / len(df.index) >= ALMOST_NULL_ATTRIBUTE_RATIO:
        return True
    return False

def get_data_median_for(df, attr):
    valid_df = df.loc[lambda x : x[attr.variable] <= attr.get_max_range()]
    med = valid_df[attr.variable].median()
    return med


def replace_invalid_values(df, attr, surrogate_value):
    df[attr.variable] = df[attr.variable].fillna(surrogate_value)
    valid = df.loc[lambda x : x[attr.variable] > attr.get_max_range()]

    df.loc[
        lambda x : x[attr.variable] > attr.get_max_range(),
        attr.variable] = surrogate_value


def log_attr_removed(removed_attribute):
    with open("preprocess_nominal.log", "a") as f:
        f.write(removed_attribute.variable + "\n")
