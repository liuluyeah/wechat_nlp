# -*- coding: utf-8 -*-

import itchat
import collections,codecs,json
from wxpy import *
fw = codecs.open('message.json','w','utf8')
# 好友地区分布
def friends_area(friends):
    provinces = []
    cities = []
    provinces.append([friend['Province'] for friend in friends[1:]])
    cities.append([friend['City'] for friend in friends[1:]])
    province = dict(collections.Counter(provinces[0]))
    city = dict(collections.Counter(cities[0]))
    del province[""]
    del city[""]
    province_b = sorted(province.items(), key=lambda province: province[1], reverse=True)
    city_b = sorted(city.items(), key=lambda city: city[1], reverse=True)
    p1,p2 = [],[]
    for ele in province_b:
        p1.append(ele[0])
        p2.append(ele[1])
    c1,c2 = [],[]
    for ele in city_b:
        c1.append(ele[0])
        c2.append(ele[1])
    return p1[:10], p2[:10],c1[:10],c2[:10]

def friend_sex(friends):
    male = female = other = 0
    for i in friends[1:]:
        sex = i["Sex"]
        if sex == 1:
            male += 1
        elif sex == 2:
            female += 1
        else:
            other += 1
    total = len(friends[1:])
    return male,female,other
    # print("男性好友: %.2f%%" % (float(male) / total * 100) + "\n"
    #       + "女性好友: %.2f%%" % (float(female) / total * 100) + "\n"
    #       + "性别不明:  %.2f%%" % (float(other) / total * 100))
    # print("好友数量: ", male + female + other)
    # print("男性好友: ", male)
    # print("女性好友: ", female)
    # print("性别不明: ", other)
if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    friends = itchat.get_friends(update=True)[0:]
    s0, s1, s2 = friend_sex(friends)
    p1, p2, c1, c2 = friends_area(friends)
    data={'s':[s0, s1 ,s2],
          'p1': p1,
          'p2': p2,
          'c1': c1,
          'c2': c2
          }
    json.dump(data, fw)
    fw.close()

    '''
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
    '''