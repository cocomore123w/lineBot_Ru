import requests
from bs4 import BeautifulSoup
#import beautifulsoup4
#import numpy



url = "https://www.youtube.com/results?search_query="


def yt_search(kw):
    request=requests.get(url+kw)
    text = request.text

    target =  text.find("channelId")
    if target != -1: #找頻道
        head = "https://www.youtube.com/channel/"
        target_end = text[target + 12:].find('"')
        channelId = text[target + 12:target + 12 + target_end]
        #print(head + channelId)
        return head + channelId
        #print(None)
    elif  text.find("videoId") != -1:   #找影片
        head = "https://www.youtube.com/watch?v="
        target = text.find("videoId")
        target_end = text[target + 10:].find('"')
        videoId = text[target + 10:target + 10 + target_end]
        #print(target)
        #print(target_end)
        #print(head + videoId)
        return head + videoId
    else:
        return None


def yt_search_v2(kw,fc):
    request=requests.get(url+kw)
    text = request.text

    target =  text.find("channelId")
    if fc == "c": #找頻道
        head = "https://www.youtube.com/channel/"
        target_end = text[target + 12:].find('"')
        channelId = text[target + 12:target + 12 + target_end]
        #print(head + channelId)
        return head + channelId
        #print(None)
    elif  fc == "v":   #找影片
        head = "https://www.youtube.com/watch?v="
        target = text.find("videoId")
        target_end = text[target + 10:].find('"')
        videoId = text[target + 10:target + 10 + target_end]
        #print(target)
        #print(target_end)
        #print(head + videoId)
        return head + videoId
    else:
        return None



# videoRenderer