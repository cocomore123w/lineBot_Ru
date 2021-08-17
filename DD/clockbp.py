from apscheduler.schedulers.blocking import BlockingScheduler
##
#import time
from DD import lib
from DD import  dataBackup
##
#sched = BlockingScheduler()

#@sched.scheduled_job('cron', hour = 0,minute = 24)
def scheduled_job():

    spreadSheet = dataBackup.connectSheet()
    sheet = spreadSheet.worksheet('工作表1')
    dataBackup.write(sheet,lib.DataFormJson)
    print("data save finish")
scheduled_job()
#sched.start()