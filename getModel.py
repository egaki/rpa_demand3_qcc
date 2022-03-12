#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/5 11:10
# @Author  : YoumingDong
# @File    : 20220205 get_def.py
# @Software: win10  python3.9
import pandas as pd
import rpa as r
import UrlModel as um
import OutputModel as op

# # 全局变量 用于记录递归次数
# global_recursion_counter = 1


global_person_table = None  # 每一家公司都有一个对应的结果表
global_over_flag = 0    # 0表示不受影响，若为1则程序可以立刻终止


def get_person_list(person_list, company_name):
    '''
    初始化 global_person_table
    :param person_list:
    :param company_name:
    :return:
    '''
    global global_person_table
    flag = [0 for i in range(len(person_list))]
    reason = ["未查询到此人" for i in range(len(person_list))]
    global_person_table = pd.DataFrame(columns=["公司全称","客户姓名","是否通过1:通过","原因"])
    global_person_table["客户姓名"] = person_list
    global_person_table["是否通过1:通过"] = flag
    global_person_table["原因"] = reason
    global_person_table["公司全称"] = company_name
    # shareholder = "杨虎"
    # person_verify(shareholder)
    pass


def person_verify(shareholder, type):
    '''
    写入模板
    :param shareholder:
    :param type: 为何种原因被命中
    :return:
    '''
    global global_person_table
    temp_bool = (global_person_table["客户姓名"] == shareholder)
    global_person_table.loc[temp_bool, ["是否通过1:通过"]] = 1
    if type == "股东":
        global_person_table.loc[temp_bool, ["原因"]] = "公司股东"
    elif type == "主要人员":
        global_person_table.loc[temp_bool, ["原因"]] = "公司主要人员"

    if all(global_person_table["是否通过1:通过"] == 1):
        # 转换终止指令
        can_over()
    # if temp_bool






def if_listed_company():
    '''
    判断是否是上市公司
    :return: 如果是返回True ,如果不是返回false
    '''
    text1 = um.get_text("body > div > div.company-detail > div:nth-child(4) > div > div > div.nav-head > a:nth-child(1) > h2")
    # shareholder_name.find('有限合伙') != -1
    if text1.find("上市信息") != -1 or text1.find("申报信息") != -1:
        return True
    else:
        return False



def executive_distinguish():
    '''
    解决工商登记问题
    :return:返回正确的css
    '''
    # dom = 0  时，就是返回空
    # #mainmember > div:nth-child(3) > div.app-ntable > table > tr:nth-child(2) > td.left > div > span.cont > span > a
    r.dom("a229 = 0")
    # r.dom("if (document.querySelector('#partner > div:nth-child(2) > div.app-tree-table > table > tr:nth-child(2) > td.left.first-td > div.td-coy.ipo-partner-app-tdcoy > span.cont > span > a')){a229 = 1}")
    r.dom(
        "if (document.querySelector('#mainmember > div:nth-child(3) > div.app-ntable > table > "
        "tr:nth-child(2) > td.left > div > span.cont > span > a')){a229 = 1}")
    # r.dom("if ('#mainmember > div:nth-child(3) > div.app-ntable > table > tr:nth-child(2) > td.left > div > span.cont > span > a'){a229 = 1}")
    lable = r.dom("return a229")
    if lable != '1':
        css_selector = "#mainmember > div > div.app-ntable > table > tr> td.left > div > span.cont > span"
        return css_selector
    else:
        css_selector = "#mainmember > div:nth-child(2) > div.app-ntable > table > tr > td.left > div > span.cont > span > a"
        return css_selector


def get_executive():
    '''
    获取主要人员
    :return: [ ["顾敏","董事长,法定代表人"], ["李南青","总经理,董事"] ]
    '''
    # #mainmember > div:nth-child(2) > div.app-ntable > table > tr:nth-child(2) > td.left > div > span.cont > span > a
    css_orign = executive_distinguish() # "#mainmember > div > div.app-ntable > table > tr> td.left > div > span.cont > span"
    num = um.get_num(css_orign)  # if num = 5 [ [],[],[],[],[],
    if num != '':
        num = int(num)
        result = []
        # #mainmember > div:nth-child(2) > div.app-ntable > table > tr:nth-child(2) > td:nth-child(5) > span
        if if_listed_company():
            for index in range(2, 2 + num):
                css_temp1 = "#mainmember > div > div.app-ntable > table > tr:nth-child(" + str(index) + ") > td.left > div > span.cont > span"
                mainmember = r.read(css_temp1)
                person_verify(mainmember,"主要人员")    # 判断是否命中
                if if_can_over():   # 如果已经全部命中，则立刻返回
                    return True

                if mainmember != '':
                    css_temp2 = "#mainmember > div > div.app-ntable > table > tr:nth-child(" + str(index) + ") > td:nth-child(5)"
                    mainmember_job = r.read(css_temp2)
                    result.append([mainmember, mainmember_job])
                else:
                    pass
            return result
        else:
            for index in range(2, 2 + num):
                css_temp1 = "#mainmember > div > div.app-ntable > table > tr:nth-child(" + str(index) + ") > td.left > div > span.cont > span"
                mainmember = r.read(css_temp1)
                if mainmember != '':
                    css_temp2 = "#mainmember > div > div.app-ntable > table > tr:nth-child(" + str(index) + ") > td:nth-child(3)"
                    mainmember_job = r.read(css_temp2)
                    result.append([mainmember, mainmember_job])
                else:
                    pass
            return result
    else:
        return []

    # 主要人员姓名
    # mainmember > div > div.app-ntable > table > tr:nth-child(2) > td.left > div > span.cont > span
    # mainmember > div > div.app-ntable > table > tr:nth-child(3) > td.left > div > span.cont > span
    # mainmember > div > div.app-ntable > table > tr:nth-child(2) > td.left > div > span.cont > span
    # #mainmember > div > div.app-ntable > table > tr> td.left > div > span.cont > span
    # 主要人员职务
    # mainmember > div > div.app-ntable > table > tr:nth-child(2) > td:nth-child(3)
    # mainmember > div > div.app-ntable > table > tr:nth-child(3) > td:nth-child(3)
    # mainmember > div > div.app-ntable > table > tr:nth-child(4) > td:nth-child(3)
    # mainmember > div > div.app-ntable > table > tr:nth-child(5) > td:nth-child(3)
    # #mainmember > div > div.app-ntable > table > tr > td:nth-child(3)



# 正常的
# #partner > div.tablist > div.app-tree-table > table > tr:nth-child(2) > td.left > div > span.cont > span > a
# #partner > div:nth-child(3) > div.sub-section > div > div.app-ntable > table > tr:nth-child(2) > td.left > div > span.cont > span > a

# 最新公示
# #partner > div:nth-child(2) > div.app-tree-table > table > tr:nth-child(2) > td.left.first-td > div.td-coy.ipo-partner-app-tdcoy > span.cont > span > a
# 工商登记
# #partner > div:nth-child(3) > div.app-tree-table > table > tr:nth-child(2) > td.left.first-td > div.td-coy.partner-app-tdcoy > span.cont > span > a

def shareholder_distinguish():
    # dom = 0  时，就是返回空
    r.dom("a229 = 0")
    r.dom("if (document.querySelector('#partner > div:nth-child(2) > div.app-tree-table > table > tr:nth-child(2) > td.left > div > span.cont > span > a')){a229 = 1}")
    lable = r.dom("return a229")
    if lable != '1':
        css_selector = "#partner > div > div.app-tree-table > table > tr > td.left > div > span.cont > span"
        return css_selector
    else:
        css_selector = "#partner > div:nth-child(2) > div.app-tree-table > table > tr > td.left > div > span.cont > span"
        return css_selector

def get_shareholder_num():
    css_selector = shareholder_distinguish()
    a = um.get_num(css_selector)
    num = int(a)
    return num

def if_can_get(company_name):
    '''
    自动识别矫正器
    :param company_name:
    :return:
    '''
    css_selector = shareholder_distinguish()
    num_flag = 0
    for i in range(3):
        try:
            a = um.get_num(css_selector)
            num = int(a)
        except ValueError:
            # 如果加载全了，还不能获取，就返回False
            if um.if_complete() and (not op.recursion_counter_if3()):
                print("!!!!!")
                print(company_name + "疑似出现问题,但已经跳过。")
                print("!!!!!")
                return company_name
            print("shareholder获取失败，正在重新尝试")
            if i < 2:
                r.wait(5)
        else:
            num_flag = 1
            break
    if num_flag == 0:
        print("shareholder获取失败，已退回" + company_name + "疑似出现问题。")
        int("")
    # 正常情况下，return True
    return True

# #partner > div.tablist > div.app-tree-table > table > tr:nth-child(2) > td.left > div > span.cont > span > span
def get_shareholder():
    '''
    return [ [zxy,a],[dym,a]]
    '''
    num = get_shareholder_num()
    result = []
    for index in range(2, 2 + num):
        css_temp = "#partner > div.tablist > div.app-tree-table > table > tr:nth-child(" + str(index) + ") > td.left > div > span.cont > span"
        shareholder = r.read(css_temp)
        person_verify(shareholder, "股东")
        if if_can_over():
            return True
        if shareholder != '':
            css_temp = "#partner > div.tablist > div.app-tree-table > table > tr:nth-child(" + str(index) + ") > td.left > div > span.cont > span > a"
            get_url = um.get_url_cssSelector(css_temp)
            result.append([shareholder, get_url])
        else:
            pass
    return result


def over_flag_init():
    global global_over_flag
    global_over_flag = 0


def can_over():
    global global_over_flag
    global_over_flag = 1


def if_can_over():
    '''
    判断程序是否可以终止，
    :return: 如果可以终止返回true,如果不可以终止，返回false
    '''
    global global_over_flag
    if global_over_flag == 0:
        return False
    else:
        return True

if __name__ == '__main__':
    r.tagui_location(r"D:")
    r.init()
    #url_init = r'https://www.qcc.com/firm/5b75938e604b0bf4b69fddb016339b70.html'  #深圳市信丰网物流有限公司
    url_init = r'https://www.qcc.com/firm/81d02fee056d6bb632440d29114f616f.html'  #佛山信仁货运代理有限公司
    #url_init = r'https://www.qcc.com/firm/bf69a9651df2bae5ffbf2219848387bf.html' #深圳市丰捷信物流有限公司

    # 实例化谷歌设置选项

    r.url(url_init)  # 打开网页了
    r.wait(8)  # 等待

    print(get_executive())
    # print(get_shareholding_ratio())
    print(get_shareholder())





def get_shareholding_ratio():
    '''

    :return: ["40%","50%",]
    '''
    # partner > div.tablist > div.app-tree-table > table > tr:nth-child(2) > td:nth-child(3)
    # #partner > div.tablist > div.app-tree-table > table > tr:nth-child(2) > td:nth-child(3)
    # #partner > div.tablist > div.app-tree-table > table > tr:nth-child(3) > td:nth-child(3)
    css_selector = shareholder_distinguish()
    num = int(um.get_num(css_selector))
    result = []
    for index in range(2, 2 + num):
        # css_temp = "#partner > div.tablist > div.app-tree-table > table > tr:nth-child(" + str(index) + ") > td:nth-child(3)"
        # shareholding_ratio = r.read(css_temp)
        # if shareholding_ratio != '':
        #     shareholding_ratio = shareholding_ratio.split("%",1)[0]
        #     result.append(shareholding_ratio)
        # else:
        #     pass
        result.append("-")
    return result
