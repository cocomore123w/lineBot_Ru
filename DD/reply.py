from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from django.conf import settings


from DD import lib
from DD.lib  import json
from DD import  signin
from DD import  dataBackup
from DD import vtr_bug
from DD import  yt_search
from DD import orderLib

from DD import redisLib
##############################
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
############################
#flg_group = False

###################
import os

#print(data)


##############
def keyword(event):
    text = event.message.text
    '''''''''
    try:
        #print(event.source.group_id)
        flg_group = True
    except AttributeError:
        flg_group = False
    '''
    ##
    #用戶id       source.user_id
    #群id    source.group_id
    ##
    #profile = line_bot_api.get_profile(event.source.user_id)
    lib.DataFormJson = dataBackup.data_json.jsonRead()
    lib.DataDemo = dataBackup.data_json.jsonRead_Demo()
    ########################################################

    ########################################################

    ####### fin
    #return orderLib.Order.replyOrder.allOrder(event)\
    ####################
    ##

    if text[0] == '#':
        ##
        _reply = orderLib.Order.replyOrder.normalOrder(event)
        #print("order")
        if _reply != None:
            return _reply
        ##
        _reply = orderLib.Order.replyOrder.keywordOrder(event)
        #print("kw")
        if _reply !=None:
            return _reply
        ##
        _reply = orderLib.Order.replyOrder.liveOrder(event)
        #print("live")
        #print(_reply)
        if _reply !=None:
        #    print("return rp")
            return _reply
        ##
        _reply = orderLib.Order.replyOrder.voteOrder(event)
        #print("vote")
        #print(_reply)
        if _reply !=None:
            return _reply
        #if text=="#vote":
        #    print(redisLib.varGetbyte2dict('totleBox'))
        #    return "hi"
        ##
        ##tag reply
        ##找到id tag
        if event.source.type == "user":
            data = lib.DataFormJson["user_id"][event.source.user_id]["tag"]
            return orderLib.Order.Lib.tag_reply(text, data)

        elif event.source.type == "group":
            data = lib.DataFormJson["group_id"][event.source.group_id]["tag"]
            return orderLib.Order.Lib.tag_reply(text, data)

    #keyword reply
    ##找到id keyword
    if event.source.type == "user":
        data = lib.DataFormJson["user_id"][event.source.user_id]["keyword"]
        return orderLib.Order.Lib.keyword_reply(text, data)

    elif event.source.type == "group":
        data = lib.DataFormJson["group_id"][event.source.group_id]["keyword"]
        return orderLib.Order.Lib.keyword_reply(text, data)

    ###########################
def flexload(docName):

    return lib.jsonC.load_menu(docName)

def followContent(event):

    if event.source.type == "user":
        user_id =line_bot_api.get_profile(event.source.user_id).display_name
        return "感謝你的追隨"+ user_id + "  啾"

    elif event.source.type == "group":
        return " こんるし --"

def follow_join(event):
    lib.DataFormJson = dataBackup.data_json.jsonRead()
    lib.DataDemo = dataBackup.data_json.jsonRead_Demo()
    if event.source.type == "user":
        add_dict = lib.DataDemo
        add_dict[event.source.user_id] = add_dict.pop("id")
        lib.DataFormJson["user_id"].update(add_dict)
        dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)

        #lib.DataFormJson = dataBackup.data_json.jsonRead()
        dataBackup.data_log.jsonUpdate(lib.DataFormJson, "user join")
        print("user data renew")
    elif event.source.type == "group":
        #lib.DataFormJson = dataBackup.data_json.jsonRead()
        # 初始化json資料
        add_dict = lib.DataDemo
        add_dict[event.source.group_id] = add_dict.pop("id")

        lib.DataFormJson["group_id"].update(add_dict)
        dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
        #lib.DataFormJson = dataBackup.data_json.jsonRead()
        dataBackup.data_log.jsonUpdate(lib.DataFormJson, "group join")
        print("group data renew")
def unfollow_leave(event):
    #elif event == 'UnfollowEvent':
        ##delet user_id
    lib.DataFormJson = dataBackup.data_json.jsonRead()
    if event.source.type == "user":
        #lib.DataFormJson = dataBackup.data_json.jsonRead()
        del (lib.DataFormJson["user_id"][event.source.user_id])
        dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
        #lib.DataFormJson = dataBackup.data_json.jsonRead()
        dataBackup.data_log.jsonUpdate(lib.DataFormJson, "user leave")
    elif event.source.type == "group":
        #lib.DataFormJson = dataBackup.data_json.jsonRead()
        del (lib.DataFormJson["group_id"][event.source.group_id])
        dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
        #lib.DataFormJson = dataBackup.data_json.jsonRead()
        dataBackup.data_log.jsonUpdate(lib.DataFormJson, "group leave")



################

