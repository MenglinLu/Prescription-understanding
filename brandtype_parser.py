"""
Created on Thu Mar 28 11:36:07 2019

@author: eileenlu
"""

import os

import pandas as pd

from ac_automaton import ACA
from base import PrescriptionComponent
from base import PrescriptionComponentParserBase
from base import _PrescriptionComponentType


class BrandTypeParser(PrescriptionComponentParserBase):
    
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        brandtype_list = list(pd.read_excel(dir_path + '/data/dict.xlsx', sheetname='drugtype_dict', header=None).iloc[:, 0])
        self.aca: ACA = ACA()
        self.aca.add_words(brandtype_list)

    def parse(self, in_str: str) -> PrescriptionComponent:
        """
        :param in_str:
        :return:
        """
        res = PrescriptionComponent(_PrescriptionComponentType.BRAND_TYPE)
        for last_idx, term in self.aca.get_hits_with_index(in_str):
            res.original_text = term
            res.offset_begin = last_idx + 1 - len(term)
            res.offset_end = last_idx
            res.type = res.type.value
        return res
