# -*- coding: utf-8 -*-
# @Time    : 9/20/2020 4:21 PM
# @Author  : Romi
# @FileName: elm_spider_fiddler.py
# @Software: PyCharm
# @Comment ：利用fiddler抓包的方法对elm商品信息进行爬虫

import json
import pandas as pd

r'''
#查看文件编码
import chardet
path = r"C:\Users\Smile\Downloads\elm_Response.txt"
f = open(path,'rb')
data = f.read()
print(chardet.detect(data))
'''

with open(r"C:\Users\Smile\Downloads\elm_Response.txt",'r',encoding='UTF-16',errors='ignore') as f:
    jsonlines=f.readlines()
    goods_name=[]
    goods_currentprice=[]
    goods_orginalprice=[]
    goods_salesunit=[]


for jsondata in jsonlines:
    if jsondata not in ['\n','Response code: 200\n']:
        jsondata=jsondata.replace('Response body: ','')
        data = json.loads(jsondata)
        foods_list=data['data']['data'][0]['foods']
        for detail_info in foods_list:
            name=detail_info['name']
            currentprice=detail_info['currentPrice']
            saleunit=detail_info['defaultSaleUnit']
            org_price=detail_info['originalPrice']
            goods_name.append(name)
            goods_currentprice.append(currentprice)
            goods_orginalprice.append(org_price)
            goods_salesunit.append(saleunit)


total={}
total['商品']=goods_name;total['现价']=goods_currentprice;total['原价']=goods_orginalprice;total['售卖单位']=goods_salesunit
data_final=pd.DataFrame(total)
print(data_final)