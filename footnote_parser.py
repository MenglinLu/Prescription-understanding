"""
Created on Thu Mar 28 21:16:56 2019

@author: eileenlu
"""

import re
from typing import List

from base import PrescriptionComponent, _PrescriptionComponentType


class FootnoteParser(object):
    def __init__(self):
        self.rep_footnote = re.compile(r"[\u4e00-\u9fa5]\S*")

    def parse(self, in_str: str, all_str: str) -> List[PrescriptionComponent]:
        """
        :param in_str, all_str:
        :return:
        """
        results: List[PrescriptionComponent] = []
        footnote_list = self.rep_footnote.findall(in_str)
        for footnote_i in footnote_list:
            a_result = PrescriptionComponent(_PrescriptionComponentType.FOOTNOTE)
            a_result.original_text = footnote_i.strip('）')
            a_result.offset_begin = all_str.find(footnote_i)
            a_result.offset_end = a_result.offset_begin + len(footnote_i) - 1
            a_result.type = a_result.type.value
            results.append(a_result)
            
        return results
