"""
Created on Thu Mar 28 19:36:59 2019

@author: eileenlu
"""

import os
import re
from typing import List

import pandas as pd

from ac_automaton import ACA
from base import PrescriptionComponent, _PrescriptionComponentType
from base import PrescriptionComponentParserBase


class FrequencyParser(PrescriptionComponentParserBase):

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        frequency_list = list(
            pd.read_excel(dir_path + r'/data/dict.xlsx', sheetname='frequency_dict',
                          header=None).iloc[:, 0])
        self.aca: ACA = ACA()
        self.aca.add_words(frequency_list)
        fre_df = pd.read_excel(dir_path + r'/data/dict.xlsx', sheetname='frequency_dict',
                               header=None)
        self.fre_dict = dict()
        for i in range(len(fre_df)):
            self.fre_dict[fre_df.iloc[i, 0]] = fre_df.iloc[i, 1]
        self.rep_frequency = re.compile(
                r"([\u4e00-\u9fa5]*['时','天','日','前','后','早','晚','午','餐','饭'][\u4e00-\u9fa5]*)")

    def parse(self, in_str: str, all_str: str) -> List[PrescriptionComponent]:
        """
        :param in_str, all_str:
        :return:
        """
        results: List[PrescriptionComponent] = []
        maxlen = -1
        for last_idx, term in self.aca.get_hits_with_index(in_str):
            if (len(term) > maxlen):
                maxlen = len(term)
                frequency_text = term
        if ('frequency_text' in vars()):
            a_result = PrescriptionComponent(_PrescriptionComponentType.FREQUENCY)
            a_result.original_text = frequency_text
            a_result.offset_begin = all_str.find(frequency_text)
            a_result.offset_end = all_str.find(frequency_text) + len(frequency_text) - 1
            a_result.interpretation = self.fre_dict[frequency_text]
            a_result.type = a_result.type.value
            results.append(a_result)
        
        frequencylist = self.rep_frequency.findall(in_str)
        for frequency_i in frequencylist:
            a_result = PrescriptionComponent(_PrescriptionComponentType.FREQUENCY)
            a_result.original_text = frequency_i
            a_result.offset_begin = all_str.find(frequency_i)
            a_result.offset_end = all_str.find(frequency_i) + len(frequency_i) - 1
            a_result.type = a_result.type.value
            a_result.interpretation = frequency_i
            results.append(a_result)

        return results
