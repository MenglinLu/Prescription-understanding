"""
Created on Thu Mar 28 14:40:43 2019

@author: eileenlu
"""
import os
import sys

import exceptions
from base import JSONObjectEncoder
from detector import Detector
from presc_parser import PrescParser


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    lines = "*门冬胰岛素 300u×1.000 Sig.5-5-5u 三餐前 qd"
    lines=lines.lower()
    f_output = open(dir_path + r'\results\med_prescription_parser.json', 'w', errors='ignore',
                    encoding='utf-8')
    det = Detector()
    try:
        prescs_lines = det.detector(lines)
        for line in prescs_lines:
            print(line)
            preparser = PrescParser()
            lines_res = preparser.parse(line)
            f_output.write(JSONObjectEncoder().to_json(lines_res))
            f_output.write('\n')
    except exceptions.NoPrescException:
        print(lines)
    finally:
        f_output.close()

if __name__ == '__main__':
    sys.exit(main())
