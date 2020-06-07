# -*- coding: utf-8 -*-
# @Time    : 3/3/2020 12:10 AM
# @Author  : Romain 
# @FileName: jd_comments_spider.py
# @Software: PyCharm
# @Comment ：抓取jd商城的商品评论并存储进行分析


from wordcloud import WordCloud
import jieba
import re
import requests
import json
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import collections # 统计库
from PIL import Image # 图像处理库
import wordcloud  #词云
from snownlp import SnowNLP  #情感分析库


#请求URL
def get_comments(good_id):
    #good_url_template = 'https://item.jd.com/{}.html'.format(good_id)
    jsonurl='https://club.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'.format(good_id)
    html=requests.get(jsonurl).text
    return html

#解析json数据
def data_stored(html):
    conn = sqlite3.connect("comments.db")  # 建立连接，数据库存在时，直接连接；不存在时，创建相应数据库
    # 新建一张表
    conn.execute('''CREATE TABLE Comments_jd

          (ID text PRIMARY KEY     NOT NULL,
          comment text     );''')
    josntext=json.loads(html)
    comments= josntext['comments']
    #注意sql语句中使用了格式化输出的占位符%s和%d来表示将要插入的变量，其中%s需要加引号''
    for comment in comments:
        sql = "insert into Comments_jd(ID,comment) values('%s','%s')" % (comment['id'],comment['content'])
        conn.execute(sql)
        conn.commit()#提交事务，否则不能插入数据

    # 关闭数据库连接
    conn.close()

#从数据库中取出评论 数据
def gettxt():
    conn= sqlite3.connect("comments.db")
    sql='select comment from Comments_jd'
    cursor=conn.execute(sql)#执行查询语句,返回sqlite3.Cursor object
    text=cursor.fetchall()# 获得查询结果集
    commentstr=''
    for txt in text:
        commentstr=commentstr+txt[0]
    #关闭游标
    conn.close()
    return commentstr, text   #python执行到return语句时，会退出函数，return之后的语句不再执行


#分词与词云处理
def  get_wordcloud(commentstr):

    # 文本预处理
    pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"') # 定义正则表达式匹配模式,u后面字符串以 Unicode 格式 进行编码，一般用在中文字符串前面，防止因为源码储存格式问题，导致再次使用时出现乱码
    string_data = re.sub(pattern, '', commentstr) # 将符合模式的字符去除

    # 文本分词
    '''
    结巴分词模式
    # jieba.lcut(s)        精确模式，返回一个列表，不存在冗余单词
    
    # jieba.lcut(s，cut_all=True)    全模式，返回一个列表，存在冗余单词
    # jieba.lcut_for_search(s)   搜索引擎模式，将精确模式下返回的长字符再次进行分词
    # jieba.add_word(w)  向分词的词典中加入新的词汇
    '''
    jieba.load_userdict("dict.txt")  # 添加用户自定义字典，防止一些词汇的拆分
    seg_list_exact = jieba.cut(string_data, cut_all = False) # 精确模式分词
    object_list = []
    # 自定义停用词,排除没有意义的高频词
    remove_words = [u'的', u'和', u'是', u'尺码大小',u'尺码大小',u'舒适度',u'做工细节',u'透气性',u'抓地效果',u'，',u'。',u'了',u'也',u'尺码',u'：',u'！','42','425',u'穿',u"很"]

    for word in seg_list_exact: # 循环读出每个分词
        if word not in remove_words: # 如果不在去除词库中
            object_list.append(word) # 分词追加到列表
    # 词频统计
    word_counts = collections.Counter(object_list) # 对分词做词频统计
    word_counts_top10 = word_counts.most_common(20) # 获取前20最高频的词
    print (word_counts_top10) # 输出检查

    # 词频展示
    mask = np.array(Image.open('adidas.jpg')) # 选择图片作为词频背景
    wc = wordcloud.WordCloud(
        font_path='C:/Windows/Fonts/simhei.ttf', # 设置字体格式
        mask=mask, # 设置背景图
        max_words=50, # 最多显示词数
        max_font_size=100 # 字体最大值
    )

    wc.generate_from_frequencies(word_counts) # 从字典生成词云
    image_colors = wordcloud.ImageColorGenerator(mask) # 从背景图建立颜色方案
    wc.recolor(color_func=image_colors) # 将词云颜色设置为背景图方案
    plt.imshow(wc) # 显示词云
    plt.axis('off') # 关闭坐标轴
    plt.show() # 显示图

#情感分析
def  comment_Emotional_analysis(text):
    sum = 0
    count = 0
    for txt in text:
        print(txt[0])
        s = SnowNLP(txt[0])
        #.sentiments用来计算positive的概率,越接近于1表示越正面
        print('{}'.format(s.sentiments))
        # print(s.sentiments,mylog)
        sum += s.sentiments
        count += 1

    score = sum / count
    print('finalscore={}'.format(score))

if __name__ == '__main__':
    html=get_comments(str(52297931949))
    data_stored(html)
    commentstr,text=gettxt()
    get_wordcloud(commentstr)
    comment_Emotional_analysis(text)