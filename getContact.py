# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 14:53:54 2017

@author: Administrator
"""

#导入模块
from wxpy import *
import codecs
if __name__ == '__main__':
    #初始化机器人，选择缓存模式（扫码）登录
    robot = Bot(cache_path=True)
    #获取好友、群、公众号信息
    robot.chats()
    #获取好友的统计信息
    Friends = robot.friends()
    print(Friends.stats_text())
    fw = codecs.open('message.txt','w','utf-8')
    fw.write(Friends.stats_text())
    fw.flush()
    fw.close()