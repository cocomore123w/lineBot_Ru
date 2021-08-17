import requests
import time

#############################
##for test
##
url = []
url.append("https://www.youtube.com/channel/UCFKOVgVbGmX65RxO3EtH3iw")
url.append("https://www.youtube.com/channel/UChAnqc_AY5_I3Px5dig3X1Q")
url.append("https://www.youtube.com/channel/UCBC7vYFNQoGPupe5NxPG4Bw")
url.append("https://www.youtube.com/channel/UCAWSyEs_Io8MtpY3m-zqILA")
url.append("https://www.youtube.com/channel/UC5CwaMl1eIgY8h02uZw7u8A")
url.append("https://www.youtube.com/channel/UCZlDXzGoo7d44bwdNObFacg")




##ushia
url_ru = "https://www.youtube.com/channel/UCl_gCybOJRIgOXw6Qb4qJzQ"
###

target_url = "https://www.youtube.com/watch?v="
###
##################################################################################################
##
##

################3
##
##input url (youtube channel url)
##return chanel status
def yt_channel_status(url):
    ru_ch = url_ru
    res = requests.get(url, verify=False)
    st_1 = find_live_videoid(res)
    if st_1==None:
        #####
        #####upcomimg stream list
        url += "/videos?view=2&live_view=502"
        ru_ch += "/videos?view=2&live_view=502"
        #####
        st_2 = _find_reserve_videoid(res)
        if st_2==None:
            if url == ru_ch:
                return "我現在沒有開台,不要太想我呦"
            return "的頻道沒有預定開台呦,乖乖回冰箱待著吧"
        else:
            if url == ru_ch:
                return "沒看到我是不是有點寂寞呢? "+st_2[0]+" 的時候記得來看我呦 "+ st_2[1]
            return "會在 " + st_2[0] +" 的時候開台呦,你該不會想丟下我去看吧... " + st_2[1] #預約開台
    else:
        if url == ru_ch:
            return "我的直播開始了,不准去偷看其他女人呦 " + st_1
        return "現在在開台呦,幫我買冰淇淋我會考慮讓你出冰箱去看 "+ st_1 #正在開台
        #return 1
    #print("1")

##########    timer work

def yt_channel_status_auto(url):
    url += "/videos?view=2&live_view=502"
    res = requests.get(url, verify=False)
    st_1 = find_live_videoid(res)
    if st_1==None:
        return None
    '''''''''''
        st_2 = _find_reserve_videoid(res)
        if st_2==None:
            if url == url_ru:
                return None
            return None
        if url == url_ru: #預約開台
            return "沒看到我是不是有點寂寞呢? "+st_2[0]+" 的時候記得來看我呦 "+ st_2[1]
        return "會在 " + st_2[0] +" 的時候開台呦,你該不會想丟下我去看吧... " + st_2[1]
    '''
    if url == url_ru: #正在開台
        return "我的直播開始了,不准去偷看其他女人呦 " + st_1
    else:
        return "現在在開台呦,幫我買冰淇淋我會考慮讓你出冰箱去看 "+ st_1
    #
##########
##if channel is live
##input requests
##return video's url
def find_live_videoid(res):
    target = "channelFeaturedContentRenderer"
    target_end = "}"
    count = res.text.find(target)
    count_end = res.text[count:].find(target_end)
    ########
    ########get videoid
    text = res.text[count:count + count_end]
    temp_id = text.find("videoId") + 10
    temp_id_end = text[temp_id:].find('"')
    videoid = text[temp_id:temp_id + temp_id_end]
    if videoid == "":
        return None
    return target_url+videoid
##############
##timestamp to timestring
##input timestamp
##return timestring
def time_tr(t):
    struct_time = time.localtime(t)
    timeString = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)
    return timeString
######################
##if channel have upcomimg stream
##input requests
##return video's url
def _find_reserve_videoid(res):
    target = "upcomingEventData"
    target_end = "isReminderSet"
    count = res.text.find(target) + 33
    count_end = res.text[count:].find(target_end) - 3
    temp = res.text[count:count+count_end]
    if temp == "":  #none upcomimg stream
        return None
    else:
        starttime =time_tr(int(temp))
    #####################################

    if starttime != "":
        target = "gridVideoRenderer"
        #target = "videoRenderer"
        target_end = "upcomingEventData"
        #count = res.text.find(target)
        count_end = res.text[:].find(target_end)
        count = res.text[:count_end].find(target) +31
        #######################################################
        if count == 30:
            target = "videoRenderer"
            target_end = "upcomingEventData"
            count_end = res.text[:].find(target_end)
            count = res.text[:count_end].find(target) + 27
        ##############################################
        temp2 = res.text[count:count_end]
        count_end_2 = temp2.find('"')
        videoid = temp2[:count_end_2]


        if len(videoid) !=11: ##not upcomimg stream
            return None
        elif free_chat(temp):
            return [starttime,target_url+videoid]
        return None
    return None
####
#if upcomimg stream is free chat (date > 14 days)
#input timestamp
#return bool
def free_chat(_time):
    time_stamp = time.time()
    diff = abs(int(_time) - int(time_stamp))
    #print(diff)
    if diff/(60*60*24) < 14:
        return True
    return False


#####################################

##### funtction test
'''''''''
for i in range(0,len(url)):
    print(yt_channel_status(url[i]))
'''
