import pandas as pd
from data.attribute import Attribute
from dataset.datasetConst import codebook_file, SheetStructure

class Codebook:
    def __init__(self):
        self.df = pd.read_excel(codebook_file, sheet_name=None)
        self.attribute_list = []

        for key in self.df.keys():
            for idx, row in self.df[key].iterrows():
                attr = Attribute(
                    key,
                    row[SheetStructure.VARIABLE],
                    row[SheetStructure.LABEL],
                    row[SheetStructure.LEVEL],
                    row[SheetStructure.VALUE_SCHEME_DETAILED]
                )
                self.attribute_list.append(attr)


    def get_attribute_list(self):
        return self.attribute_list
    