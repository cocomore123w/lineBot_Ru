import time
import os
##
##
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from  DD import lib
##
doc_key = os.environ.get('doc_key', None)
##

def connectSheet():  ##串接
  scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
  creds = ServiceAccountCredentials.from_json_keyfile_name(lib.google_token, scope)
  client = gspread.authorize(creds)
  spreadSheet = client.open_by_key(doc_key)
  # spreadSheet.
  # sheet = spreadSheet.worksheet("工作表1") # 利用 title 來抓 sheet
  return spreadSheet



def write(sheet,data):
  get_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split(" ")[0]


  sheet.add_rows(1)
  count = sheet.row_count + 1
  index = "A" + str(count) + ":" + "B" + str(count)
  sheet.update(index, [[get_date, str(data)]])

  print("back up")


#####################################
class data_json:
  def connectSheet_json():  ##串接
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(lib.google_token, scope)
    client = gspread.authorize(creds)
    # spreadSheet = client.open("簽到表")#或是可以用 add_worksheet("11月", 100, 100) 來新增
    spreadSheet = client.open_by_key(doc_key)
    # spreadSheet.
    # sheet = spreadSheet.worksheet("工作表1") # 利用 title 來抓 sheet
    return spreadSheet

  def jsonUpdate(data,pos):
    #sp = data_json.connectSheet_json()
    sheet = data_json.connectSheet_json().worksheet("data_")
    index = "A" + str(pos)
    sheet.update(index,[[str(data)]])
    #print("update")

  def jsonRead():
    sheet = data_json.connectSheet_json().worksheet("data_")

    data = eval(sheet.get("A1")[0][0])
    #print("refresh")
    return data

  def jsonRead_Demo():
    sheet = data_json.connectSheet_json().worksheet("data_")

    data = eval(sheet.get("A2")[0][0])
    #print("refresh")
    return data

  #def jsonRead_SilentFlag():
  #    sheet = data_json.connectSheet_json().worksheet("data_")

   #   data = eval(sheet.get("A3")[0][0])
   #   print("bot flag")
   #   return data
    #print(type(data))
    #data = dict(data)
    #return data

####################################
class data_log:
  def connectSheet_log():  ##串接
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
    #creds = ServiceAccountCredentials.from_json_keyfile_name("./DD/line-bot-test-314017-8251d384c729.json", scope)
    creds = ServiceAccountCredentials.from_json_keyfile_name(lib.google_token, scope)
    #creds = ServiceAccountCredentials.from_json_keyfile_name("line-bot-test-314017-8251d384c729.json", scope)
    client = gspread.authorize(creds)
    # spreadSheet = client.open("簽到表")#或是可以用 add_worksheet("11月", 100, 100) 來新增
    spreadSheet = client.open_by_key(doc_key)
    # spreadSheet.
    # sheet = spreadSheet.worksheet("工作表1") # 利用 title 來抓 sheet
    return spreadSheet

  def jsonUpdate(data, event):
    # sp = data_json.connectSheet_json()
    sheet = data_log.connectSheet_log().worksheet("follow_log")
    get_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    ##### up to sheet
    sheet.add_rows(1)
    count = sheet.row_count + 1
    index = "A" + str(count) + ":" + "C" + str(count)
    sheet.update(index, [[get_date, event, str(data)]])  # time event status content
    print("write")