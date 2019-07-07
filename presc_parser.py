"""
Created on Thu Mar 28 14:40:43 2019

@author: eileenlu
"""

from Ingredient_parser import IngredientParser
from base import PrescriptionResult
from brandname_parser import BrandnameParser
from brandtype_parser import BrandTypeParser
from dosage_parser import DosageParser
from dosagetype_parser import DosagetypeParser
from footnote_parser import FootnoteParser
from frequency_parser import FrequencyParser
from route_parser import RouteParser
from specification_parser import SpecificationTotalAmountParser


class PrescParser(object):

    def __init__(self):
        pass

    def parse(self, line: str) -> PrescriptionResult:
        """
        :param line:
        :return:
        """
        line = line.lower()

        parser = BrandnameParser()
        brandname_res = parser.parse(line)
        left_str = line.replace(brandname_res.medicine.original_text, '').strip()
        brandtype_res = BrandTypeParser().parse(left_str)
        brandname_res.attributes.append(brandtype_res)

        if brandtype_res.original_text is not None:
            left_str = left_str.replace(brandtype_res.original_text, '').strip()

        ingredient_res = IngredientParser().parse(left_str, line)
        brandname_res.attributes.append(ingredient_res)
        dosagetype_res = DosagetypeParser().parse(left_str, line)
        brandname_res.attributes.append(dosagetype_res)

        specificationamount = SpecificationTotalAmountParser(left_str)
        specification_res = specificationamount.parser(line)[0]
        totalamount_res = specificationamount.parser(line)[1]

        brandname_res.attributes.append(specification_res)
        brandname_res.attributes.append(totalamount_res)
        left_str = left_str.replace('sig.', '').replace('sig', '').strip()
        if totalamount_res.original_text is not None:
            left_str = left_str.replace(totalamount_res.original_text, '').strip()

        frequency_res = FrequencyParser().parse(left_str, line)
        brandname_res.attributes.append(frequency_res)
        if len(frequency_res) > 0:
            for i in frequency_res:
                left_str = left_str.replace(i.original_text, '').strip()

        route_res = RouteParser().parse(left_str, line)
        brandname_res.attributes.append(route_res)

        if route_res.original_text is not None:
            left_str = left_str.replace(route_res.original_text, '').strip()

        dosageparser = DosageParser()
        if (specification_res.value_unit is not None):
            if (len(specification_res.value_unit) > 0):
                dosage_res = dosageparser.parse(in_str=left_str, all_str=line,
                                                specification=specification_res.value_unit[0][
                                                    'value'],
                                                specunit=specification_res.value_unit[0]['unit'])
        else:
            dosage_res = dosageparser.parse(in_str=left_str, all_str=line, specification=-1.0, specunit="")
        brandname_res.attributes.append(dosage_res)

        if (len(dosage_res) > 0):
            for i in dosage_res:
                left_str = left_str.replace(i.original_text, '').strip()

        footnote_res = FootnoteParser().parse(left_str, line)
        brandname_res.attributes.append(footnote_res)

        return brandname_res
