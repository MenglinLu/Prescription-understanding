"""
Created on Thu Mar 28 20:43:23 2019

@author: eileenlu
"""

import os
import re
from typing import List
import pandas as pd
from base import PrescriptionComponentParserBase
from base import PrescriptionNumericalComponent, _PrescriptionComponentType


class DosageParser(PrescriptionComponentParserBase):
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        
        unit_df = pd.read_excel(dir_path + r'/data/dict.xlsx', sheetname = 'unit_dict', header = None)
        self.unit_dict = dict()
        for i in range(len(unit_df)):
            self.unit_dict[unit_df.iloc[i, 0]] = unit_df.iloc[i, 1]
            
        self.rep_dosage = re.compile("[0-9|.]+[a-z|\u4e00-\u9fa5]+")
        self.rep_spec_value = re.compile("[0-9][0-9|.]*")
        self.rep_spec_unit = re.compile("[a-z|\u4e00-\u9fa5]+")
        self.rep_dosage1 = re.compile("\S*['量']+\S*")

    def parse(self, in_str: str, all_str: str, specification, specunit) -> List[PrescriptionNumericalComponent]:
        """
        :param in_str, all_str, specification, specunit:
        :return:
        """
        dosage_text = self.rep_dosage.findall(in_str)
        if ('sig' in all_str):
            sig_pos = all_str.find('sig')
        else:
            sig_pos = 0
        results: List[PrescriptionNumericalComponent] = []
        for dosage_i in dosage_text:
            value = self.rep_spec_value.findall(dosage_i)
            if(len(value)>0):
                value=value[0]
                unit = self.rep_spec_unit.findall(dosage_i)
                if (len(unit) > 0):
                    unit = unit[0]
                    if ('\u4e00' <= unit <= '\u9fff'):
                        unit = unit
                    else:
                        unit = self.unit_dict[unit]
                else:
                    unit=""
            a_result = PrescriptionNumericalComponent(_PrescriptionComponentType.DOSAGE)
            valueunit_dict = {'value': float(value), 'unit': unit}
            a_result.original_text = dosage_i
            a_result.offset_begin = all_str.find(dosage_i, sig_pos, len(all_str))
            a_result.offset_end = all_str.find(dosage_i, sig_pos, len(all_str)) + len(dosage_i)
            a_result.type = a_result.type.value
            a_result.value_unit = valueunit_dict
            if (unit == specunit):
                calcu_value = round(float(value) * 1.0 / specification, 4)
                a_result.interpretation = str(calcu_value) + '片/粒/袋/支'
            results.append(a_result)
        
        dosage_text1 = self.rep_dosage1.findall(in_str)
        for dosage_i1 in dosage_text1:
            a_result = PrescriptionNumericalComponent(_PrescriptionComponentType.DOSAGE)
            a_result.original_text = dosage_i1
            a_result.offset_begin = all_str.find(dosage_i1, sig_pos, len(all_str))
            a_result.offset_end = all_str.find(dosage_i1, sig_pos, len(all_str)) + len(dosage_i1) - 1
            a_result.type = a_result.type.value
            value = dosage_i1
            unit = ""
            valueunit_dict = {'value': value, 'unit': unit}
            a_result.interpretation = value
            results.append(a_result)

        return results
