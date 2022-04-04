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


class AttributeLevel:
    ORDINAL = "Ordinal"
    NOMINAL = "Nominal"
    SCALE = "Scale"
    RATIO = "Ratio"
    NOT_DEFINED = "Not defined"


class BackgroundVariable:
    STUDENT = "BSGM7"
    TEACHER = "BTMM7"
    SCHOOL = "BCGM7"


class Fields:
    ID_COUNTRY = 'IDCNTRY'
    ID_BOOK = 'IDBOOK'
    ID_SCHOOL = 'IDSCHOOL'
    ID_CLASS = 'IDCLASS'
    ID_STUDENT = 'IDSTUD'
    FINAL_SCORE = 'finalscore'
    FINAL_SCORE_ALGEBRA = 'finalscorealgebra'
    FINAL_SCORE_DAT = 'finalscoredat'
    FINAL_SCORE_GEO = 'finalscoregeo'
    FINAL_SCORE_NUM = 'finalscorenum'

ID_FIELDS = [Fields.ID_COUNTRY, Fields.ID_BOOK,
                Fields.ID_SCHOOL, Fields.ID_CLASS, Fields.ID_STUDENT]

SCORE_FIELDS = [Fields.FINAL_SCORE, Fields.FINAL_SCORE_ALGEBRA,
                Fields.FINAL_SCORE_DAT, Fields.FINAL_SCORE_GEO,
                Fields.FINAL_SCORE_NUM]
