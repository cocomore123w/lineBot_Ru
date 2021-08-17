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

    #################
    '''''''''
    if text[0] == '#':
        #############################


        if text.split(' ')[0] == "#add":
            ##找到id tag
            try:
                tmp = text.split(" ",2)  ##
                _tag = tmp[1]
                _act = tmp[2]
                if event.source.type == "user":
                    ##找到id tag
                    data = lib.DataFormJson["user_id"][event.source.user_id]["tag"]
                    ##update
                    data[_tag] = _act
                    dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
                    lib.DataFormJson = dataBackup.data_json.jsonRead()
                elif event.source.type == "group":
                    ##找到id tag
                    data = lib.DataFormJson["group_id"][event.source.group_id]["tag"]
                    ##update
                    data[_tag] = _act
                    dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
                    lib.DataFormJson = dataBackup.data_json.jsonRead()
                return "指令 " + _tag + " 新增好摟"
            except IndexError:
                return "指令格式打錯瞜"
        elif text.split(' ')[0]  == "#del":
            tmp = text.split(" ")
            _tag = tmp[1]
            try :
                if event.source.type == "user":
                    ##找到id tag
                    data = lib.DataFormJson["user_id"][event.source.user_id]["tag"]
                    ##delet
                    del (data[_tag])
                    dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
                    lib.DataFormJson = dataBackup.data_json.jsonRead()
                elif event.source.type == "group":
                    ##找到id tag
                    data = lib.DataFormJson["group_id"][event.source.group_id]["tag"]
                    ##delet
                    del (data[_tag])
                    dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
                    lib.DataFormJson = dataBackup.data_json.jsonRead()
                return "指令 " + _tag + " 刪掉摟"
            except KeyError:
                return "找不到指令 " + _tag + " 再打一次好嗎"
        elif text.split(' ')[0]  == "#orderlist":
            txt = "現在的指令有這些可以用呦\n----------------------\n"
            #txt += "#add\n#del\n#orderlist\n#addkw\n#delkw\n#kwlist\n#簽到\n"
            if event.source.type == "user":
                ##找到id tag
                data = lib.DataFormJson["user_id"][event.source.user_id]["tag"]
                ##排列
                for i in range(0,len(list(data))):
                    txt += '#'+list(data)[i] + '\n'
                return txt
            elif event.source.type == "group":
                ##找到id tag
                data = lib.DataFormJson["group_id"][event.source.group_id]["tag"]
                ##排列
                for i in range(0,len(list(data))):
                    txt += '#'+list(data)[i] + '\n'
                return txt

            #return 0
        elif text.split(' ')[0] == "#addkw":
            try:
                tmp = text.split(" ",2)
                _tag = tmp[1]
                _act = tmp[2]

                ##找到id tag
                if event.source.type == "user":
                    ##找到id keyword
                    data = lib.DataFormJson["user_id"][event.source.user_id]["keyword"]
                    ##update
                    data[_tag] = _act
                    dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
                    lib.DataFormJson = dataBackup.data_json.jsonRead()
                elif event.source.type == "group":
                    ##找到id keyword
                    data = lib.DataFormJson["group_id"][event.source.group_id]["keyword"]
                    ##update
                    data[_tag] = _act
                    dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
                    lib.DataFormJson = dataBackup.data_json.jsonRead()
            ##update
                return "關鍵字指令 " + _tag + " 新增好摟"
            except IndexError:
                return "指令格式打錯瞜"
        elif text.split(' ')[0] == "#delkw":
            tmp = text.split(" ")
            _tag = tmp[1]
            try :
                if event.source.type == "user":
                    ##找到id keyword
                    data = lib.DataFormJson["user_id"][event.source.user_id]["keyword"]
                    ##delet
                    del (data[_tag])
                    dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
                    lib.DataFormJson = dataBackup.data_json.jsonRead()
                elif event.source.type == "group":
                    ##找到id keyword
                    data = lib.DataFormJson["group_id"][event.source.group_id]["keyword"]
                    ##delet
                    del (data[_tag])
                    dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
                    lib.DataFormJson = dataBackup.data_json.jsonRead()

                return "關鍵字指令 " + _tag + " 刪掉搂"
            except KeyError:
                return "找不到指令 " + _tag + " 再打一次好嗎"
        elif text.split(' ')[0] == "#kwlist":  ##
            txt = "現在的關鍵字回話有這些呦\n----------------------\n"
            if event.source.type == "user":
                ##找到id keyword
                data = lib.DataFormJson["user_id"][event.source.user_id]["keyword"]
                ##排列

                for i in range(0,len(list(data))):
                    txt += list(data)[i] + '\n'
                return txt
            elif event.source.type == "group":
                ##找到id keyword
                data = lib.DataFormJson["group_id"][event.source.group_id]["keyword"]
                ##排列
                for i in range(0, len(list(data))):
                    txt += list(data)[i] + '\n'
                return txt
            #return 0

        ######################################################
        #elif text.split(' ')[0] == "#簽到":  ##
        #    user_id = line_bot_api.get_profile(event.source.user_id).display_name
        #    spreadSheet = signin.connectSheet()
        #    sheet =  signin.findtoday(spreadSheet)
        #    eror = signin.SignIn(sheet, text)
        #    if eror== 0:
        #        return user_id+"簽到成功"
        #    else:
        #        return user_id + eror
        #elif text.split(' ')[0] == "#feedback":  ##to do
        #    txt = "\n"

        #    return 0
        ###################################################################################################################   待修改

        elif text.split(' ')[0] == "#addlive":
            try:
                tmp = text.split(" ",2)
                _char = tmp[1]
                _url = tmp[2]

                ##找到id tag
                if event.source.type == "user":
                    ##找到id keyword
                    data = lib.DataFormJson["user_id"][event.source.user_id]["live"]
                    ##update
                    data[_char] = _url
                    dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
                    lib.DataFormJson = dataBackup.data_json.jsonRead()
                elif event.source.type == "group":
                    ##找到id keyword
                    data = lib.DataFormJson["group_id"][event.source.group_id]["live"]
                    ##update
                    data[_char] = _url
                    dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
                    lib.DataFormJson = dataBackup.data_json.jsonRead()
            ##update
                if _url == vtr_bug.url_ru:
                    return "要常來看我呦,啾~"
                else:
                    return  "臭DD,又想背著我去偷看 "+_char+" 了嗎QQ"
            except IndexError:
                return "你的指令格式打錯瞜"
        elif text.split(' ')[0] == "#dellive":
            try:
                tmp = text.split(" ")
                _char = tmp[1]
            except IndexError:
                return "你的指令格式打錯瞜"
            try :
                if event.source.type == "user":
                    ##找到id keyword
                    data = lib.DataFormJson["user_id"][event.source.user_id]["live"]
                    _url = data[_char]
                    ##delet
                    del (data[_char])
                    dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
                    lib.DataFormJson = dataBackup.data_json.jsonRead()
                elif event.source.type == "group":
                    ##找到id keyword
                    data = lib.DataFormJson["group_id"][event.source.group_id]["live"]
                    _url = data[_char]
                    ##delet
                    del (data[_char])
                    dataBackup.data_json.jsonUpdate(lib.DataFormJson,1)
                    lib.DataFormJson = dataBackup.data_json.jsonRead()
                else:
                    return 0
                if vtr_bug.url_ru == _url:
                    return "Neeeeeeeeeeeeeeeeeeeeee"
                else:
                    return  "不想看 "+_char + " 了嗎,就知道你最愛我了~啾"
            except KeyError:
                return "我不認識 " + _char + " 這個人欸,你是不是又在幻想了"
        elif text.split(' ')[0] == "#livelist":  ##
            txt = "你們這些臭DD都跑去看這些人,嗚嗚\n----------------------\n"
            if event.source.type == "user":
                ##找到id keyword
                data = lib.DataFormJson["user_id"][event.source.user_id]["live"]
                ##排列

                for i in range(0,len(list(data))):
                    txt += list(data)[i] + '\n'
                return txt
            elif event.source.type == "group":
                ##找到id keyword
                data = lib.DataFormJson["group_id"][event.source.group_id]["live"]
                ##排列
                for i in range(0, len(list(data))):
                    txt += list(data)[i] + '\n'
                return txt
        elif text.split(' ')[0] == "#live":  ##
            try:
                _char = text.split(' ')[1]  # 人
            except IndexError:
                return "你的格式打錯摟"
            try:
                if event.source.type == "user":
                    url = lib.DataFormJson["user_id"][event.source.user_id]["live"][_char]
                    # print()
                    if url == vtr_bug.url_ru:
                        return vtr_bug.yt_channel_status(url)
                    else:
                        return _char+vtr_bug.yt_channel_status(url)#lib.tag_reply(text, data)
                elif event.source.type == "group":
                    url = lib.DataFormJson["group_id"][event.source.group_id]["live"][_char]
                    if url == vtr_bug.url_ru:
                        return vtr_bug.yt_channel_status(url)
                    else:
                        return _char+vtr_bug.yt_channel_status(url)
                else:
                    return 0
                #url = lib.DataFormJson
                #opt = vtr_bug.yt_channel_status(url)
            except KeyError:
                return "我不認識 " + _char + " 這個人欸,你是不是又在幻想了"
        #####################################################################################################################
        elif text.split(' ')[0] == "#高雄確診":  ##to do
            #txt = "\n"
            if lib._char.is_all_number(text.split(' ')[1]) ==True:
                return text.split(' ')[1]
            else:
                return None
        ########################################################################
        elif text.split(' ')[0] == "#yts":
            try:
                #tmp = text.split(" ")
                #_searchkw = tmp[1]
                tmp = text.find(" ") + 1
                _searchkw = text[tmp:]
            except IndexError:
                return "你的指令格式打錯瞜"
            url = yt_search.yt_search(_searchkw)
            if url == None:
                return "我沒有找到相關的東西噢"
            else:
                return "我找到最像的是這個噢 " + url
        #

        #elif text.split(' ')[0] == "#live"

        #elif text.split(' ')[0] == "#sd":  ##to do:
        #    if event.source.user_id == lib.master_id:
        #        if text.split(' ')[1] == "datasave":
        #            spreadSheet = dataBackup.connectSheet()
        #            sheet = spreadSheet.worksheet('工作表1')
        #            dataBackup.write(sheet,lib.DataFormJson)
        #            return 	"儲存成功"
        #        elif text.split(' ')[1] == "dataprint":
        #            return str(lib.DataFormJson)
        #        elif text.split(' ')[1] == "dataadd":
        #            try:
        #                up_data =text.split(' ')[2]
        #                _element_user = list(lib.DataFormJson["user_id"].keys())
        #                _element_group = list(lib.DataFormJson["group_id"].keys())
        #                _user = len(lib.DataFormJson["user_id"])
        #                _group = len(lib.DataFormJson["group_id"])

        #                for i in range(0,_user):
        #                    lib.DataFormJson["user_id"][_element_user[i]][up_data]={}
        #                for i in range(0,_group):
        #                    lib.DataFormJson["group_id"][_element_group[i]][up_data]={}
                        ###
         #               lib.DataDemo["id"][up_data]={}
                        ###
          #              dataBackup.data_json.jsonUpdate(lib.DataFormJson)
          #              lib.DataFormJson = dataBackup.data_json.jsonRead()
          #              dataBackup.data_json.jsonUpdate(lib.DataDemo)
          #              lib.DataFormJson = dataBackup.data_json.jsonRead_Demo()

          #              return "資料庫項目新增成功"
          #          except IndexError:
          #              return "資料格式錯誤,格式為#sudo dataadd [up_data]"
                #elif text.split(' ')[1] == "datadel":
                    #return str(lib.DataFormJson)
                    #return str(lib.DataFormJson)

           # else:
           #     return "權限不夠的不要亂打好嗎"

        else:
            ##找到id tag
            if event.source.type == "user":
                data = lib.DataFormJson["user_id"][event.source.user_id]["tag"]
                #print()
                return lib.tag_reply(text, data)
            elif event.source.type == "group":
                data = lib.DataFormJson["group_id"][event.source.group_id]["tag"]
                return lib.tag_reply(text, data)
    else:   #keyword reply
            ##找到id keyword
            if event.source.type == "user":
                data = lib.DataFormJson["user_id"][event.source.user_id]["keyword"]
                #print()
                return lib.keyword_reply(text, data)
            elif event.source.type == "group":
                data = lib.DataFormJson["group_id"][event.source.group_id]["keyword"]
                return lib.keyword_reply(text, data)
    '''
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

