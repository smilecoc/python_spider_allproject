# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 17:43
# @Author  : Smilecoc
# @FileName: maoyan_top100.py
# @Software: PyCharm
# @Comment : 猫眼电影Top 100爬虫并写入csv


import requests
import re
import csv

# 获取html信息，并进行异常处理.status_code为200表示请求成功
def get_html_text(url, header):
    try:
        response = requests.get(url, headers=header, timeout=30)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            print("请求成功")
            return response.text
    except requests.exceptions.RequestException:
        print("请求失败，请检查网络条件或重新运行")



# Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
# yield生成迭代对象
# 利用正则表达式解析HTML获取信息
def get_info_from_htmltext(html):
    pattern = re.compile('.*?board-index.*?>(\d+)</i>'
                         + '.*?<p class="name"><.*?>(.*?)</a></p>'
                         + '.*?<p class="star">(.*?)</p>'
                         + '.*?<p class="releasetime">(.*?)</p>'
                         + '.*?<p class="score"><i class="integer">(.*?)</i><i class="fraction">(.*?)</i></p>', re.S)
    infomation = re.findall(pattern, html)
    for info in infomation:
        # 构造生成器函数,生成迭代对象
        yield {
            '排名': info[0],
            '电影名称': info[1],
            '主演': info[2].strip()[3:],#去除空格与换行符
            '上映时间': info[3].strip()[5:],
            '评分': info[4] + info[5]
        }


#数据写入csv中
def save_data(data):
    with open('miaoyan_top_100_film.csv', 'a', newline='', encoding='utf-8-sig', errors='ignore') as f:
        csv_file = csv.writer(f)
        csv_file.writerow([data['排名'], data['电影名称'], data['主演'], data['上映时间'], data['评分']])


def main(page):
    url = "https://maoyan.com/board/4?offset=" + str(page * 10)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "cookie": "__mta=217946409.1602755224603.1602820125740.1602820410838.8; uuid_n_v=v1; uuid=37FEFDA00ECB11EBB74D8BF51EFE42AFB5B820214EE9447685C70B6F27096D57; _csrf=a69c3c1dd1c13dad15868d1d821fac56d68691a1af9466e3534930fadceea199; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1602755166; _lxsdk_cuid=17356de2b62c8-0c5a381c554641-4353760-100200-17356de2b62c8; _lxsdk=37FEFDA00ECB11EBB74D8BF51EFE42AFB5B820214EE9447685C70B6F27096D57; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1602820411; _lxsdk_s=1752f852f16-684-f32-ead%7C%7C11"
    }
    html = get_html_text(url, header)
    for one_page_data in get_info_from_htmltext(html):
        print(one_page_data)
        save_data(one_page_data)


if __name__ == '__main__':
    for i in range(10):
        main(i)

