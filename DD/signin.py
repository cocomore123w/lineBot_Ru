import time
import os
##
#from linebot import LineBotApi, WebhookParser
#from linebot.exceptions import InvalidSignatureError, LineBotApiError
#from linebot.models import MessageEvent, TextMessage, TextSendMessage
#from django.conf import settings
##
import gspread
from oauth2client.service_account import ServiceAccountCredentials
##
doc_key = os.environ.get('doc_key', None)

##line_bot_api.get_profile(event.source.user_id)
####
def SignIn(sheet,text):  #簽到 name cellphone
    _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        name = text.split(" ")[1]
        cellphone = text.split(" ")[2]
        if name==None or cellphone==None:
            return "輸入格式錯誤,姓名或手機不能為空"
        elif is_contains_chinese(name) == False and is_contains_english(name) == False: #不是中文也不是英文
            return "輸入格式錯誤,姓名請輸入包含中英文之字元"
        elif is_all_number(cellphone) == False:
            return "輸入格式錯誤,手機不得輸入數字以外之字元"
        elif len(cellphone) != 10:
            return "輸入格式錯誤,手機字元數量錯誤"
        else:
            sheet.add_rows(1)
            # print(sheet.row_count)
            count = sheet.row_count + 1
            index = "A" + str(count) + ":" + "C" + str(count)
            sheet.update(index, [[_time, name, cellphone]])
            return 0
    except IndexError:
        return "輸入格式錯誤,請重新輸入"
    #except name== or cellphone
#print()
def connectSheet():  ##串接
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("./DD/line-bot-test-314017-8251d384c729.json", scope)
    client = gspread.authorize(creds)
    # spreadSheet = client.open("簽到表")#或是可以用 add_worksheet("11月", 100, 100) 來新增
    spreadSheet = client.open_by_key(doc_key)
    #spreadSheet.
    #sheet = spreadSheet.worksheet("工作表1") # 利用 title 來抓 sheet
    return spreadSheet

def sheetInit(spreadSheet,worksheet):
    sheet = spreadSheet.worksheet(worksheet) #("工作表1")
    sheet.update('A1:C1', [["Time", "Name", "Cellphone"]])

def newWorksheet(spreadSheet,name):
    spreadSheet.add_worksheet(title=name, rows='1', cols='3')
    #sheet = spreadSheet.worksheet(name)
    #return  name

def changeDay(spreadSheet):
    get_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split(" ")[0]
    year = get_date.split("-")[0]
    month = get_date.split("-")[1]
    day = get_date.split("-")[2]
    WorksheetName = year + "/" +  month + "/" + day

    #spreadSheet.add_worksheet(title = name, rows='2000', cols='3')
    newWorksheet(spreadSheet,WorksheetName)
    sheetInit(spreadSheet,WorksheetName)

    return WorksheetName

def findtoday(spreadSheet):
    get_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split(" ")[0]
    year = get_date.split("-")[0]
    month = get_date.split("-")[1]
    day = get_date.split("-")[2]
    WorksheetName = year + "/" + month + "/" + day
    try:
        sheet = spreadSheet.worksheet(WorksheetName)
    except gspread.exceptions.WorksheetNotFound:
        newWorksheet(spreadSheet, WorksheetName)
        sheetInit(spreadSheet, WorksheetName)
        sheet = spreadSheet.worksheet(WorksheetName)

    return sheet
        #print("hi")
    #finally:
def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def is_all_number(strs):

    for _char in strs:
        _char = ord(_char)
        if not 48 <= _char <= 57: ##0-9
            return False
    return True

def is_all_english(strs):
    for _char in strs:
        _char = ord(_char)
        if not 65 <= _char <= 90 and not 97 <= _char <= 122 : #小寫 大寫
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
        if  65 <= _char <= 90 or  97 <= _char <= 122:
            return True
    return False
'''''''''
text = "#簽到 coco 0987987987"
spreadSheet = connectSheet()
#newWorksheet(spreadSheet,"aaa")
sheet = spreadSheet.worksheet("aaa")
#sheetInit(spreadSheet,"aaa")
#sheet = spreadSheet.worksheet("工作表1")
#sheet.insert_row(["1","2" ,"3" ],2)
SignIn(spreadSheet,"aaa",text)
#changeDay(spreadSheet)
'''
