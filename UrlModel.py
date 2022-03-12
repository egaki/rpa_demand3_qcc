#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/5 11:16
# @Author  : YoumingDong
# @File    : UrlModel.py
# @Software: win10  python3.9
import rpa as r


def if_complete():
    '''
    判断界面是否加载成功
    :return: 加载成功返回True
    '''
    state = r.dom('''return document.readyState=="complete"''')
    if state == "true":
        return True
    else:
        return False
    # r.dom("a229 = 'False'")
    # r.dom('''
    #     if (document.readyState=="complete"){a229 = 'True'}
    # ''')
    # state = r.dom("return a229")


def wait_complete(wait_seconds=15):
    '''
    如果这个界面加载完，就停止等待，最大等待wait_seconds
    :param wait_seconds:
    :return:
    '''
    flag = 0
    for i in range(wait_seconds):
        if if_complete():
            flag = 1
            break
        else:
            r.wait(1)
    if flag == 0:
        return False

    return True



def go_href(url):
    r.url(url)  # 打开网页了
    max_wait_time = 15  # 最大等待时间
    for i in range(max_wait_time):
        if if_complete():
            break
        else:
            r.wait(1)



def get_url_cssSelector(css):
    '''
    通过selector 获取超链接
    :param css:
    :return:
    '''
    # tr:nth-child(1) > td:nth-child(3) > div > div.app-copy-box.copy-hover-item > span.copy-title > a
    js1 = '''element = document.querySelector(' ''' + css +"')"
    js2 = '''return element.href'''
    r.dom(js1)
    url = r.dom(js2)
    return url


def get_num(css):
    '''
    通过css selector 获取有多少符合的元素【数量】
    :param css:
    :return: num 有多少个命中该css的元素
    '''
    js1 = "a = document.querySelectorAll('" + css + "')"
    r.dom(js1)
    num = r.dom('''return a.length''')
    return num


def get_text(css):
    js1 = "a = document.querySelector('" + css + "')"
    r.dom(js1)
    text = r.dom('''return a.textContent''')    # ""
    return text


def get_url_xpath(xpath):
    result = r.read(xpath+"/@href")
    return result



def go_back():
    # r.dom("window.location.href = document.referrer")
    r.dom("window.history.back(-1)")
    max_wait_time = 15
    for i in range(max_wait_time):
        if if_complete():
            break
        else:
            r.wait(1)


def my_click(css_selector):
    r.click(css_selector)
    wait_complete(15)


def w_close():
    r.dom("window.close()")



if __name__ == '__main__':
    r.tagui_location(r"D:")
    r.init()
    r.url("www.qcc.com")
    print(if_complete())
    r.wait(6)
    print(if_complete())
    r.wait(3)
    r.url("https://www.qcc.com/web/search?key=%E4%B8%AD%E5%9B%BD%E9%93%B6%E8%A1%8C")

    r.wait(6)
    go_back()
    # a = get_url_cssSelector('tr:nth-child(1) > td:nth-child(3) > div > div.app-copy-box.copy-hover-item > span.copy-title > a')
    # r.url("https://www.qcc.com/firm/cdb52314af5aa8f7889d8f72c800ee6f.html")
    # r.wait(5)
    # b = get_num("#partner > div.tablist > div.app-tree-table > table.ntable > tr > td.left > div > span.cont > span > a")
    pass



def get_url1(xpath):
    '''
    旧版
    '''
    js5 = "element = document.evaluate('" + xpath + "',document).iterateNext()"
    r.dom(js5)
    js6 = '''return element.href'''
    result = r.dom(js6)

    js7 = "return document.evaluate('" + xpath + "',document).iterateNext()"
    result2 = r.dom(js7)
    js1_1 = '''//DOM加载时加载testXpath
    addLoadEvent(testXpath)
    function testXpath(){
            getElementByXpath("/html/body/button").onclick = function(){
            var element = getElementByXpath("/html/body/select");//获取到select元素
            var index = element.selectedIndex;//获取元素下标
            console.log(element.options[index].text);
        }
    }'''
    js1_1 = '''testXpathaddLoadEvent(testXpath)function testXpath(){getElementByXpath("/html/body/button").onclick = function(){var element = getElementByXpath("/html/body/select");var index = element.selectedIndex;console.log(element.options[index].text);}}'''

    js1_2 = '''function addLoadEvent(func) {
        var oldonload = window.onload;
        if (typeof window.onload != 'function') {
            window.onload = func;
        } else {
            window.onload = function() {
                oldonload();
                func();
          }
        }
    }'''
    js1_3 = '''function getElementByXpath(xpath){
        var element = document.evaluate(xpath,document).iterateNext();
        return element;
    }
    '''
    r.dom(js1_1)
    r.dom(js1_2)
    r.dom(js1_3)
    js2 = "a_23 = getElementByXpath('" + xpath + "')"
    r2 = r.dom(js2)
    js3 = "return a_23.href"
    result = r.dom(js3)


    return result