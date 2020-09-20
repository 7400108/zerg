"""
Created by 饼干 on 2020/9/20 14:04
"""
import re
import gzip
from io import BytesIO
from urllib import request
__author__ = '饼干'

class Spider():
    url = 'https://www.douyu.com/g_wzry'
    root_pattern = '<div class="DyListCover-info">([\s\S]*?)</h2>'
    name_pattern = '<div class="DyListCover-userName is-template">([\s\S]*?)</div>'
    number_patter = '</svg>([\s\S]*?)</span>'
    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        htmls = r.read()
        # 返回的HTML字节码是b 开头的 是gzip压缩过的
        buff = BytesIO(htmls)
        # 解压缩
        f = gzip.GzipFile(fileobj=buff)
        htmls = f.read().decode('utf-8')
        return htmls


    def __analysis(self, htmls):
        """ 正则取值 封装数据 字典格式"""
        root_html = re.findall(Spider.root_pattern, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_patter, html)
            anchor = {'name': name, 'number': number}
            anchors.append(anchor)
        return anchors


    def __refine(self, anchors):
        """ 优化字典数据 """
        l = lambda anchor: {'name': anchor['name'][0].strip(), 'number': anchor['number'][0]}
        return map(l, anchors)

    def __sort(self, anchors):
        """ 排序 """
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    def __sort_seed(self, anchor):
        """ 排序key"""
        r = re.findall('\d*', anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number

    def __show(self, anchors):
        """ 展示数据 """
        for anchor in anchors:
            print(anchor['name'] + '-----' + anchor['number'])

    def go(self):
        """ 主方法函数 """
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)
        print(anchors)

spider = Spider()
spider.go()