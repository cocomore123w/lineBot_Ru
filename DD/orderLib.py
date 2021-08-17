from DD import lib
from DD import  dataBackup
from DD import vtr_bug
from DD import  yt_search
from DD import  voteLib
from DD import redisLib
##############
import random
import time
import numpy as np
####################
from linebot import LineBotApi, WebhookParser
###################
#totleBox = {}
#################
voteResult = ". 　　　　　。　　　　　　•　　　 　ﾟ　　。 　　.\n"+"\n"+"　　　.　　　 　　　　.　　　　　　　。　　　 。　. 　\n"+"\n"+".　　 。　　　　　~~~~~ඞ  　　 • 　　　　•\n"+"\n"+"　. 　ﾟ　.  臥底1號 was An Impostor.　    。　.\n"+"\n"+"　　ﾟ　　　　　.　　　　　. ,　　　　　　　　.　 ."

######
from django.conf import settings
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)





#####################
class Order:
    ########################
    #管理員指令 可以對資料庫做編輯
    #
    #
    #################
    def superuserOrder(event):
        order = event.message.text.split(" ")[1]
        silent_flag = redisLib.varGetbyte2dict("silent_flag")
        ##########################
        if order == "list":
            return "現在可以用的指令有這些噢\ndatasave\ndataadd\non\noff"
        elif order == "datasave":
            spreadSheet = dataBackup.connectSheet()
            sheet = spreadSheet.worksheet('工作表1')
            dataBackup.write(sheet, lib.DataFormJson)
            return "儲存成功"

        elif order == "dataadd":
            try:
                lib.DataFormJson = dataBackup.data_json.jsonRead()
                lib.DataDemo = dataBackup.data_json.jsonRead_Demo()
                # print(lib.DataFormJson)
                up_data = event.message.text.split(' ')[2]
                _element_user = list(lib.DataFormJson["user_id"].keys())
                _element_group = list(lib.DataFormJson["group_id"].keys())
                _user = len(lib.DataFormJson["user_id"])
                _group = len(lib.DataFormJson["group_id"])

                for i in range(0, _user):
                    lib.DataFormJson["user_id"][_element_user[i]][up_data] = {}
                for i in range(0, _group):
                    lib.DataFormJson["group_id"][_element_group[i]][up_data] = {}
                ###
                lib.DataDemo["id"][up_data] = {}
                ###
                dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                lib.DataFormJson = dataBackup.data_json.jsonRead()
                dataBackup.data_json.jsonUpdate(lib.DataDemo, 2)
                lib.DataDemo = dataBackup.data_json.jsonRead_Demo()

                return "資料庫項目新增成功"
            except IndexError:
                return "資料格式錯誤,格式為#sd dataadd up_data"

        elif order == "on":
            silent_flag = False
            redisLib.varSet("silent_flag",silent_flag)
            # dataBackup.data_json.jsonUpdate("F", 3)
            return "可以開始使用摟"

        elif order == "off":
            silent_flag = True
            redisLib.varSet("silent_flag", silent_flag)
            # dataBackup.data_json.jsonUpdate("T", 3)
            return "目前暫停使用瞜"
        return "權限不夠的不要亂打好嗎"
    ############################################
    class replyOrder:
        #####
        ##一般tag指令
        ##
        def normalOrder(event):
            text = event.message.text
            if text.split(' ')[0] == "#add":
                ##找到id tag
                try:
                    tmp = text.split(" ", 2)  ##
                    _tag = tmp[1]
                    _act = tmp[2]
                    if event.source.type == "user":
                        ##找到id tag
                        data = lib.DataFormJson["user_id"][event.source.user_id]["tag"]
                        ##update
                        data[_tag] = _act
                        dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                        lib.DataFormJson = dataBackup.data_json.jsonRead()
                    elif event.source.type == "group":
                        ##找到id tag
                        data = lib.DataFormJson["group_id"][event.source.group_id]["tag"]
                        ##update
                        data[_tag] = _act
                        dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                        lib.DataFormJson = dataBackup.data_json.jsonRead()
                    return "指令 " + _tag + " 新增好摟"
                except IndexError:
                    return "指令格式打錯瞜"

            elif text.split(' ')[0] == "#del":
                tmp = text.split(" ")
                _tag = tmp[1]
                try:
                    if event.source.type == "user":
                        ##找到id tag
                        data = lib.DataFormJson["user_id"][event.source.user_id]["tag"]
                        ##delet
                        del (data[_tag])
                        dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                        lib.DataFormJson = dataBackup.data_json.jsonRead()
                    elif event.source.type == "group":
                        ##找到id tag
                        data = lib.DataFormJson["group_id"][event.source.group_id]["tag"]
                        ##delet
                        del (data[_tag])
                        dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                        lib.DataFormJson = dataBackup.data_json.jsonRead()
                    return "指令 " + _tag + " 刪掉摟"
                except KeyError:
                    return "找不到指令 " + _tag + " 再打一次好嗎"

            elif text.split(' ')[0] == "#orderlist":
                txt = "現在的指令有這些可以用呦\n----------------------\n"
                # txt += "#add\n#del\n#orderlist\n#addkw\n#delkw\n#kwlist\n#簽到\n"
                if event.source.type == "user":
                    ##找到id tag
                    data = lib.DataFormJson["user_id"][event.source.user_id]["tag"]
                    ##排列
                    for i in range(0, len(list(data))):
                        txt += '#' + list(data)[i] + '\n'
                    return txt
                elif event.source.type == "group":
                    ##找到id tag
                    data = lib.DataFormJson["group_id"][event.source.group_id]["tag"]
                    ##排列
                    for i in range(0, len(list(data))):
                        txt += '#' + list(data)[i] + '\n'
                    return txt

            return None
                # return 0
            #######################################################################################################################################
        #######################################
        ##關鍵字指令
        ##
        def keywordOrder(event):
            text = event.message.text
            if text.split(' ')[0] == "#addkw":
                try:
                    tmp = text.split(" ", 2)
                    _tag = tmp[1]
                    _act = tmp[2]

                    ##找到id tag
                    if event.source.type == "user":
                        ##找到id keyword
                        data = lib.DataFormJson["user_id"][event.source.user_id]["keyword"]
                        ##update
                        data[_tag] = _act
                        dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                        lib.DataFormJson = dataBackup.data_json.jsonRead()
                    elif event.source.type == "group":
                        ##找到id keyword
                        data = lib.DataFormJson["group_id"][event.source.group_id]["keyword"]
                        ##update
                        data[_tag] = _act
                        dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                        lib.DataFormJson = dataBackup.data_json.jsonRead()
                    ##update
                    return "關鍵字指令 " + _tag + " 新增好摟"
                except IndexError:
                    return "指令格式打錯瞜"

            elif text.split(' ')[0] == "#delkw":
                tmp = text.split(" ")
                _tag = tmp[1]
                try:
                    if event.source.type == "user":
                        ##找到id keyword
                        data = lib.DataFormJson["user_id"][event.source.user_id]["keyword"]
                        ##delet
                        del (data[_tag])
                        dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                        lib.DataFormJson = dataBackup.data_json.jsonRead()
                    elif event.source.type == "group":
                        ##找到id keyword
                        data = lib.DataFormJson["group_id"][event.source.group_id]["keyword"]
                        ##delet
                        del (data[_tag])
                        dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
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

                    for i in range(0, len(list(data))):
                        txt += list(data)[i] + '\n'
                    return txt
                elif event.source.type == "group":
                    ##找到id keyword
                    data = lib.DataFormJson["group_id"][event.source.group_id]["keyword"]
                    ##排列
                    for i in range(0, len(list(data))):
                        txt += list(data)[i] + '\n'
                    return txt

            return None
        #######################################
        ##yt開台查詢
        ##
        def liveOrder(event):
            text = event.message.text
            if text.split(' ')[0] == "#addlive":
                try:
                    tmp = text.split(" ", 2)
                    _char = tmp[1]
                    _url = tmp[2]

                    ##找到id tag
                    if event.source.type == "user":
                        ##找到id keyword
                        data = lib.DataFormJson["user_id"][event.source.user_id]["live"]
                        ##update
                        data[_char] = _url
                        dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                        lib.DataFormJson = dataBackup.data_json.jsonRead()
                    elif event.source.type == "group":
                        ##找到id keyword
                        data = lib.DataFormJson["group_id"][event.source.group_id]["live"]
                        ##update
                        data[_char] = _url
                        dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                        lib.DataFormJson = dataBackup.data_json.jsonRead()
                    ##update
                    if _url == vtr_bug.url_ru:
                        return "要常來看我呦,啾~"
                    else:
                        return "臭DD,又想背著我去偷看 " + _char + " 了嗎QQ"
                except IndexError:
                    return "你的指令格式打錯瞜"

            elif text.split(' ')[0] == "#dellive":
                try:
                    tmp = text.split(" ")
                    _char = tmp[1]
                except IndexError:
                    return "你的指令格式打錯瞜"
                try:
                    if event.source.type == "user":
                        ##找到id keyword
                        data = lib.DataFormJson["user_id"][event.source.user_id]["live"]
                        _url = data[_char]
                        ##delet
                        del (data[_char])
                        dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                        lib.DataFormJson = dataBackup.data_json.jsonRead()
                    elif event.source.type == "group":
                        ##找到id keyword
                        data = lib.DataFormJson["group_id"][event.source.group_id]["live"]
                        _url = data[_char]
                        ##delet
                        del (data[_char])
                        dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                        lib.DataFormJson = dataBackup.data_json.jsonRead()
                    else:
                        return 0
                    if vtr_bug.url_ru == _url:
                        return "Neeeeeeeeeeeeeeeeeeeeee"
                    else:
                        return "不想看 " + _char + " 了嗎,就知道你最愛我了~啾"
                except KeyError:
                    return "我不認識 " + _char + " 這個人欸,你是不是又在幻想了"

            elif text.split(' ')[0] == "#livelist":  ##
                txt = "你們這些臭DD都跑去看這些人,嗚嗚\n----------------------\n"
                if event.source.type == "user":
                    ##找到id keyword
                    data = lib.DataFormJson["user_id"][event.source.user_id]["live"]
                    ##排列

                    for i in range(0, len(list(data))):
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
                            return _char + vtr_bug.yt_channel_status(url)  # lib.tag_reply(text, data)
                    elif event.source.type == "group":
                        url = lib.DataFormJson["group_id"][event.source.group_id]["live"][_char]
                        if url == vtr_bug.url_ru:
                            return vtr_bug.yt_channel_status(url)
                        else:
                            return _char + vtr_bug.yt_channel_status(url)
                    else:
                        return 0

                except KeyError:
                    return "我不認識 " + _char + " 這個人欸,你是不是又在幻想了"

            return None
        #######################################
        ##記名投票 id
        ##計時
        ##
        ##
        ##
        ##
        ##
        def voteOrder(event):
            text = event.message.text
            totleBox = redisLib.varGetbyte2dict("totleBox")

            #print("hi go vote")
            ##發起投票 決定 主題 開始計時
            ##
            ##
            #global totleBox
            if text.split(" ")[0] == "#vote" :

                try:
                    if event.source.type == "user":
                        return "個人模式不能用投票功能呦"
                    _host = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id).display_name
                    _topic = text.split(" ",2)[1]
                    _group = event.source.group_id
                    poll = str(_host) + " 提出了\n" + _topic +"\n"+ "要表決," +"倒數兩分鐘結束投票噢"
                    print(totleBox)


                    if totleBox.get(_group) != None:
                    #if redisLib.varGet(_group) != None:
                        print("正在表決,投票")
                        # 正在表決中嘔
                        #
                        #time.sleep(1)
                        #global totleBox
                        totleBox[_group].vote(event.source.user_id, text.split(" ", 2)[1])
                        #redisLib.varSet(_group,)
                        #data = redisLib.varGetbyte2dict(_group)
                        #data.vote(event.source.user_id, text.split(" ", 2)[1])
                        redisLib.varSet("totleBox",totleBox)
                        return line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id).display_name + "已完成投票"
                    else:
                        ##提案
                        print("提案")
                        #redisLib.varSet(_group, voteLib.BallotBox(_topic,event))
                        totleBox[_group] = voteLib.BallotBox(_topic,event)
                        redisLib.varSet("totleBox", totleBox)
                        #time.sleep(1)
                        ##開始計時
                        #print("倒數計時兩分鐘")
                        sche = voteLib.scheduleCreat()
                        sche.start()

                        return poll

                    #return poll
                except IndexError:
                    return "你的指令格式打錯了呦"
                '''''''''
            elif text.split(" ")[0] == "#vote":
                #voter = vote.BallotBox
                #voter.groupId = event.source.group_id

                try:
                    _id = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id).display_name
                    _poll = text.split(" ", 2)[1]

                    return 0
                except IndexError:
                    return "你的指令格式打錯了呦"
                '''
            return None
        #######################################
        def allOrder(event):
            text = event.message.text
            if text[0] == '#':
                if text.split(' ')[0] == "#add":
                    ##找到id tag
                    try:
                        tmp = text.split(" ", 2)  ##
                        _tag = tmp[1]
                        _act = tmp[2]
                        if event.source.type == "user":
                            ##找到id tag
                            data = lib.DataFormJson["user_id"][event.source.user_id]["tag"]
                            ##update
                            data[_tag] = _act
                            dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                            lib.DataFormJson = dataBackup.data_json.jsonRead()
                        elif event.source.type == "group":
                            ##找到id tag
                            data = lib.DataFormJson["group_id"][event.source.group_id]["tag"]
                            ##update
                            data[_tag] = _act
                            dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                            lib.DataFormJson = dataBackup.data_json.jsonRead()
                        return "指令 " + _tag + " 新增好摟"
                    except IndexError:
                        return "指令格式打錯瞜"

                elif text.split(' ')[0] == "#del":
                    tmp = text.split(" ")
                    _tag = tmp[1]
                    try:
                        if event.source.type == "user":
                            ##找到id tag
                            data = lib.DataFormJson["user_id"][event.source.user_id]["tag"]
                            ##delet
                            del (data[_tag])
                            dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                            lib.DataFormJson = dataBackup.data_json.jsonRead()
                        elif event.source.type == "group":
                            ##找到id tag
                            data = lib.DataFormJson["group_id"][event.source.group_id]["tag"]
                            ##delet
                            del (data[_tag])
                            dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                            lib.DataFormJson = dataBackup.data_json.jsonRead()
                        return "指令 " + _tag + " 刪掉摟"
                    except KeyError:
                        return "找不到指令 " + _tag + " 再打一次好嗎"

                elif text.split(' ')[0] == "#orderlist":
                    txt = "現在的指令有這些可以用呦\n----------------------\n"
                    # txt += "#add\n#del\n#orderlist\n#addkw\n#delkw\n#kwlist\n#簽到\n"
                    if event.source.type == "user":
                        ##找到id tag
                        data = lib.DataFormJson["user_id"][event.source.user_id]["tag"]
                        ##排列
                        for i in range(0, len(list(data))):
                            txt += '#' + list(data)[i] + '\n'
                        return txt
                    elif event.source.type == "group":
                        ##找到id tag
                        data = lib.DataFormJson["group_id"][event.source.group_id]["tag"]
                        ##排列
                        for i in range(0, len(list(data))):
                            txt += '#' + list(data)[i] + '\n'
                        return txt
                #######################
                elif text.split(' ')[0] == "#addkw":
                    try:
                        tmp = text.split(" ", 2)
                        _tag = tmp[1]
                        _act = tmp[2]

                        ##找到id tag
                        if event.source.type == "user":
                            ##找到id keyword
                            data = lib.DataFormJson["user_id"][event.source.user_id]["keyword"]
                            ##update
                            data[_tag] = _act
                            dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                            lib.DataFormJson = dataBackup.data_json.jsonRead()
                        elif event.source.type == "group":
                            ##找到id keyword
                            data = lib.DataFormJson["group_id"][event.source.group_id]["keyword"]
                            ##update
                            data[_tag] = _act
                            dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                            lib.DataFormJson = dataBackup.data_json.jsonRead()
                        ##update
                        return "關鍵字指令 " + _tag + " 新增好摟"
                    except IndexError:
                        return "指令格式打錯瞜"

                elif text.split(' ')[0] == "#delkw":
                    tmp = text.split(" ")
                    _tag = tmp[1]
                    try:
                        if event.source.type == "user":
                            ##找到id keyword
                            data = lib.DataFormJson["user_id"][event.source.user_id]["keyword"]
                            ##delet
                            del (data[_tag])
                            dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                            lib.DataFormJson = dataBackup.data_json.jsonRead()
                        elif event.source.type == "group":
                            ##找到id keyword
                            data = lib.DataFormJson["group_id"][event.source.group_id]["keyword"]
                            ##delet
                            del (data[_tag])
                            dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
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

                        for i in range(0, len(list(data))):
                            txt += list(data)[i] + '\n'
                        return txt
                    elif event.source.type == "group":
                        ##找到id keyword
                        data = lib.DataFormJson["group_id"][event.source.group_id]["keyword"]
                        ##排列
                        for i in range(0, len(list(data))):
                            txt += list(data)[i] + '\n'
                        return txt
                #############################
                elif text.split(' ')[0] == "#addlive":
                    try:
                        tmp = text.split(" ", 2)
                        _char = tmp[1]
                        _url = tmp[2]

                        ##找到id tag
                        if event.source.type == "user":
                            ##找到id keyword
                            data = lib.DataFormJson["user_id"][event.source.user_id]["live"]
                            ##update
                            data[_char] = _url
                            dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                            lib.DataFormJson = dataBackup.data_json.jsonRead()
                        elif event.source.type == "group":
                            ##找到id keyword
                            data = lib.DataFormJson["group_id"][event.source.group_id]["live"]
                            ##update
                            data[_char] = _url
                            dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                            lib.DataFormJson = dataBackup.data_json.jsonRead()
                        ##update
                        if _url == vtr_bug.url_ru:
                            return "要常來看我呦,啾~"
                        else:
                            return "臭DD,又想背著我去偷看 " + _char + " 了嗎QQ"
                    except IndexError:
                        return "你的指令格式打錯瞜"

                elif text.split(' ')[0] == "#dellive":
                    try:
                        tmp = text.split(" ")
                        _char = tmp[1]
                    except IndexError:
                        return "你的指令格式打錯瞜"
                    try:
                        if event.source.type == "user":
                            ##找到id keyword
                            data = lib.DataFormJson["user_id"][event.source.user_id]["live"]
                            _url = data[_char]
                            ##delet
                            del (data[_char])
                            dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                            lib.DataFormJson = dataBackup.data_json.jsonRead()
                        elif event.source.type == "group":
                            ##找到id keyword
                            data = lib.DataFormJson["group_id"][event.source.group_id]["live"]
                            _url = data[_char]
                            ##delet
                            del (data[_char])
                            dataBackup.data_json.jsonUpdate(lib.DataFormJson, 1)
                            lib.DataFormJson = dataBackup.data_json.jsonRead()
                        else:
                            return 0
                        if vtr_bug.url_ru == _url:
                            return "Neeeeeeeeeeeeeeeeeeeeee"
                        else:
                            return "不想看 " + _char + " 了嗎,就知道你最愛我了~啾"
                    except KeyError:
                        return "我不認識 " + _char + " 這個人欸,你是不是又在幻想了"

                elif text.split(' ')[0] == "#livelist":  ##
                    txt = "你們這些臭DD都跑去看這些人,嗚嗚\n----------------------\n"
                    if event.source.type == "user":
                        ##找到id keyword
                        data = lib.DataFormJson["user_id"][event.source.user_id]["live"]
                        ##排列

                        for i in range(0, len(list(data))):
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
                                return _char + vtr_bug.yt_channel_status(url)  # lib.tag_reply(text, data)
                        elif event.source.type == "group":
                            url = lib.DataFormJson["group_id"][event.source.group_id]["live"][_char]
                            if url == vtr_bug.url_ru:
                                return vtr_bug.yt_channel_status(url)
                            else:
                                return _char + vtr_bug.yt_channel_status(url)
                        else:
                            return 0
                        # url = lib.DataFormJson
                        # opt = vtr_bug.yt_channel_status(url)
                    except KeyError:
                        return "我不認識 " + _char + " 這個人欸,你是不是又在幻想了"

                if event.source.type == "user":
                        data = lib.DataFormJson["user_id"][event.source.user_id]["tag"]
                        # print()
                        # return lib.tag_reply(text, data)
                        return Order.Lib.tag_reply(text, data)
                elif event.source.type == "group":
                        data = lib.DataFormJson["group_id"][event.source.group_id]["tag"]
                        # return lib.tag_reply(text, data)
                        return Order.Lib.tag_reply(text, data)
            #######################################################
            if event.source.type == "user":
                    data = lib.DataFormJson["user_id"][event.source.user_id]["keyword"]
                    # print()
                    # return lib.keyword_reply(text, data)
                    return Order.Lib.keyword_reply(text, data)
            elif event.source.type == "group":
                    data = lib.DataFormJson["group_id"][event.source.group_id]["keyword"]
                    # return lib.keyword_reply(text, data)
                    return Order.Lib.keyword_reply(text, data)
        ######################################

    class Lib:
        #############tag指令回覆
        ##
        ##
        def tag_reply(text, data):  # 根據tag回覆
            text = text[1:]  # 取內文
            if data.get(text) != None:
                return data.get(text)
            else:
                return '我不知道你在說啥欸'
        #############關鍵字回覆
        ##
        ##回覆最長的kw
        def keyword_reply(text, data):
            try:
                key = data.keys()
                matchAns = []
                index = []
                for i in range(0, len(list(key))):
                    if text.find(list(key)[i]) != -1:
                        # return data[list(a)[i]] # data.get(text)
                        matchAns.append(len(list(key)[i]))
                        index.append(i)
                        # print("aa")
                        # print(data[list(a)[i]])
                if matchAns.count(max(matchAns)) > 1:
                    array = np.array(matchAns)
                    ele = index[np.where(array == max(matchAns))[0][
                        random.randint(0, matchAns.count(max(matchAns)) - 1)]]  ##      找到矩陣元素的index
                    ##
                    # print(ele[random.randint(0,matchAns.count(max(matchAns))-1)])
                    rpy = list(key)[ele]
                else:
                    ele = max(matchAns)
                    rpy = list(key)[index[matchAns.index(ele)]]
                return data[rpy]

            except ValueError:
                return None
        ################
        ##
        ##隨機回覆一個符合的kw
        def keyword_reply_v2(text, data):
            key = data.keys()
            matchAns = []
            index = []
            for i in range(0, len(list(key))):
                if text.find(list(key)[i]) != -1:
                    # return data[list(a)[i]] # data.get(text)
                    matchAns.append(len(list(key)[i]))
                    index.append(i)
            # print(index)
            # print(matchAns)
            if len(matchAns) > 1:
                ele = index[random.randint(0, len(matchAns) - 1)]
                # print(ele)
                ##
                # print(ele[random.randint(0,matchAns.count(max(matchAns))-1)])
                rpy = list(key)[ele]
            else:
                ele = max(matchAns)
                rpy = list(key)[index[matchAns.index(ele)]]
            return data[rpy]
        #################################################
########################################################
