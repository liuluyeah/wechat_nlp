#encoding:utf-8

from itchat.content import *
import requests
import json
import itchat
import time
import os
import re
import sys
import shutil



msg_dict = {}

#ClearTimeOutMsg用于清理消息字典，把超时消息清理掉
#为减少资源占用，此函数只在有新消息动态时调用
def ClearTimeOutMsg():
    if msg_dict.__len__() > 0:
        for msgid in list(msg_dict): #由于字典在遍历过程中不能删除元素，故使用此方法
            if time.time() - msg_dict.get(msgid, None)["msg_time"] > 130.0: #超时两分钟
                item = msg_dict.pop(msgid)
                if item['msg_type'] == "Picture" \
                        or item['msg_type'] == "Recording" \
                        or item['msg_type'] == "Video" \
                        or item['msg_type'] == "Attachment":
                    print("要删除的文件：", item['msg_content'])
                    os.remove(item['msg_content'])

#将接收到的消息存放在字典中，当接收到新消息时对字典中超时的消息进行清理
#没有注册note（通知类）消息，通知类消息一般为：红包 转账 消息撤回提醒等，不具有撤回功能
@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO, FRIENDS])
def HandleMsg(msg):
    if not os.path.exists("../php/ReceivedMsg/"):
        os.mkdir("../php/ReceivedMsg/")

    mytime = time.localtime()  # 这儿获取的是本地时间
    #获取用于展示给用户看的时间 2017/03/03 13:23:53
    msg_time_touser = mytime.tm_year.__str__() \
                      + "/" + mytime.tm_mon.__str__() \
                      + "/" + mytime.tm_mday.__str__() \
                      + " " + mytime.tm_hour.__str__() \
                      + ":" + mytime.tm_min.__str__() \
                      + ":" + mytime.tm_sec.__str__()

    msg_id = msg['MsgId'] #消息ID
    msg_time = msg['CreateTime'] #消息时间
    msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName'] #消息发送人昵称
    msg_type = msg['Type'] #消息类型
    msg_content = None #根据消息类型不同，消息内容不同
    msg_url = None #分享类消息有url

    if msg['Type'] == 'Text':

        msg_content = msg['Text']
        msg.user.send('%s' % (tuling(msg.text)))

    elif msg['Type'] == 'Picture':
        msg_content = r"../php/ReceivedMsg/" + msg['FileName']
        msg['Text'](msg_content)

    elif msg['Type'] == 'Card':
        msg_content = msg['RecommendInfo']['NickName'] + r" 的名片"

    elif msg['Type'] == 'Map':
        x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1,
                                                                                                                    2,
                                                                                                                    3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()
        else:
            msg_content = r"" + location
    elif msg['Type'] == 'Sharing':
        msg_content = msg['Text']
        msg_url = msg['Url']

    elif msg['Type'] == 'Recording':
        msg_content = r"../php/ReceivedMsg/" + msg['FileName']
        msg['Text'](msg_content)

    elif msg['Type'] == 'Attachment':
        msg_content = r"../php/ReceivedMsg/" + msg['FileName']
        msg['Text'](msg_content)

    elif msg['Type'] == 'Video':
        msg_content = r"../php/ReceivedMsg/" + msg['FileName']
        msg['Text'](msg_content)

    elif msg['Type'] == 'Friends':
        msg_content = msg['Text']

    #更新字典
    # {msg_id:(msg_from,msg_time,msg_time_touser,msg_type,msg_content,msg_url)}
    print(msg_id);
    msg_dict.update(
        {msg_id: {"msg_from": msg_from, "msg_time": msg_time, "msg_time_touser": msg_time_touser, "msg_type": msg_type,
                  "msg_content": msg_content, "msg_url": msg_url}})
    #清理字典
    ClearTimeOutMsg()

#收到note类消息，判断是不是撤回并进行相应操作
@itchat.msg_register([NOTE])
def SaveMsg(msg):
    # print(msg)
    if not os.path.exists("../php/RevokedMsg/"):
        os.mkdir("../php/RevokedMsg/")

    print(msg['Content'])
    if re.search(r"\<replacemsg\>\<\!\[CDATA\[.*撤回了一条消息\]\]\>\<\/replacemsg\>", msg['Content'].encode('utf8')) != None \
        or re.search(r"\<replacemsg\>\<\!\[CDATA\[.*has recalled a message\.\]\]\>\<\/replacemsg\>", msg['Content']) != None:
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        old_msg = msg_dict.get(old_msg_id, {})
        print(old_msg_id, old_msg)
        msg_send = r"您的好友：" \
                   + old_msg.get('msg_from', None) \
                   + r"  在 [" + old_msg.get('msg_time_touser', None) \
                   + r"], 撤回了一条 ["+old_msg['msg_type']+"] 消息, 内容如下:" \
                   + old_msg.get('msg_content', None)
        if old_msg['msg_type'] == "Sharing":
            msg_send += r", 链接: " \
                        + old_msg.get('msg_url', None)
        elif old_msg['msg_type'] == 'Picture' \
                or old_msg['msg_type'] == 'Recording' \
                or old_msg['msg_type'] == 'Video' \
                or old_msg['msg_type'] == 'Attachment':
            msg_send += r", 存储在php/RevokedMsg目录中，查看前请不要Logout"

            shutil.move(old_msg['msg_content'], r"../php/RevokedMsg/")

        itchat.send(msg_send, toUserName='filehelper') #将撤回消息的通知以及细节发送到文件助手

        msg_dict.pop(old_msg_id)
        ClearTimeOutMsg()


#图灵机器人
def tuling(info):
    appkey = "b1bf4f8c-7ba3-4cac-b728-d25f1a388fb2"
    url = "http://sandbox.api.simsimi.com/request.p?key=%s&lc=zh&ft=1.0&text=%s"%(appkey, info)
    req = requests.get(url)
    content = req.text
    data = json.loads(content)
    answer = data['response']
    return answer


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.isAt:
        msg.user.send('%s' % (tuling(msg.text)))


reload(sys)
sys.setdefaultencoding('utf8')

itchat.auto_login(hotReload=True)
itchat.run(True)

