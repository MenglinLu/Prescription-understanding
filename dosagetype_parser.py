"""
Created on Thu Mar 28 15:57:49 2019

@author: eileenlu
"""

from base import PrescriptionComponent, _PrescriptionComponentType


class DosagetypeParser(object):

    def __init__(self):
        pass

    def parse(self, in_str: str, all_str: str) -> PrescriptionComponent:
        """
        :param in_str, all_str:
        :return:
        """
        res = PrescriptionComponent(_PrescriptionComponentType.DOSAGE_TYPE)
        return res
