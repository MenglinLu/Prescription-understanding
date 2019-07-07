"""
Prescription Base Class

Author: Tao Yang, tytaoyang@tencent.com
Date: 2018-03-27, init.
"""

import abc
import json
import ujson
from enum import Enum
from typing import List


class _BilingualEnum(Enum):
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)

    def __new__(cls, eng, chs=None):
        obj = object.__new__(cls)
        obj.eng = eng
        if chs is not None:
            obj.chs = chs
        obj._value_ = eng
        return obj


class _PrescriptionComponentType(_BilingualEnum):
    MEDICINE_NAME = 'Medicine_Name', '药品名称'  # or '品牌名称'
    BRAND_TYPE = 'Brand_Type', '药品来源'
    INGREDIENT = 'Ingredient', '药品成分'
    SPECIFICATION = 'Specification', '药品规格'
    DOSAGE_TYPE = 'Dosage_Type', '剂型'
    TOTAL_AMOUNT = 'Total_Amount', '给药总量'
    DOSAGE = 'Dosage', '每次用量'
    ROUTE = 'Route', '给药途径'
    FREQUENCY = 'Frequency', '给药时间'
    FOOTNOTE = 'Footnote', '脚注'


class PrescriptionComponent(object):
    def __init__(self, p_type: _PrescriptionComponentType):
        self.type: _PrescriptionComponentType = p_type

        self.offset_begin: int = None
        self.offset_end: int = None
        self.original_text: str = None
        self.interpretation: str = None

    def __iter__(self):
        if self.offset_begin is None:
            return
        else:
            yield 'Type', self.type
            yield 'Offset_Begin', self.offset_begin
            yield 'Offset_End', self.offset_end
            yield 'Original_Text', self.original_text
            yield 'Interpretation', self.interpretation


set_PrescriptionNumericalComponent = (_PrescriptionComponentType.SPECIFICATION,
                                      _PrescriptionComponentType.TOTAL_AMOUNT,
                                      _PrescriptionComponentType.DOSAGE,)


class PrescriptionNumericalComponent(PrescriptionComponent):
    def __init__(self, p_type: _PrescriptionComponentType):
        assert p_type in set_PrescriptionNumericalComponent, 'Wrong PrescriptionN Component Type...'
        super().__init__(p_type)
        self.value_unit: list = None

    def __iter__(self):
        if self.offset_begin is None:
            return
        else:
            for item in super().__iter__():
                yield item

            yield 'Value_Unit', self.value_unit


class JSONObjectEncoder(json.JSONEncoder):
    def default(self, obj) -> dict:
        if isinstance(obj, _BilingualEnum):
            return obj.eng

        data = dict(obj)
        org_str = ujson.dumps(data, ensure_ascii=False)
        json_dict = ujson.loads(org_str)
        return {type(obj).__name__: json_dict} if len(json_dict) > 0 else {}

    @staticmethod
    def to_json(input_obj) -> str:
        data = dict(input_obj)
        return json.dumps(data, ensure_ascii=False, cls=JSONObjectEncoder)


class PrescriptionResult(object):
    def __init__(self):
        self.medicine = PrescriptionComponent(_PrescriptionComponentType.MEDICINE_NAME)
        self.attributes: List[PrescriptionComponent] = []

    def __iter__(self):
        if self.medicine:
            for item in self.medicine.__iter__():
                yield item

        if self.attributes:
            yield 'Attributes', self.attributes


class PrescriptionComponentParserBase(object):
    @abc.abstractmethod
    def __init__(self):
        raise Exception('abstract method not implemented ...')

    @abc.abstractmethod
    def parse(self, in_str: str) -> List[PrescriptionComponent]:
        raise Exception('abstract method not implemented ...')
