import requests
import time
from PIL import Image
import requests
from bs4 import BeautifulSoup

import os
import shutil
import re
#############################

#url = 'https://www.youtube.com/channel/UC-hM6YJuNYVAmUWxeIr9FeA'
#url2 ='https://www.youtube.com/channel/UChAnqc_AY5_I3Px5dig3X1Q'
#url3 = 'https://www.youtube.com/channel/UCBC7vYFNQoGPupe5NxPG4Bw'
#target_url = 'https://www.youtube.com/watch?v='

#soup = BeautifulSoup(res.text,'html.parser')
#print(soup)
#print(res.text)
#print('---------------------')

#target = '<ytd-thumbnail-overlay-time-status-renderer class="style-scope ytd-thumbnail" overlay-style="UPCOMING">'
#target = 'videoId'
#A = res.text.find(target)
#b = res.text[A+10:A+50].find('"')
#videoId = res.text[A+10:A+10+b]
#print(b)
#print(a)

def find_today_new():

    url_kao_g = "https://www.kcg.gov.tw/2019nCoV/News.aspx?n=37402DE676C7AAA5&sms=3E86285D7FF55C61"
    target_ = 'href="News_Content.aspx?n=37402DE676C7AAA5&sms='
    end_ = '本市確診個案活動史'  # +7


    html_kao_g = requests.get(url_kao_g, verify=False).text
    count = html_kao_g.find(target_)
    count_end = html_kao_g.find(end_) + len(end_)

    #print(count)
    ######
    today =  _now_time()[1] + _now_time()[2]
    latest_news_date = latest_news(html_kao_g,count)

    if today != latest_news_date:
        return None

    #latest_news =

    ####
    else:
        #url = "https://www.kcg.gov.tw/2019nCoV/" +  html_kao_g[count:count+100].split('"')[1]
        #url = html_kao_g[count:count_end]
        #print(url)
        url = "https://www.kcg.gov.tw/2019nCoV/" + html_kao_g[count:count_end].split('"')[1]       ##改
        #return 0
        return url

def find_date_new(date):

    url_kao_g = "https://www.kcg.gov.tw/2019nCoV/News.aspx?n=37402DE676C7AAA5&sms=3E86285D7FF55C61"
    #target_ = 'href="News_Content.aspx?n=37402DE676C7AAA5&sms='
    end_ = date+'本市確診個案活動史'  #


    html_kao_g = requests.get(url_kao_g, verify=False).text
    #count = html_kao_g.find(target_)

    count_end = html_kao_g.find(end_) + len(end_)   #
    ######

    if count_end == len(end_) -1:
        return None
    ####
    else:
        url = "https://www.kcg.gov.tw/2019nCoV/" +  html_kao_g[count_end-98:count_end].split('"')[0]
        return url
        #return  0

def _now_time():
    get_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split(" ")[0]
    year = get_date.split("-")[0]
    month = get_date.split("-")[1]
    day = get_date.split("-")[2]

    #data = month + day
    #target_ = data + "本市確診個案活動史"
    return year,month,day

def latest_news(text,index):
    latest_news_date = text[index:index + 120].split('"')[3].split("本市確診")[0]
    #print(temp)
    #latest_news_date =temp
    #print(latest_news_date)
    return latest_news_date

def date_news(date,text,index):

    latest_news_date = text[index:index + 120].split('"')[3].split(date+"本市確診")[0]
    #print(temp)
    #latest_news_date =temp
    #print(latest_news_date)
    return latest_news_date


def get_jpg(url):
    html_kao_g = requests.get(url, verify=False).text
    #target_ = '<div class="data_midlle_news_box02" ><p><img alt="'


    ##
    temp = get_sentence(html_kao_g)
    #print(temp)
    jpg_url =[]
    ##
    #a = temp.find('src="')
    sp1 = temp.split('src="')
    #print(len(sp1))
    for i in range(0,len(sp1)-1):
        jpg_url.append(sp1[i+1].split('"')[0].replace("amp;",""))

    if len(jpg_url) == 0:
        #sts = temp.split('\n')
        #sts_c = len(sts) - 3
        #print(sts_c)
        #txt = ''
        #for i in range(0,sts_c):
        #    txt += get_content(sts[i]) + '\n'
        opt = ['txt',get_content(temp)]
        return opt
    #print(len(jpg_url))
    else:
        return  jpg_url

def get_content(text):
    #target_ = '">'
    # end_ = 'width: 100%;" /></p>'  # +7
    #end_ = '</span>'
    #count = text.find(target_) +2
    #count_end = text[count:].find(end_)
    #return text[count:count + count_end]
    soup = BeautifulSoup(text, 'html.parser')
    # print(soup)
    paragraphs = soup.find('p')
    # print(paragraphs)
    #print(paragraphs.text)
    return paragraphs.text
def get_sentence(text):
    #target_ = '<div class="data_midlle_news_box02" ><p><img alt="'
    #target_ ='src="https://ws.kcg.gov.tw/Download.ashx?u='
    target_ = '<div class="data_midlle_news_box02" ><p>'
    #end_ = 'width: 100%;" /></p>'  # +7
    end_ = '</div>'
    count = text.find(target_)
    #count_end = text[count:].find(end_) + len(end_) + 8
    count_end = text[count:].find(end_)
    #print(count)
    #print(count_end)
    #print(text[count:count+count_end])
    #print(text[count:count+count_end].split("</div")[0])
    return text[count:count+count_end].split("</div")[0]


#print(get_jpg('https://www.kcg.gov.tw/2019nCoV/News_Content.aspx?n=37402DE676C7AAA5&sms=3E86285D7FF55C61&s=F638FE07BD1684C8'))
#print((find_today_new()))

#def reset_imgtemp():


def download_img(url):
    ##
    shutil.rmtree("static/img_temp")
    os.mkdir("static/img_temp")
    ####
    doc = len(url)
    for i in range(0,doc):
        im = Image.open(requests.get(url[i], stream=True).raw)
        rows,cols = im.size
        im = im.resize( (int(rows/2), int(cols/2)), Image.BILINEAR )
        name = str(i) + ".jpg"
        im.save(r"static/img_temp/" + name, "PNG")
    #domain = "2137d9ac9d57.ngrok.io"
    #im = Image.open(requests.get(url, stream=True).raw)
    #name = str(1) + ".jpg"
    #im.save(domain+"/static/img_temp/"+ name, "png")
    #im.save(r"../static/img_temp/" + name, "png")
    #im.save(r"static/img_temp/"+name, "png")
    #print("成功")
    #return 0

def preview_img(domain,index):
    url = []
    for i in range(0,index):
        img_url = 'https://' + domain + "/static/img_temp/" + str(i) + ".jpg"
        url.append(img_url)
    return url

def findall_chinese(s):
    return re.compile('[\u4e00-\u9fff]+').findall(s)

#print(find_today_new())
#img =  get_jpg(find_today_new())
#print("案件數量:"+str(len(img)))
#for i in range(0,len(img)):
#    print(img[i])
#url = 'https://ws.kcg.gov.tw/Download.ashx?u=LzAwMS9LY2dVcGxvYWRGaWxlcy8zMTAvY2tmaWxlLzM3ZTA5OGE0LTNmN2UtNDNiYS1iOWNjLTdkYTQ0ZWNhYWU3OUAxMDI0eDc2OC5qcGc%3d&n=Mjk2NC5qcGc%3d&Icon=.jpg'
#download_img(url)

#print(find_date_new("0603"))
#img =  get_jpg(find_date_new("0603"))
#print(img[1])
#print("案件數量:"+str(len(img)))
#for i in range(0,len(img)):
#    print(img[i])

