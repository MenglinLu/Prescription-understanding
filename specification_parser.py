"""
Created on Thu Mar 28 20:44:13 2019

@author: eileenlu
"""

import os
import re
import pandas as pd
from base import PrescriptionNumericalComponent, _PrescriptionComponentType
from typing import List

class SpecificationTotalAmountParser(object):

    def __init__(self, in_str: str):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        
        unit_df = pd.read_excel(self.dir_path + r'/data/dict.xlsx', sheetname = 'unit_dict', header = None)
        unit_dict = dict()
        for i in range(len(unit_df)):
            unit_dict[unit_df.iloc[i, 0]] = unit_df.iloc[i, 1]
        self.unit_dict = unit_dict
        
        self.rep_spec_valueunit = re.compile("[0-9][0-9|a-z|\u4e00-\u9fa5|.]+")
        self.rep_spec_value = re.compile("[0-9|.]+")
        self.rep_spec_unit = re.compile("[a-z|\u4e00-\u9fa5]+")
        
        rep_dosage = re.compile(r"[0-9]\S+")
        if ('sig' in in_str):
            sig_pos = in_str.find('sig')
            totalamount_text = rep_dosage.findall(in_str, 0, sig_pos)
            if (len(totalamount_text) > 0):
                totalamount_text = totalamount_text[-1]
                if ('*' in totalamount_text and '×' in totalamount_text):
                    componet_list = re.split("[*×]", totalamount_text)
                    specification_text = componet_list[0]  ###每片规格
                    every_text = componet_list[1]  ###每盒多少片
                    amount_text = componet_list[2]  ###给药多少盒
                if ('*' in totalamount_text and '×' not in totalamount_text):
                    componet_list = totalamount_text.split('*')
                    specification_text = componet_list[0]
                    every_text = componet_list[1]
                    amount_text = "1.000"
                if ('*' not in totalamount_text and '×' in totalamount_text):
                    componet_list = totalamount_text.split('×')
                    specification_text = componet_list[0]
                    every_text = '1'
                    amount_text = componet_list[1]
                if ('*' not in totalamount_text and '×' not in totalamount_text):
                    specification_text = totalamount_text
                    every_text = '1'
                    amount_text = "1.000"
                self.totalamount_text = totalamount_text  ###给药总量
                self.specification_text = specification_text  ###描述每片规格
                self.every_text = every_text  ###描述每盒多少片
                self.amount_text = amount_text  ###描述给药多少盒
            else:
                self.totalamount_text = "Null"
        else:
            self.totalamount_text = "Null"

    def parse_specfication(self, all_str: str) -> PrescriptionNumericalComponent:
        """
        :param all_str:
        :return:
        """
        res_specification = PrescriptionNumericalComponent(_PrescriptionComponentType.SPECIFICATION)
        
        valueunit_list = []
        valueunit_interpretation = ""
        for valueunit in self.rep_spec_valueunit.findall(self.specification_text):
            value = self.rep_spec_value.findall(valueunit)[0]
            unit = self.rep_spec_unit.findall(valueunit)
            if (len(unit) > 0):
                unit = unit[0]
                if ('\u4e00' <= unit <= '\u9fff'):
                    unit = unit
                else:
                    unit = self.unit_dict[unit]
            else:
                unit = ""
            valueunit_interpretation = valueunit_interpretation + ' ' + str(value) + unit
            valueunit_dict = {'value': float(value), 'unit': unit}
            valueunit_list.append(valueunit_dict)
            
        res_specification.value_unit = valueunit_list
        res_specification.interpretation = "每片/粒/袋/支" + valueunit_interpretation
        res_specification.original_text = self.specification_text
        res_specification.offset_begin = all_str.find(self.specification_text)
        res_specification.offset_end = all_str.find(self.specification_text) + len(self.specification_text)
        res_specification.type = res_specification.type.value
        return res_specification

    def parse_totalamount(self, all_str: str) -> PrescriptionNumericalComponent:
        """
        :param all_str:
        :return:
        """
        res_totalamount = PrescriptionNumericalComponent(_PrescriptionComponentType.TOTAL_AMOUNT)
        res_spec_specification = self.parse_specfication(all_str)
        res_totalamount.original_text = self.totalamount_text
        res_totalamount.offset_begin = all_str.find(self.totalamount_text)
        res_totalamount.offset_end = all_str.find(self.totalamount_text) + len(self.totalamount_text)
        res_totalamount.type = res_totalamount.type.value
        
        every_value = float(re.compile('[0-9|.]+').findall(self.every_text)[0])
        amount_value = float(re.compile('[0-9|.]+').findall(self.amount_text)[0])
        if (len(res_spec_specification.value_unit) > 0):
            res_totalamount.unit = res_spec_specification.value_unit[0]['unit']
            value = round(res_spec_specification.value_unit[0]['value'] * every_value * amount_value, 2)
            res_totalamount.value = value
            res_totalamount.interpretation = res_spec_specification.interpretation + "，每盒" + str(
                every_value) + "片/粒/袋/支，共" + str(amount_value) + "盒，共计" + str(
                value) + res_totalamount.unit
                    
        return res_totalamount
    
    def parser(self, all_str: str) -> List[PrescriptionNumericalComponent]:
        """
        :param all_str:
        :return:
        """
        if(self.totalamount_text != 'Null'):
            specification_res = self.parse_specfication(all_str)
            totalamount_res = self.parse_totalamount(all_str)
        else:
            specification_res = PrescriptionNumericalComponent(_PrescriptionComponentType.SPECIFICATION)
            totalamount_res = PrescriptionNumericalComponent(_PrescriptionComponentType.TOTAL_AMOUNT)
        return [specification_res, totalamount_res]
