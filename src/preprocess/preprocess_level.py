from datetime import datetime


class LevelPreprocess:
    def __init__(self):
        self.log_file = 'preprocess.log'

    def fill_missing_value(self, df, attr):
        raise NotImplementedError

    def log_attr_removed(self, attr):
        with open(self.log_file, "a") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                + ": " + "attribute " + attr.variable + "\tremoved\n")

    def log_key_not_exist(self, attr):
        with open(self.log_file, 'a') as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                + ": " + 'key ' + attr.variable + '\tdoes not exists in dataframe\n')
