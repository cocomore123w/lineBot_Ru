from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from linebot import LineBotApi, WebhookParser

import time
from django.conf import settings
from DD import orderLib
from DD import redisLib
##

from linebot.models import (
    TextSendMessage
)
##
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
###
#flag = False
#totleBox = {}
###########
##
##

##
'''''''''
class BallotBox :
    groupId = ""
    topic = ""
    Ballot = []
    def vote(self,_id,_poll):
        BallotBox.Ballot.append([_id , _poll])
'''
## v2
class BallotBox :
    #index = 0
    def __init__(self,topic,event):
        self.groupId = event.source.group_id
        #self.host = event.source.user_id
        self.topic = topic
        self.Ballot = []

    def vote(self,_id,_poll):
        self.Ballot.append([_id , _poll])

    def getBallot(self):
        #if groupId == self.groupId:
        return self.Ballot
    def getGroupId(self):
        return self.groupId
    def getTopic(self):
        return self.topic
###########
##
##push vote result
def scheduleTask():
    ##
    ##
    totleBox = redisLib.varGetbyte2dict("totleBox")

    #print(pollObjResult_Name(totleBox[list(totleBox.keys())[0]].getBallot()))
    #############################
    text = "在"+ totleBox[list(totleBox.keys())[0]].getTopic()+ "中\n" +pollObjResult_Name(totleBox[list(totleBox.keys())[0]].getBallot())
    line_bot_api.push_message(totleBox[list(totleBox.keys())[0]].getGroupId(), TextSendMessage(text = text))
    ##########################33
    totleBox.pop(list(totleBox.keys())[0])
    redisLib.varSet("totleBox", totleBox)
    ##

#############
##
##
##sched return job_id
def scheduleCreat():
    #print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    get_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 120)) # 2 minutes
    sched = BackgroundScheduler()
    # sched.add_job(some_decorated_task,'interval',seconds=3)
    sched.add_job(scheduleTask, 'date', run_date=get_date)
    return sched
##############

##############
##無記名投票
##input list
##return string
def pollObjResult(pollObj):
    ##############
    ##統計投票項目
    #global pollObjArray
    pollObjArray = []
    for i in range(len(pollObj)):
        if (pollObj[i] in pollObjArray) == False:
            pollObjArray.append(pollObj[i])
    #return pollObjArray
    print(pollObjArray)
    result = "有" + str(len(pollObj)) +"人投票\n"
    result += "==================\n"
    ###########
    ##歸票
    for i in range(len(pollObjArray)):
        result += str(pollObjArray[i]) + "出現了"
        result += str(pollObj.count(pollObjArray[i])) + "次\n"
        result += "##########\n"

    return result
###################
#記名
##input list
##return string
def pollObjResult_Name(pollObj):
    ##############
    ##統計投票項目
    pollObjDict = {}
    #idArray = []
    for i in range(len(pollObj)):
        pollObjDict[pollObj[i][0]] = pollObj[i][1]

    #print(pollObjDict)
    ##歸票
    return pollObjResult(list(pollObjDict.values()))
    ###########
##########
##
##input #vote [vote topic] (第一次輸入發起投票)
##input #vote [vote item] (投票)
##
'''''''''
########### 無記名投票測試
while(1):
    a = input("輸入指令")
    print(flag)
    if a.split(" ")[0] == "#vote" and flag == False:

        print("投票主題 "+ a.split(" ",2)[1])
        flag = True
        sched = scheduleCreat()
        sched.start()
        #print("finish")
    elif a.split(" ")[0] == "#vote" and flag == True:

        obj = a.split(" ",2)[1]
        objArray.append(obj)
        #print("")
    else:
        print("x")
'''

'''''''''
######歸票功能測試
array = ["A","B","A","C","C","C"]
(print(pollObjResult(array)))
'''


