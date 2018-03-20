# coding:utf-8
import codecs
import collections
import json
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except:
    pass
import os
import re
import time

import itchat
from itchat.content import *
from secretary import analyze, ifPersonalInfo
from wenzhi import zhengzhi, laji
msg_information = {}
face_bug = None  # 针对表情包的内容


@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD,
                      MAP, SHARING, RECORDING, ATTACHMENT,
                      VIDEO], isFriendChat=True,
                     isMpChat=True)
def handle_receive_msg(msg):
    global face_bug
    # 接受消息的时间
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 在好友列表中查询发送信息的好友昵称
    msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']
    msg_time = msg['CreateTime']  # 信息发送的时间
    msg_id = msg['MsgId']  # 每条信息的id
    msg_content = None  # 储存信息的内容
    msg_share_url = None  # 储存分享的链接，比如分享的文章和音乐
    print(msg['Type'])
    print(msg['MsgId'])

    # 如果发送的消息是文本或者好友推荐
    if msg['Type'] == 'Text' or msg['Type'] == 'Friends':
        msg_content = msg['Text']
        print(msg_content)
        r1 = float(zhengzhi(msg_content))
        r2 = float(laji(msg_content))
        if r1 > 0.5:
            print(msg_content + '--政治敏感度：'+ str(r1))
        if r2 > 0.5:
            print(msg_content + '--垃圾敏感度：'+ str(r2))
        if (msg['FromUserName'] != itchat.originInstance.storageClass.userName) and (analyze(msg_content, 0)):
            # print(msg_from)
            itchat.send(u'您可能在和“%s”的聊天中被询问私人信息，请注意防范 聊天内容为：\n\n%s' %
                        (msg_from, msg['Text']), toUserName='filehelper')
        elif (msg['FromUserName'] == itchat.originInstance.storageClass.userName) and (ifPersonalInfo(msg_content)):
            itchat.send(u'您可能在和“%s”的聊天中泄露了私人信息，请注意防范 聊天内容为：\n\n%s\n\n请及时撤回' %
                        (msg_from, msg['Text']),toUserName='filehelper')
    # 如果发送的消息是附件、视屏、图片、语音
    elif msg['Type'] == "Attachment" or msg['Type'] == "Video" \
            or msg['Type'] == 'Picture' \
            or msg['Type'] == 'Recording':
        msg_content = msg['FileName']  # 内容就是他们的文件名
        msg['Text'](str(msg_content))  # 下载文件

    #将信息存储在字典中，每一个msg_id对应一条信息
    msg_information.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time,
                "msg_time_rec": msg_time_rec,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )


##这个是用于监听是否有friend消息撤回
@itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=True, isMpChat=True)
def information(msg):
    # 这里如果这里的msg['Content']中包含消息撤回和id，就执行下面的语句
    if '撤回了一条消息' in msg['Content']:
        # 在返回的content查找撤回的消息的id
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)

        # 得到消息
        old_msg = msg_information.get(old_msg_id)
        print(old_msg)
        if len(old_msg_id) < 11:  # 如果发送的是表情包
            itchat.send_file(face_bug, toUserName='filehelper')
        else:  # 发送撤回的提示给文件助手
            msg_body = "【" \
                       + old_msg.get('msg_from') + " 撤回了 】\n" \
                       + old_msg.get("msg_type") + " 消息：" + "\n" \
                       + old_msg.get('msg_time_rec') + "\n" \
                       + r"" + old_msg.get('msg_content')
            # 如果是分享的文件被撤回了，那么就将分享的url加在msg_body中发送给文件助手
            if old_msg['msg_type'] == "Sharing":
                msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')
            fw.write(msg_body + '\n')
            fw.flush()
            # 将撤回消息发送到文件助手
            itchat.send_msg(msg_body, toUserName='filehelper')
            # 有文件的话也要将文件发送回去
            if old_msg["msg_type"] == "Picture" \
                    or old_msg["msg_type"] == "Recording" \
                    or old_msg["msg_type"] == "Video" \
                    or old_msg["msg_type"] == "Attachment":
                file = '@fil@%s' % (old_msg['msg_content'])
                itchat.send(msg=file, toUserName='filehelper')
                os.remove(old_msg['msg_content'])
            # 删除字典旧消息
            msg_information.pop(old_msg_id)
    # 在好友列表中查询发送信息的好友昵称
    msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']

@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP,
                      SHARING, RECORDING, ATTACHMENT,
                      VIDEO], isGroupChat=True)
def handle_receive_msg(msg):
    global face_bug
    # 接受消息的时间
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # groupid = msg['FromUserName']
    # chatroom = itchat.search_chatrooms(userName=groupid)
    msg_Actual_from = msg['ActualNickName']
    # msg_Actual_from = msg['User']
    # msg_from = msg_Actual_from['Self']['NickName']
    msg_from = msg_Actual_from
    msg_time = msg['CreateTime']  # 信息发送的时间
    msg_id = msg['MsgId']  # 每条信息的id
    msg_content = None  # 储存信息的内容
    msg_share_url = None  # 储存分享的链接，比如分享的文章和音乐
    print(msg['Type'])
    print(msg['MsgId'])

    # 如果发送的消息是文本或者好友推荐
    if msg['Type'] == 'Text' or msg['Type'] == 'Friends':
        msg_content = msg['Text']
        print(msg_content)
        if (msg['FromUserName'] != itchat.originInstance.storageClass.userName) and (analyze(msg_content, 0)):
            # print(msg_from)
            itchat.send(u'您可能在和“%s”的聊天中被询问私人信息，请注意防范 聊天内容为：\n\n%s' %
                        (msg_from, msg['Text']), toUserName='filehelper')
        elif (msg['FromUserName'] == itchat.originInstance.storageClass.userName) and (ifPersonalInfo(msg_content)):
            itchat.send(u'您可能在和“%s”的聊天中泄露了私人信息，请注意防范 聊天内容为：\n\n%s\n\n请及时撤回' %
                        (msg_from, msg['Text']), toUserName='filehelper')
    # 如果发送的消息是附件、视屏、图片、语音
    elif msg['Type'] == "Attachment" or msg['Type'] == "Video" \
            or msg['Type'] == 'Picture' \
            or msg['Type'] == 'Recording':
        msg_content = msg['FileName']  # 内容就是他们的文件名
        msg['Text'](str(msg_content))  # 下载文件
        # print msg_content
    elif msg['Type'] == 'Card':  # 如果消息是推荐的名片
        # 内容就是推荐人的昵称和性别
        msg_content = msg['RecommendInfo']['NickName'] + '的名片'
        if msg['RecommendInfo']['Sex'] == 1:
            msg_content += '性别为男'
        else:
            msg_content += '性别为女'
        print(msg_content)
    elif msg['Type'] == 'Map':  # 如果消息为分享的位置信息
        x, y, location = re.search(
            "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*",
            msg['OriContent']).group(1, 2, 3)
        if location is None:
            # 内容为详细的地址
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()
        else:
            msg_content = r"" + location
    elif msg['Type'] == 'Sharing':
        # 如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
        msg_content = msg['Text']
        msg_share_url = msg['Url']  # 记录分享的url
        print(msg_share_url)
    face_bug = msg_content

    ##将信息存储在字典中，每一个msg_id对应一条信息
    msg_information.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time, "msg_time_rec": msg_time_rec,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )



##这个是用于监听是否有Group消息撤回
@itchat.msg_register(NOTE, isGroupChat=True, isMpChat=True)
def information(msg):
    # 这里如果这里的msg['Content']中包含消息撤回和id，就执行下面的语句
    if '撤回了一条消息' in msg['Content']:
        # 在返回的content查找撤回的消息的id
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        old_msg = msg_information.get(old_msg_id)  # 得到消息
        print(old_msg)
        if len(old_msg_id) < 11:  # 如果发送的是表情包
            itchat.send_file(face_bug, toUserName='filehelper')
        else:  # 发送撤回的提示给文件助手
            msg_body = "【" \
                       + old_msg.get('msg_from') + " 群消息撤回提醒】\n" \
                       + " 撤回了 " + old_msg.get("msg_type") + " 消息：" + "\n" \
                       + old_msg.get('msg_time_rec') + "\n" \
                       + r"" + old_msg.get('msg_content')
            # 如果是分享的文件被撤回了，那么就将分享的url加在msg_body中发送给文件助手
            if old_msg['msg_type'] == "Sharing":
                msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')
            fw.write(msg_body + '\n')
            fw.flush()
            # 将撤回消息发送到文件助手
            itchat.send_msg(msg_body, toUserName='filehelper')
            # 有文件的话也要将文件发送回去
            if old_msg["msg_type"] == "Picture" \
                    or old_msg["msg_type"] == "Recording" \
                    or old_msg["msg_type"] == "Video" \
                    or old_msg["msg_type"] == "Attachment":
                file = '@fil@%s' % (old_msg['msg_content'])
                itchat.send(msg=file, toUserName='filehelper')
                os.remove(old_msg['msg_content'])
            # 删除字典旧消息
            msg_information.pop(old_msg_id)
""" 数据统计分析函数 """
fdata = codecs.open('message.json','w','utf8')
friendlist = codecs.open('friendlist.txt', 'w', 'utf-8')
roomlist = codecs.open('roomlist.txt', 'w', 'utf-8')
""" 好友地区分布 """
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

if __name__ == '__main__':
    # itchat.auto_login( hotReload=True)
    # itchat.run()
    fw = codecs.open('recall.txt', 'a', 'utf-8')
    itchat.auto_login( hotReload=True)
    friends = itchat.get_friends(update=True)[0:]
    s0, s1, s2 = friend_sex(friends)
    p1, p2, c1, c2 = friends_area(friends)
    data={'s':[s0, s1 ,s2],
          'p1': p1,
          'p2': p2,
          'c1': c1,
          'c2': c2
          }
    # print(data)
    json.dump(data, fdata)
    fdata.close()
    friendlist.write( '您总共有' + str(len(friends)-1)+'位好友' + '\n')
    for i in friends[1:]:
        friendlist.write(i['NickName']+' is your friend now.'+'\n')
    friendlist.close()
    """ 获取群聊列表 """
    rooms = itchat.get_chatrooms()
    roomlist.write('您总共有' + str(len(rooms)) + '个群，群名称列表如下：' + '\n')
    for i in rooms:
        roomlist.write(i['NickName'] + '\n')
    roomlist.close()
    itchat.run()
    fw.close()