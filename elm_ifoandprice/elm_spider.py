# -*- coding: utf-8 -*-
# @Time    : 2020/4/22 18:04
# @FileName: elm_spider.py
# @Software: PyCharm
# @Comments: 饿了么爬虫，爬取商品信息与价格

import re
import pandas as pd

#读取本地的html文件
path=r"C:\Users\Desktop\test.html"
fp = open(path,'rb')
html = fp.read().decode('utf-8')

#对html进行解析
#([\s\S]*使用正则提取所有的字符串，？表示使用使用非贪婪模式
goodslist=re.findall(r'<div class="name" data-s-2fa74f50fceca7d0683c7058722358a8="">([\s\S]*?)</div>',html)
#-?\d+\.?\d*e?-?\d*？提取所有的数字，包括小数
currentpricelist=re.findall(r'￥</span>(-?\d+\.?\d*e?-?\d*?)</div>',html)

#将list转为datafarme
goods=pd.DataFrame(goodslist)
currentprice=pd.DataFrame(currentpricelist)
#横向拼接
result=pd.concat([goods,currentprice],axis=1)
#更改dataframe列名称
result.columns=['商品名','现价']
#保存文件
result.to_excel(r"C:\Users\Desktop\result.xlsx",index=None)

