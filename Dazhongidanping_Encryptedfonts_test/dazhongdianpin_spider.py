'''
大众点评爬虫，实现文字加密下的爬取
'''
from fontTools.ttLib import TTFont
import requests

def get_font():
    font = TTFont(r"C:\Users\smile\Downloads\7691db5b.woff")
    font_names = font.getGlyphOrder()

    # 这些文字就是在FontEditor软件打开字体文件后看到的文字名字
    texts = ['','、','1','2','3','4','5','6','7','8','9','0', '','']

    font_name = {}
    # 将字体名字和它们所对应的乱码构成一个字典

    for index,value in enumerate(texts):
        a = font_names[index].replace('uni', '&#x').lower() + ";"
        font_name[a] = value
    print(font_name)
    return font_name


def get_html_text():
    headers = {'User-Agent': '浏览器头信息'}
    cookies = {'cookie':'你的cookies'}
    url = 'http://www.dianping.com/shanghai/ch10/g110p1'

    html = requests.get(url, headers=headers,cookies = cookies).text
    #requests获得html

    num = get_font()
    #获得加密映射关系

    for key in num:
        if key in html:
            html = html.replace(key, str(num[key]))
    #替换html中加密文字
    return html
y
get_html_text()


