#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/18 16:54
# @Author  : YoumingDong
# @File    : verifyModel.py
# @Software: win10  python3.9
import rpa as r
import UrlModel as um
import getModel as gm


# TODO 判断公司是否合规，并且将结果送进结果栏
def company_qualification_verify():
    reason = ""
    if_pass = True
    if if_abnormal() is not True:
        reason += "error1:企业被吊销或注销\n"
        if_pass = False
    if if_Executee() is not True:
        reason += "error2:企业经营异常或为被执行人\n"
        if_pass = False

    temp_flag = enterprise_type()
    if temp_flag is not True:
        reason += "error3:"+ temp_flag + "\n"
        if_pass = False

    temp_flag2 = registered_capital()
    if temp_flag2 is not True:
        reason += "error3:"+ temp_flag2 + "\n"
        if_pass = False

    temp_flag3 = insured_persons()
    if temp_flag3 is not True:
        reason += "error3:" + temp_flag3 + "\n"
        if_pass = False

    if if_pass is True:
        return True
    else:
        verify_result_out(reason)
        return False

def verify_result_out(reason):
    '''
    写入模板
    :param shareholder:
    :param type: 为何种原因被命中
    :return:
    '''
    gm.global_person_table["是否通过1:通过"] = 0
    gm.global_person_table["原因"] = reason



    # if temp_bool


def if_abnormal():
    '''
    判断企业是否经营吊销或者注销
    :return: 正常：True 异常：返回False
    '''
    text = um.get_text("body > div:nth-child(2) > div.company-detail > div.company-header > div > div.nheader > div.infos.clearfix > div.content > div:nth-child(1) > div > div > span:nth-child(1) > span")
    #print(text)
    if text.find("吊销") != -1 or text.find("注销") != -1:
        # string_object.find(sub, start, end)
        # 如果字符串string_object中包含sub，则返回sub在string_object中起始的位置索引，否则返回-1.
        return False
    else:
        return True

def if_Executee():
    '''
    判断是否为经营异常或者被执行人
    :return:
    '''
    # css_temp = "div > div.company-detail > div.company-header > div > div.nheader.normalcom > div.infos.clearfix > div.content > div.tags-wrap > div.tags > span > span"
    r.dom(''' temp_char = "a" ''')
    r.dom(''' a = document.querySelectorAll('body > div:nth-child(2) > div.company-detail > div.company-header > div > 
    div.nheader.normalcom > div.infos.clearfix > div.content > div.tags-wrap > div.tags > span > span')''')
    r.dom('''for (var i=0;i<a.length;i++){ temp_char = temp_char + a[i].textContent;}''')
    text = r.dom(" return temp_char")
    # print(text)
    if text.find("经营异常") != -1 or text.find("被执行人") != -1:
        return False
    else:
        return True



    #注册资本
    # #cominfo > div:nth-child(2) > table > tr:nth-child(3) > td:nth-child(2)
    # #cominfo > div:nth-child(2) > table > tr:nth-child(3) > td:nth-child(2)
    # #socominfo > table > tr:nth-child(2) > td:nth-child(2)
    #人员规模
    # #cominfo > div:nth-child(2) > table > tr:nth-child(7) > td:nth-child(2)
    # #cominfo > div:nth-child(2) > table > tr:nth-child(7) > td:nth-child(2)
    #参保人数
    # #cominfo > div:nth-child(2) > table > tr:nth-child(7) > td:nth-child(4) > span
    # #cominfo > div:nth-child(2) > table > tr:nth-child(7) > td:nth-child(4) > span
    #企业类型
    # #cominfo > div:nth-child(2) > table > tr:nth-child(5) > td:nth-child(2)
    # #cominfo > div:nth-child(2) > table > tr:nth-child(5) > td:nth-child(2)

def enterprise_type():
    css_temp = "#cominfo > div:nth-child(2) > table > tr:nth-child(5) > td:nth-child(2)"
    enterprise_type = r.read(css_temp)
    if enterprise_type == "个体工商户":
        return "异常：该企业为个体工商户，未能通过校验！"
    else:
        return True

def registered_capital():
    capital = um.get_text( "#cominfo > div:nth-child(2) > table > tr:nth-child(3) > td:nth-child(2)")
    if capital == "-":
        return "人工：注册资本为空"
    elif capital.find("美元") != -1:
        # 2022/2/19日汇率：50万元人民币=7.905万美元
        capital1 = capital.split("万", 1)[0]
        if float(capital1) < 7.905:
            return "异常：注册资本 "+capital+" 小于50万！"
        else:
            return True
    elif capital.find("港元") != -1:
            # 2022/2/19日汇率：50万元人民币=61.66万港元
        capital1 = capital.split("万", 1)[0]
        if float(capital1) < 61.66:
            return "异常：注册资本 "+ capital +" 小于50万！"
        else:
            return True
    elif capital.find("台币") != -1:
            # 2022/2/19日汇率：50万元人民币=220.075万新台币
        capital1 = capital.split("万", 1)[0]
        if float(capital1) < 220.075:
            return "异常：注册资本 "+ capital +" 小于50万！"
        else:
            return True
    elif capital.find("人民币") != -1:
        capital1 = capital.split("万", 1)[0]
        if float(capital1) < 50:
            return "异常：注册资本 "+ capital +" 小于50万！"
        else:
            return True
    else:
        return "人工：特殊币种:" + capital


def insured_persons():
    css_temp = "#cominfo > div:nth-child(2) > table > tr:nth-child(7) > td:nth-child(4) > span"
    insured_persons = r.read(css_temp)
    # insured_persons_text = um.get_text("#cominfo > div:nth-child(2) > table > tr:nth-child(7) > td:nth-child(4) > span")
    # print(text)
    if insured_persons == "-":
        return "人工：参保人数为空"
    elif int(insured_persons) < 50:
        # print("参保人数：", insured_persons)
        return "异常：参保人数：" + insured_persons + " 少于50人！"
    else:
        # print("参保人数：", insured_persons)
        return True

if __name__ == '__main__':
    r.tagui_location(r"E:\python")
    r.init()
    #url_init = r'https://www.qcc.com/firm/5b75938e604b0bf4b69fddb016339b70.html'  #深圳市信丰网物流有限公司
    #url_init = r'https://www.qcc.com/firm/81d02fee056d6bb632440d29114f616f.html'  #佛山信仁货运代理有限公司
    #url_init = r'https://www.qcc.com/firm/bf69a9651df2bae5ffbf2219848387bf.html' #深圳市丰捷信物流有限公司
    #url_init = r'https://www.qcc.com/firm/4ce87073e5b41c70131acf03094e7a4c.html'#吊销、经营异常
    #url_init = r'https://www.qcc.com/firm/1090f61cde46ca4a896931146e4c98c4.html' #被执行人
    #url_init = r'https://www.qcc.com/firm/47917322d01035779f59cd8d22c3faf8.html' #存续、经营异常
    #url_init = r'https://www.qcc.com/firm/0c08dfdf5addbd7aac08134f05d2482a.html' #吊销、经营异常
    #url_init = r'https://www.qcc.com/firm/4d0d7bf037b29bca5cdfb55bc924e46b.html' #在业、经营异常
    #url_init = r'https://www.qcc.com/firm/4ce87073e5b41c70131acf03094e7a4c.html' #吊销、经营异常
    #url_init = r'https://www.qcc.com/firm/4ce3ed8d03dd9cdc56a67e3c144eb58a.html' #吊销、经营异常
    #url_init = r'https://www.qcc.com/firm/82983faea5c5fcaab1db71a396ff9875.html' #在业，个体工商户
    #url_init = r'https://www.qcc.com/firm/2f4d33b63fef02fd9a2aee5986eafc56.html' #存续，个体工商户
    #url_init = r'https://www.qcc.com/firm/f31412956564493e0f7ec60559b7d81d.html' #被执行人
    url_init = r'https://www.qcc.com/firm/5b615520c1c928bd85defd84a4e8c0c0.html' #美元

    r.url(url_init)
    r.wait(8)

    print(if_abnormal1())
    print(if_abnormal2())
    #print(if_Executee1())
    #print(if_Executee2())
    print(registered_capital())
    #print(personnel_scale())
    print(enterprise_type())
    print(insured_persons())




















def if_abnormal1():
    '''
    判断企业是否经营吊销或者注销
    :return: 正常：True 异常：返回False
    '''
    # body > div:nth-child(2) > div.company-detail > div.company-header > div > div.nheader > div.infos.clearfix > div.content > div:nth-child(1) > div > div > span:nth-child(1) > span
    # body > div:nth-child(2) > div.company-detail > div.company-header > div > div.nheader > div.infos.clearfix > div.content > div:nth-child(1) > div > div > span:nth-child(1) > span
    css_temp = "body > div:nth-child(2) > div.company-detail > div.company-header > div > div.nheader > div.infos.clearfix > div.content > div:nth-child(1) > div > div > span:nth-child(1) > span"
    state = r.read(css_temp)
    #print(state)
    if state == "吊销" or state == "注销" :
        return False
    else:
        return True


def if_Executee1():

    #被执行人
    #body > div:nth-child(2) > div.company-detail > div.company-header > div > div.nheader.normalcom > div.infos.clearfix > div.content > div.tags-wrap > div.tags > span:nth-child(2) > span
    #body > div > div.company-detail > div.company-header > div > div.nheader.normalcom > div.infos.clearfix > div.content > div.tags-wrap > div.tags > span:nth-child(2) > span
    #经营异常
    #body > div > div.company-detail > div.company-header > div > div.nheader.normalcom > div.infos.clearfix > div.content > div.tags-wrap > div.tags > span:nth-child(2) > span
    #body > div:nth-child(2) > div.company-detail > div.company-header > div > div.nheader.normalcom > div.infos.clearfix > div.content > div.tags-wrap > div.tags > span.ntag.text-primary > span
    #body > div > div.company-detail > div.company-header > div > div.nheader.normalcom > div.infos.clearfix > div.content > div.tags-wrap > div.tags > span:nth-child(1) > span
    #body > div:nth-child(2) > div.company-detail > div.company-header > div > div.nheader.normalcom > div.infos.clearfix > div.content > div.tags-wrap > div.tags > span.ntag.text-primary > span
    #body > div:nth-child(2) > div.company-detail > div.company-header > div > div.nheader.normalcom > div.infos.clearfix > div.content > div.tags-wrap > div.tags > span.ntag.text-primary > span
    #body > div:nth-child(2) > div.company-detail > div.company-header > div > div.nheader.normalcom > div.infos.clearfix > div.content > div.tags-wrap > div.tags > span:nth-child(2) > span
    #综合
    #body > div > div.company-detail > div.company-header > div > div.nheader.normalcom > div.infos.clearfix > div.content > div.tags-wrap > div.tags > span > span

    text = um.get_text( "div > div.company-detail > div.company-header > div > div.nheader.normalcom > div.infos.clearfix > div.content > div.tags-wrap > div.tags > span > span")
    #print(text)
    if text.find("经营异常") != -1 or text.find("被执行人") != -1:
        return False
    else:
        return True

def if_Executee2():
    css_temp = "div > div.company-detail > div.company-header > div > div.nheader.normalcom > div.infos.clearfix > div.content > div.tags-wrap > div.tags > span > span"
    state = r.read(css_temp)
    print(state)
    if state == "经营异常" or state == "被执行人":
        return False
    else:
        return True