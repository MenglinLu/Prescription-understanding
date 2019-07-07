"""
Created on Tue Apr  9 11:01:57 2019

@author: eileenlu
"""

import logging
import os
import sys

import pandas as pd
import re
import exceptions
from ac_automaton import ACA


class Detector(object):
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.rep_frequency = re.compile(r"([\u4e00-\u9fa5]*['时','天','日','前','后','早','晚','午','餐','饭'][\u4e00-\u9fa5]*)")
        self.rep_route = re.compile(r"([\u4e00-\u9fa5]*['入','射','服','眼','耳','外','内','疗','用']+[\u4e00-\u9fa5]*)")
        self.aca: ACA = ACA()
        brandname_list_cfda = list(set(pd.read_csv(dir_path + '/data/brandname.csv',header = None).iloc[:,0]))
        brandname_list_addition = list(pd.read_excel(dir_path + '/data/dict.xlsx',sheetname = 'brandname_dict',header = None).iloc[:, 0])
        brandname_list = list(set(brandname_list_cfda + brandname_list_addition))
        self.aca.add_words(brandname_list)
        
        self.aca_route: ACA = ACA()
        route_list = list(
            pd.read_excel(dir_path + '/data/dict.xlsx',
                          sheetname = 'route_dict',
                          header = None).iloc[:, 0])
        self.aca_route.add_words(route_list)
        
        self.aca_frequency: ACA = ACA()
        frequency_list = list(
            pd.read_excel(dir_path + '/data/dict.xlsx',
                          sheetname = 'frequency_dict',
                          header = None).iloc[:, 0])
        self.aca_frequency.add_words(frequency_list)
        
        
        
    def detector(self, lines: str) -> list:
        results = []
        for last_idx, term in self.aca.get_hits_with_index(lines):
            a_result = [term, last_idx + 1 - len(term), last_idx]
            results.append(a_result)
        ###删除错误药品名
        results_final=[]
        for result_i in results:
            start_i=result_i[1]
            end_i=result_i[2]
            flag=0
            for result_j in results:
                start_j=result_j[1]
                end_j=result_j[2]
                if((start_i>=start_j and end_i<=end_j) and (result_i[0]!=result_j[0])):
                    flag=1
            if(flag==0):
                results_final.append(result_i)
        print(str(results_final))
        try:
            ####匹配药品名
            presc_list = []
            presc_list_final = []
            for i in range(len(results_final) - 1):
                p_lines = lines[results_final[i][1]:results_final[i + 1][1]].strip()
                if (p_lines.strip().strip('*') != ''):
                    presc_list.append(p_lines)
            last_lines = lines[results_final[len(results_final) - 1][1]:len(lines)]
            if last_lines.strip().strip('*') != '':
                presc_list.append(last_lines)
            ####匹配给药时间
            for presc_ii in presc_list:
                if('sig' in presc_ii):
                    presc_i = presc_ii.replace('sig','')
                    sig_pos = presc_ii.find('sig')+3
                else:
                    presc_i = presc_ii
                    sig_pos = 0
                maxlen_fre = -1
                frequency_end=0
                for last_idx, term in self.aca_frequency.get_hits_with_index(presc_i):
                    if (len(term) > maxlen_fre):
                        maxlen_fre = len(term)
                        text_fre = term
                if('text_fre' in vars()):
                    frequency_end_0 = presc_ii.find(text_fre,sig_pos,len(presc_ii))+len(text_fre)
                    presc_i = presc_i.replace(text_fre,'')
                    frequency_end = max(frequency_end,frequency_end_0)
                frequencylist = self.rep_frequency.findall(presc_ii)
                if(len(frequencylist)>0):
                    frequency_end_1 = presc_ii.find(frequencylist[-1])+len(frequencylist[-1])
                    frequency_end = max(frequency_end,frequency_end_1)
               
                maxlen_route = -1
                route_end = 0
                for last_idx, term in self.aca_route.get_hits_with_index(presc_i):
                    if (len(term) > maxlen_route):
                        maxlen_route = len(term)
                        text_route = term
                if('text_route' in vars()):
                    route_end_0 = presc_ii.find(text_route,sig_pos,len(presc_ii))+len(text_route)
                    route_end = max(route_end,route_end_0)
                routelist = self.rep_route.findall(presc_ii)
                if(len(routelist)>0):
                    route_end_1 = presc_ii.find(routelist[-1])+len(routelist[-1])
                    route_end = max(route_end,route_end_1)

                end_presc = max(frequency_end,route_end)
                if(end_presc == 0):
                    end_presc = len(presc_ii)
                presc_i_final = presc_ii[:end_presc]
                presc_list_final.append(presc_i_final)
            return presc_list_final

        except IndexError:
            logging.error('!!! Error: Not prescription')
            logging.error(lines)
            raise exceptions.NoPrescException()


def detector_test():
    """
    unit test
    :return: 
    """
    ec = Detector()

    lines = '''4.出院带药：阿司匹林(进口) 100mg*30×30.000 Sig.100.000mg po qd 泮托拉唑(进口) 40mg*7×14.000 Sig.40.000mg po bid 瑞舒伐他汀钙(进口) 10mg*7×7.000 Sig.10.000mg po qn *美托洛尔缓释片(合资) 47.5mg*7×7.000 Sig.47.500mg po qd 达比加群酯 110mg*10×20.000 Sig.110.000mg po bid

5.如您不方便到我院复诊，请携带病历资料到就近社区医院或社康中心复诊，以上出院医嘱内容可作为社区医师治疗或康复建议方案的参考。'''
    try:
        for line in lines.split('\n'):
            presc_lines = ec.detector(line.strip().lower())
            print(presc_lines)
    except exceptions.NoPrescException:
        presc_lines = None
        print(presc_lines)

if __name__ == "__main__":
    sys.exit(detector_test())
