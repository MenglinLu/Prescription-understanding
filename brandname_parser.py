# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 11:36:07 2019

@author: eileenlu
"""

import os
import pandas as pd
from ac_automaton import ACA
from base import PrescriptionResult
from base import PrescriptionComponentParserBase

class BrandnameParser(PrescriptionComponentParserBase):
    
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        brandname_list_addition = list(pd.read_excel(dir_path + '/data/dict.xlsx', sheetname = 'brandname_dict', header = None).iloc[: , 0])
        brandname_list_cfda = list(set(pd.read_csv(dir_path + '/data/brandname.csv', header = None).iloc[: , 0]))
        brandname_list = list(set(brandname_list_cfda + brandname_list_addition))
        self.aca: ACA = ACA()
        self.aca.add_words(brandname_list)

    def parse(self, in_str: str) -> PrescriptionResult:
        """
        :param in_str:
        :return:
        """
        res = PrescriptionResult()
        maxlen = -1
        for last_idx, term in self.aca.get_hits_with_index(in_str):
            if (len(term) > maxlen):
                maxlen = len(term)
                brandname_text = term
                end_index = last_idx
        res.medicine.original_text = brandname_text
        res.medicine.offset_begin = end_index + 1 - len(brandname_text)
        res.medicine.offset_end = end_index
        res.medicine.type = res.medicine.type.value
        return res


        
        
        
        

        
        
    
    


            

            
                    
            
        
        