"""
Created on Thu Mar 28 19:36:59 2019

@author: eileenlu
"""

import os
import re

import pandas as pd

from ac_automaton import ACA
from base import PrescriptionComponent, _PrescriptionComponentType


class RouteParser(object):

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        route_list = list(
            pd.read_excel(dir_path + r'/data/dict.xlsx',
                          sheetname='route_dict',
                          header=None).iloc[:, 0])
        self.aca: ACA = ACA()
        self.aca.add_words(route_list)
        route_df = pd.read_excel(dir_path + r'/data/dict.xlsx', sheetname='route_dict', header=None)
        self.route_dict = dict()
        for i in range(len(route_df)):
            self.route_dict[route_df.iloc[i, 0]] = route_df.iloc[i, 1]
        self.rep_route = re.compile(
                r"([\u4e00-\u9fa5]*['入','射','服','眼','耳','外','内','疗','用']+[\u4e00-\u9fa5]*)")

    def parse(self, in_str: str, all_str: str) -> PrescriptionComponent:
        """
        :param in_str, all_str:
        :return:
        """
        if ('sig' in all_str):
            sig_pos = all_str.find('sig') + 3
        else:
            sig_pos = 0
        maxlen = -1
        for last_idx, term in self.aca.get_hits_with_index(in_str):
            if (len(term) > maxlen):
                maxlen = len(term)
                route_text = term
        a_result = PrescriptionComponent(_PrescriptionComponentType.ROUTE)
        if ('route_text' in vars()):
            a_result.original_text = route_text
            a_result.offset_begin = all_str.find(route_text, sig_pos, len(all_str))
            a_result.offset_end = a_result.offset_begin + len(route_text) - 1
            a_result.interpretation = self.route_dict[route_text]
            a_result.type = a_result.type.value
        else: 
            routelist = self.rep_route.findall(in_str)
            if (len(routelist) > 0):
                a_result.original_text = routelist[0]
                a_result.offset_begin = all_str.find(routelist[0])
                a_result.offset_end = all_str.find(routelist[0]) + len(routelist[0]) - 1
                a_result.interpretation = routelist[0]
                a_result.type = a_result.type.value
                
        return a_result
