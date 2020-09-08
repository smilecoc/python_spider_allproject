#Bilibili每日热榜爬虫

import re
import requests
from  openpyxl import  Workbook


def get_html_text(url,self_header):
    try:
        response = requests.get(url,headers=self_header,timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        #print(response.text)
        return response.text
    except:
        return ""

def re_get_inf(html):
    list=[]
    rank_list=re.findall(r'<div class="num">(\d*)</div>',html)
    title_list=re.findall(r'<div class="info"><a href=[\s\S]*?class="title">([\s\S]*?)</a><!---->',html)
    play_num=re.findall(r'<div class="detail"><span class="data-box"><i class="b-icon play"></i>(\d*.\d*)\S</span>',html)
    author_list=re.findall(r'<span class="data-box"><i class="b-icon author"></i>([\s\S]*?)</span>',html)
    wb=Workbook()
    sheet=wb.active
    sheet.append(['rank','title','playnum','author'])
    for i in range(len(rank_list)):
        rank = rank_list[i]
        title = title_list[i]
        playnum=play_num[i]
        author=author_list[i]
        sheet.append([rank,title,playnum,author])
    wb.save('bilibili_rankdata.xlsx')

def main():
     bilibili_url='https://www.bilibili.com/ranking/all/0/0/3'
     self_header = {
       "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
     }
     html=get_html_text(bilibili_url,self_header)
     re_get_inf(html)


if __name__ == '__main__':
   main()
