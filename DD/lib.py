import json
import  shutil
import time
import os

import numpy as np
import random
from DD import dataBackup
###################
master_id = os.environ.get('master_id', None)
google_token = "./DD/line-bot-test-314017-8251d384c729.json"
############3
redisHost = os.environ.get('redisHost', None)
redisPort = os.environ.get('redisPort', None)
redisPwd = os.environ.get('redisPwd', None)
#######
DataFormJson = dataBackup.data_json.jsonRead()
DataDemo = dataBackup.data_json.jsonRead_Demo()
#print()
#####################
def Case_sw(text,text_key):  #大小寫對照
    num = len(text_key)
    text= text.lower()
    text_key = text_key.lower()
    if (text.find(text_key)) != -1:
        return True
    else:
        return False

def tag_reply(text,data): #根據tag回覆
    text = text[1:] #取內文
    if data.get(text) != None:
        return data.get(text)
    else:
        return '我不知道你在說啥欸'
#############
##
##回覆最長的kw
def keyword_reply(text,data):
    try:
        key = data.keys()
        matchAns = []
        index = []
        for i in range(0, len(list(key))):
            if text.find(list(key)[i]) != -1:
                #return data[list(a)[i]] # data.get(text)
                matchAns.append(len(list(key)[i]))
                index.append(i)
                #print("aa")
                #print(data[list(a)[i]])
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
    #if data.find(text) != None:
################
##
##隨機回覆一個符合的kw
def keyword_reply_v2(text,data):
    key = data.keys()
    matchAns = []
    index = []
    for i in range(0, len(list(key))):
        if text.find(list(key)[i]) != -1:
            #return data[list(a)[i]] # data.get(text)
            matchAns.append(len(list(key)[i]))
            index.append(i)
    #print(index)
    #print(matchAns)
    if len(matchAns) > 1:
        ele = index[random.randint(0, len(matchAns) - 1)]
        #print(ele)
        ##
        # print(ele[random.randint(0,matchAns.count(max(matchAns))-1)])
        rpy = list(key)[ele]
    else:
        ele = max(matchAns)
        rpy = list(key)[index[matchAns.index(ele)]]
    return data[rpy]



def flag_value(bool):
    return bool





def updataTag(event,data):
    return 0
#print(tag_reply('#aa'))
class jsonC:
    '''''''''
    def updatejson(data):
        with open(json_docName, "w", encoding='utf8') as f:
            json.dump(data, f)
        f.close()
        #return data
    def refreshjson(data):
        with open(json_docName, "r",encoding = 'utf8') as f:
            data = json.load(f)
        f.close()
        return data
    '''
    def load_menu(docName):
        with open(docName, "r",encoding = 'utf8') as f:
            data = json.load(f)
        f.close()
        return data
    '''
    def backupjson():  ##備份資料
        get_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split(" ")[0]
        year = get_date.split("-")[0]
        month = get_date.split("-")[1]
        day = get_date.split("-")[2]
        date = year + month + day +"data_backup" +".json"

        #_dirSource = "data.json"
        #_dirSource = r"data.json"
        #if not os.path.isdir("DD/batabp"):
        #    os.mkdir("DD/batabp")
        #    print("mkdir finish")
        _dir = r"databp/" + date
        with open(json_docName, "r", encoding='utf8') as f:
            DataFormJson = json.load(f)
        f.close()

        with open(_dir, "w", encoding='utf8') as f:
            json.dump(DataFormJson, f)
        f.close()
        #shutil.copy(_dirSource, _dir)
        print("data cpoy")
        #return 0
    '''
class _char:
    def is_all_chinese(strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True

    def is_all_number(strs):

        for _char in strs:
            _char = ord(_char)
            if not 48 <= _char <= 57:  ##0-9
                return False
        return True

    def is_all_english(strs):
        for _char in strs:
            _char = ord(_char)
            if not 65 <= _char <= 90 and not 97 <= _char <= 122:  # 小寫 大寫
                return False
        return True

    def is_contains_chinese(strs):
        for _char in strs:
            if '\u4e00' <= _char <= '\u9fa5':
                return True
        return False

    def is_contains_english(strs):
        for _char in strs:
            _char = ord(_char)
            if 65 <= _char <= 90 or 97 <= _char <= 122:
                return True
        return False


##############
#jsonC.backupjson()