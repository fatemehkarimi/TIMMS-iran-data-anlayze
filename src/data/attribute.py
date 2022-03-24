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