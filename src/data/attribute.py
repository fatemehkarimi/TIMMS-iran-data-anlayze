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


    def set_options(self, options):
        self.options = options
