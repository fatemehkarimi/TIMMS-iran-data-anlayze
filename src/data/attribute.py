from operator import le
import dataset.datasetConst as dataConst
class Attribute:
    def __init__(self, background, variable, label,
                    level, detail, min_range=None, max_range=None):
        self.background = background
        self.variable = variable
        self.label = label
        self.level = level
        self.detail = detail
        self.min_range = min_range
        self.max_range = max_range
        self.options = []
        self.extract_options()


    def set_options(self, options):
        self.options = options

    def get_options(self):
        return self.options

    def get_min_range(self):
        if self.min_range is None:
            return 1
        return self.min_range

    def get_max_range(self):
        if self.max_range is None:
            return len(self.options)
        return self.max_range

    def extract_options(self):
        if (self.level != dataConst.AttributeLevel.NOMINAL
            and self.level != dataConst.AttributeLevel.ORDINAL):
            return

        detail = self.detail
        option_str_list = detail.split(";")

        options = []
        for option in option_str_list:
            option_text = option.split(':')
            if len(option_text) >= 2:
                options.append(option_text[1].strip())

        self.set_options(options)