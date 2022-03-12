#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/8 13:08
# @Author  : YoumingDong
# @File    : OutputModel.py
# @Software: win10  python3.9
import copy

import numpy as np
import pandas as pd
import getModel as gm

# 全局变量 用于记录递归次数（穿刺次数）
global_recursion_counter = 0

# 全局变量 用于记录当前的母公司名称
global_company_name = ""

# 全局变量 用于记录当前母公司的编号
global_index_num = np.NAN
# 全局变量 用于记录当前母公司的支行名称
global_sub_bank = np.NAN
# 全局变量 用于保存当前母公司中，所有的结果表，最后集中输出。
global_table_list = []

def recursion_counter_up():
    global global_recursion_counter
    global_recursion_counter += 1

def recursion_counter_down():
    global global_recursion_counter
    global_recursion_counter = global_recursion_counter - 1

def recursion_counter_init():
    '''
    递归次数初始化
    :return:
    '''
    global global_recursion_counter
    global_recursion_counter = 0

def recursion_counter_if1():
    '''
    判断是否进行了穿刺
    :return:进行了返回ture,没进行返回false
    '''
    global global_recursion_counter
    if global_recursion_counter >= 2:
        return True
    else:
        return False

def recursion_counter_if2():
    '''
    判断是否继续进行穿刺
    :return:
    '''
    global global_recursion_counter
    if global_recursion_counter >= 3:
        return False
    else:
        return True


def company_getter(company_name, index_num):
    global global_company_name
    global global_index_num
    global_company_name = company_name
    global_index_num = index_num





def recursion_counter_if3():
    '''
    如果是母公司，return True，不是就return False
    :return:
    '''
    global global_recursion_counter
    if global_recursion_counter == 0:
        return True
    else:
        return False












def verify_result_output(cn_table):
    temp_table = copy.deepcopy(gm.global_person_table)
    result_table = pd.merge(cn_table, temp_table, how="right", on=["客户姓名", "公司全称"])
    file_name = "result\\" + global_index_num + "_" + global_company_name + "output.xlsx"
    result_table.to_excel(file_name, index=None)
    pass


if __name__ == '__main__':
    shareholder_list1 = [["a1","b1"],["a2","b2"],["a3","b3"]]
    key_person_list3 = [["c1", "d1"], ["d2", "d2"], ["d3", "d3"],["d4", "d4"]]
    ratio_list2 = ["g1", "g2", "g3"]
    company_name = "test"
