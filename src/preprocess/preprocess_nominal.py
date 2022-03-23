def fill_missing_value(df, attr):
    if attr.min_range is None or attr.max_range is None:
        extract_range(attr)


def extract_range(attr):
    detail = attr.detail
    option_str_list = detail.split(";")

    options = []
    for option in option_str_list:
        option_text = option.split(':')
        if len(option_text) >= 2:
            options.append(option_text[1].strip())

    attr.min_range = 1
    attr.max_range = len(option)
    attr.set_options(options)
