from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


class LevelPreprocess:
    def __init__(self):
        self.log_file = 'preprocess.log'

    def fill_missing_value(self, df, attr_list):
        raise NotImplementedError

    def visualize_correlation(self, df, attr_list):
        raise NotImplementedError

    def plot_correlation(self, correlation, filename, labels=None):
        fig = plt.figure(figsize=(10.41, 7.29))
        ax = fig.add_subplot(111)
        cax = ax.matshow(correlation, vmin=-1, vmax=1)
        fig.colorbar(cax)
        if labels:
            ticks = np.arange(0, len(labels), 1)
            ax.set_xticks(ticks)
            ax.set_yticks(ticks)
            ax.set_xticklabels(labels)
            ax.set_yticklabels(labels)
        plt.savefig(filename)

    def filter_correlated_columns(self, df, attr_list):
        raise NotImplementedError

    def log_attr_removed(self, attr):
        with open(self.log_file, "a") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                + ": " + "attribute " + attr.variable + "\tremoved\n")

    def log_key_not_exist(self, attr):
        with open(self.log_file, 'a') as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                + ": " + 'key ' + attr.variable + '\tdoes not exists in dataframe\n')
