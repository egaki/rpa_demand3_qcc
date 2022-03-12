#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/3 12:05
# @Author  : YoumingDong
# @File    : 20220203rpa_test.py
# @Software: win10  python3.9

# UTF-8 u3467

import rpa as r
import pandas as pd
import UrlModel as um
import getModel as gm
import OutputModel as op
import verifyModel as vm
import os

global_company_error_list = []



def edge_on():
    '''
    浏览器启动
    :return:
    '''
    r.tagui_location(r"D:")
    r.init()
    r.url("www.baidu.com")


# TODO 拟人化
def search_name(company_name):
    '''
    从主页开始查 某个company_name
    :param diver:
    :param company_name:
    :return:
    '''

    url_init = r'https://www.qcc.com/'  # 网址

    # 实例化谷歌设置选项

    um.go_href(url_init)
    r.wait(1)
    r.type("#searchKey", company_name)
    r.wait(2)
    um.my_click('body > div > div.app-home > section.nindex-search > div > div > div > div.app-search-input.big > div > div > span > button')
    url2 = um.get_url_cssSelector("tr:nth-child(1) > td:nth-child(3) > div > div.app-copy-box.copy-hover-item > span.copy-title > a")
    # um.my_click("tr:nth-child(1) > td:nth-child(3) > div > div.app-copy-box.copy-hover-item > span.copy-title > a")

    um.go_href(url2)
    if gm.if_listed_company():
        r.click("body > div > div.company-detail > div:nth-child(4) > div > div > div.nav-head > a:nth-child(2) > h2")
    pass


def shareholder_output(shareholder_list1, ratio_list2):
    for a,b in zip(shareholder_list1, ratio_list2):
        print(a[0] + ":" + b + "\n")


def key_person_output(key_person_list3):
    for key_person in key_person_list3:
        print(key_person[0] + ":" + key_person[1] + "\n")


def shareholder_main(company_name):
    print("START-" + company_name + "-START")
    op.recursion_counter_up()


    shareholder_list1 = gm.get_shareholder()
    if gm.if_can_over() is True:
        return True
    # ratio_list2 = gm.get_shareholding_ratio()
    key_person_list3 = gm.get_executive()
    if gm.if_can_over() is True:
        return True

    # shareholder_output(shareholder_list1, ratio_list2, key_person_list3)
    # key_person_output(key_person_list3)
    # op.result_output(shareholder_list1, key_person_list3,company_name)

    for element in shareholder_list1:
        shareholder_name = element[0]
        href = element[1]
        # print(executive)
        if (shareholder_name.find('有限合伙') != -1) and (op.recursion_counter_if2()):
            # search_name(driver, shareholder_name)
            um.go_href(href)
            probe = gm.if_can_get(shareholder_name)
            if probe is True:
                shareholder_main(shareholder_name)
                if gm.if_can_over() is True:    # 终止信号判断
                    return True
            else:
                global global_company_error_list
                global_company_error_list.append(probe)
                pass
        else:
            pass
    print("FINISH-" + company_name + "-FINISH")
    op.recursion_counter_down()
    um.go_back()
    pass


def company_selector(index1, index2):
    index1 -= 1
    index2 -= 1
    sub_company = cn_table[index1:index2]
    company_name = sub_company["公司全称"]
    index_num = sub_company["序号"]
    sub_bank = sub_company["管辖支行"]
    return company_name, index_num, sub_bank


def company_selector2(index1):
    index1 = [x-1 for x in index1]
    sub_company = cn_table.iloc[index1,:]
    company_name = sub_company["公司全称"]
    index_num = sub_company["序号"]
    sub_bank = sub_company["管辖支行"]
    return company_name, index_num, sub_bank


def index_maker(cn_table):
    index_path = r"data/temp_index.xlsx"
    if os.path.exists(index_path):
        temp_index = pd.read_excel(index_path, dtype='string')
        company_name_list = temp_index["公司全称"]
        index_num = temp_index["运行编号"]
        return company_name_list, index_num
    else:
        company_name_list = cn_table["公司全称"].drop_duplicates()
        index_num = [x for x in range(len(company_name_list))]
        temp_index = pd.DataFrame(columns=["运行编号", "公司全称"])
        temp_index["公司全称"] = company_name_list
        temp_index["运行编号"] = index_num
        temp_index.to_excel(index_path, index=None)
        return company_name_list, index_num



if __name__ == '__main__':

    excel_path = r"data/样板.xlsx"
    cn_table = pd.read_excel(excel_path, dtype='string')



    company_name_list, index_num_list = index_maker(cn_table)

    edge_on()
    error_list = []

    for company_name, index_num in zip(company_name_list, index_num_list):
        index_num  = str(index_num)
        temp_table = cn_table[cn_table["公司全称"] == company_name]

        person_list = temp_table["客户姓名"]


    ##########初始化模块###########
        # 初始化结果输出表
        gm.get_person_list(person_list, company_name)
        # 初始化递归次数、母公司名称与序号
        op.recursion_counter_init()
        op.company_getter(company_name, index_num)
        # 初始化结束标志
        gm.over_flag_init()

        try:
            print("运行编号：" + index_num + "-" + company_name + " 开始获取")
            search_name(company_name)   # 查公司
            if vm.company_qualification_verify():
                shareholder_main(company_name)
            else:
                pass
            op.verify_result_output(cn_table)   # 结果输出
        except ValueError as error_result:
            print(company_name + ":error,请重试")
            print(error_result)
            error_list.append(index_num)
            os.system("a.wav")
            r.close()
            r.wait(5)
            edge_on()
            r.wait(10)
        else:
            print("运行编号：" + index_num + "-" + company_name + " 获取完成！")
        print("当前错误序号：")
        print(error_list)
        print(global_company_error_list)


    pass




# CSS selector :#partner > div.tablist > div.app-tree-table > table > tr:nth-child(2) > td.left.first-td > div.td-coy.partner-app-tdcoy > span.cont > span > a

#XPath  //*[@id="partner"]/div[2]/div[2]/table/tr[2]/td[2]/div[1]/span[2]/span/a