"""
Created on Thu Mar 28 14:48:24 2019

@author: eileenlu
"""

from base import PrescriptionComponent, _PrescriptionComponentType


class IngredientParser(object):

    def __init__(self):
        pass

    def parse(self, in_str: str, all_str: str) -> PrescriptionComponent:
        """
        :param in_str, all_str:
        :return:
        """
        res = PrescriptionComponent(_PrescriptionComponentType.INGREDIENT)
        return res
