import os

codebook_file = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__), 'T2019_G8_Codebook.xlsx'))

data_file = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__), 'TIMSS2019.xlsx'))

class SheetStructure:
    VARIABLE = 'Variable'
    LABEL = 'Label'
    LEVEL = 'Level'
    RANGE_MINIMUM = 'Range Minimum'
    RANGE_MAXIMUM = 'Range Maximum'
    VALUE_SCHEME_DETAILED = 'Value Scheme Detailed'


class AttrbuteLevel:
    ORDINAL = "Ordinal"
    NOMINAL = "Nominal"
    SCALE = "Scale"
    RATIO = "Ratio"
    NOT_DEFINED = "Not defined"


class BackgroundVariable:
    STUDENT = "BSGM7"
    TEACHER = "BTMM7"
    SCHOOL = "BCGM7"

ID_FIELDS = ['IDCNTRY', 'IDBOOK', 'IDSCHOOL', 'IDCLASS', 'IDSTUD']