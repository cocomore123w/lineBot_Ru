from django.shortcuts import render

from DD import reply
from DD import lib
from DD import orderLib
from DD import redisLib
from  DD import covid19_kao
from DD import  dataBackup
# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
#from linebot.models import MessageEvent, TextSendMessage

#from linebot.models import MessageEvent, TextMessage, TextSendMessage

from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    ImageSendMessage,
    FollowEvent,
    UnfollowEvent,
    JoinEvent,
    LeaveEvent,
    FlexSendMessage,
    AudioSendMessage,
    BubbleContainer,
    ImageComponent,
    URIAction
)
import math
##
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


#silent_flag = False#lib.flag_value(False)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

    ###############
        #global silent_flag
        for event in events:
            print(events)
            #print(lib.silent_flag)
            silent_flag = redisLib.varGetbyte2dict("silent_flag")
            #print(silent_flag)
            #lib.silent_flag = dataBackup.data_json.jsonRead_SilentFlag()
            try:
                if isinstance(event, MessageEvent):  # 如果有訊息事件
                    if event.message.text.split(' ')[0] == "#sd" and event.source.user_id == lib.master_id:  ##to do:
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TextSendMessage(text=orderLib.Order.superuserOrder(event))
                        )
                    elif  silent_flag ==False:
                        if event.message.text == "#說明":
                            flex_message = FlexSendMessage('call menu',reply.flexload("menu.json"))
                            line_bot_api.reply_message(event.reply_token, flex_message)
                            print("說明")
                        elif event.message.text == "#使用說明":
                            #flex_message = FlexSendMessage('how to use', reply.flexload("howtouse.json"))
                            flex_message = FlexSendMessage('how to use', reply.flexload("how2use_2.json"))
                            line_bot_api.reply_message(event.reply_token, flex_message)
                            print("使用說明")
                            '''''''''
                        elif event.message.text == "#高雄確診":
                            news = covid19_kao.find_today_new()
                            if news == None:
                                txt = "本日資料尚未更新\n可以使用#高雄確診 日期(ex:0519)\n來查詢"
                                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=txt))
                            else:
                                img = covid19_kao.get_jpg(news)
                                if img[0] == "txt":
                                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=img[1]))
                                    break
                                message_group = []
                                message = []
                                #print( len(img))
                                count =math.ceil(len(img) / 5)
                                surplus = len(img) - (count-1) * 5
                                #print(surplus)
                                for j in range(0,count):
                                    if j ==count-1:
                                        for i in range(0, surplus):
                                            message.append(ImageSendMessage(original_content_url=img[i+j*5], preview_image_url=img[i+j*5]))
                                    else:
                                        for i in range(0, 5):
                                            message.append(ImageSendMessage(original_content_url=img[i+j*5], preview_image_url=img[i+j*5]))
    
                                    message_group.append(message)
                                    #print(message_group)
                                    message = []
                                #message.append(ImageSendMessage(original_content_url=img[i], preview_image_url=img_a))
                            #line_bot_api.reply_message(event.reply_token, message)
                            #print(message_group)
                                if event.source.type == "user":
                                    for i in range(0,count):
                                        line_bot_api.push_message(event.source.user_id,message_group[i])
                                else:
                                    for i in range(0, count):
                                        line_bot_api.push_message(event.source.group_id, message_group[i])
                        elif event.message.text.split(" ")[0] == "#高雄確診":
                            _date = reply.keyword(event)
                            if _date == None :
                                line_bot_api.reply_message(  # 回復傳入的訊息文字
                                    event.reply_token,
                                    TextSendMessage(text="格式錯誤")
                                )
                            else:
                                #img_a = 'https://media.discordapp.net/attachments/634316340794228746/845317902369423410/2964.jpg?width=624&height=468'
                                news = covid19_kao.find_date_new(_date)
                                if news == None:
                                    txt = "該日期沒有資料"
                                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=txt))
                                else:
                                    img = covid19_kao.get_jpg(news)
                                    if img[0] == "txt":
                                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=img[1]))
                                        break
                                    message_group = []
                                    message = []
                                    print(len(img))
                                    count = math.ceil(len(img) / 5)
                                    surplus = len(img) - (count - 1) * 5
                                    print(surplus)
                                    for j in range(0, count):
                                        if j == count - 1:
                                            for i in range(0, surplus):
                                                message.append(ImageSendMessage(original_content_url=img[i + j * 5],
                                                                            preview_image_url=img[i + j * 5]))
                                        else:
                                            for i in range(0, 5):
                                                message.append(ImageSendMessage(original_content_url=img[i + j * 5],
                                                                            preview_image_url=img[i + j * 5]))
    
                                        message_group.append(message)
                                    # print(message_group)
                                        message = []
                                    # message.append(ImageSendMessage(original_content_url=img[i], preview_image_url=img_a))
                                # line_bot_api.reply_message(event.reply_token, message)
                                # print(message_group)
                                    if event.source.type == "user":
                                        for i in range(0, count):
                                            line_bot_api.push_message(event.source.user_id, message_group[i])
                                    else:
                                        for i in range(0, count):
                                            line_bot_api.push_message(event.source.group_id, message_group[i])
                            '''
                        else:
                            bot_ans = reply.keyword(event)
                            if bot_ans == None:
                                break
                            else:
                                line_bot_api.reply_message(                     # 回復傳入的訊息文字
                                event.reply_token,
                                TextSendMessage(text=bot_ans))
                                print("MessageEvent")

                elif isinstance(event, FollowEvent):
                    # print
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply.followContent(event))
                    )
                    ##save user id
                    reply.follow_join(event)
                    print("FollowEvent")

                elif isinstance(event, UnfollowEvent):
                    ###save group id
                    reply.unfollow_leave(event)
                    print("UnfollowEvent")

                elif isinstance(event, JoinEvent):
                    ###save group id
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply.followContent(event))
                    )
                    reply.follow_join(event)
                    print("JoinEvent")

                elif isinstance(event, LeaveEvent):
                    ###delet group id
                    reply.unfollow_leave(event)
                    print("LeaveEvent")

            except AttributeError:
                break

            #elif isinstance(event, LeaveEvent):
            #
        return HttpResponse()
    ################

    else:
        return HttpResponseBadRequest()
