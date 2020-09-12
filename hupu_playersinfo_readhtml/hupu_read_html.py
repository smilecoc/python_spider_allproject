# -*- coding: utf-8 -*-
# @Author  : Romi
# @FileName: hupu_read_html.py
# @Software: PyCharm
# @Comment ：虎扑NBA球员数据爬虫

import pandas as pd

table = []
for i in range(1,4):
    table.append(pd.read_html('https://nba.hupu.com/stats/players/pts/%d' %i)[0])

players = pd.concat(table)
# 变量重命名
columns=['排名','球员','球队','得分','命中-出手','命中率','命中-三分','三分命中率','命中-罚球','罚球命中率','场次','上场时间']
players.columns=columns

# 删除行标签为0的记录
players.drop(0,inplace=True)


#保存文件
players.to_csv('hupu_players_info.csv',index=None,encoding='utf_8_sig')