# -*- coding: utf-8 -*-
# @Time    : 12/5/2021 9:41 PM
# @Author  : Romain 
# @FileName: zhihu_spider.py
# @Software: PyCharm
# @Comment ：知乎爬虫

import requests
import json
import re

#请求特定的URL并返回请求内容
def request_url(url,self_header):
    try:
        response = requests.get(url,headers=self_header,timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        return ""

#对返回的josn进行解析并提取所有的回答数据
def all_answer(content):
    con = json.loads(content)

    answers = [item["content"] for item in con["data"]]
    for answer in answers:
        # 原回答中带有html标签，利用正则表达式去除
         answer = re.sub("<.*?>", "", answer)
         print(answer)

if __name__=='__main__':
    self_header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    for offsetnum in range(109):
        url = "https://www.zhihu.com/api/v4/questions/490840493/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=" + str(offsetnum) + "&platform=desktop&sort_by=default"
        content=request_url(url, self_header)
        all_answer(content)