import pandas as pd

def fill_missing_value(df, attr):
    pd.to_numeric(df[attr.variable])
    extract_options(attr)
    med = get_data_median_for(df, attr)
    replace_invalid_values(df, attr, med)
    return df


def extract_options(attr):
    detail = attr.detail
    option_str_list = detail.split(";")

    options = []
    for option in option_str_list:
        option_text = option.split(':')
        if len(option_text) >= 2:
            options.append(option_text[1].strip())

    attr.set_options(options)


def get_data_median_for(df, attr):
    valid_df = df.loc[lambda x : x[attr.variable] <= attr.get_max_range()]
    med = valid_df[attr.variable].median()
    return med


def replace_invalid_values(df, attr, surrogate_value):
    df[attr.variable] = df[attr.variable].fillna(surrogate_value)
    df.loc[
        lambda x : x[attr.variable] > attr.get_max_range(),
        attr.variable] = surrogate_value
