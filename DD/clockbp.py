from apscheduler.schedulers.blocking import BlockingScheduler
##
#import time
from DD import lib
from DD import  dataBackup
##

def scheduled_job():

    spreadSheet = dataBackup.connectSheet()
    sheet = spreadSheet.worksheet('工作表1')
    dataBackup.write(sheet,lib.DataFormJson)
    print("data save finish")
scheduled_job()
