from data.config import partner_collection,staff_collection, ticket_collection, settings_collection, pmessages_collection, videos_collection, photos_collection, videocircles_collection, channelid, user_collection, links_collection
from loader import dp, bot
from datetime import datetime
def issupport(x):
    thisuser=staff_collection.find({"user_id":x, "$or":[{"staffrole":"support"},{"staffrole":"owner"}, {"staffrole":"admin"}]})
    if thisuser.count()==1:
        return True      
    else:
        return False
def isowner(x):
    thisuser=staff_collection.find({"user_id":x, "$or":[{"staffrole":"owner"}]})
    if thisuser.count()==1:
        return True      
    else:
        return False
def isadmin(x):
    thisuser=staff_collection.find({"user_id":x, "$or":[{"staffrole":"owner"},{"staffrole":"admin"}]})
    if thisuser.count()==1:
        return True      
    else:
        return False

def support_role_check(x):
    thisuser=staff_collection.find_one({"user_id":x})
    if thisuser["role"]=="1":
        return 'MAIN'      
    else:
        return 'PLUS'
# def parse_city(x):
#     asd=settings_collection.find_one({"settings":"mainsettings"})
#     cities_obj=asd["current_cities"]
#     gotcha=""
#     for y in cities_obj:
#         if x == y['code']:
#             gotcha = y['city']
#             break
#     return gotcha

def get_user_city(x):
    asd=user_collection.find_one({'user_id':x})
    cities_obj=asd["citytag"]
    return cities_obj

def get_user_came_from(x):
    asd=user_collection.find_one({'user_id':x})
    cities_obj=asd["came_from"]
    return cities_obj

def parse_message_by_tag_name(x):
    asd = pmessages_collection.find_one({"tag_name":x})
    if asd==None:
        return ''
    return asd['text']

async def check_error_ticket(x):
    asd = ticket_collection.find_one({'ticketid':x})
    if asd==None:
        
        return ''
    elif asd['isopen']=='created':
        returning='Невозможно переключиться на обращение. Возможно клиент заблокировал бота.'
        
        counttickets=ticket_collection.find().count()+1

        if asd['operator']=='none':
            
            operatorcallmeas='none'
            operatornickname='none'
        else:
            operatornickname=staff_collection.find_one({'user_id':asd['operator']})
            operatorcallmeas=operatornickname['callmeas']
            operatornickname=operatornickname['username']

        clientnickname=user_collection.find_one({'user_id':asd['userid']})
        clientcallmeas=clientnickname['callmeas']
        clientnickname=clientnickname['username']

        if operatornickname=='none':
            operatornickname='Без ника'
        else:
            operatornickname="@"+operatornickname

        if clientnickname=='none':
            clientnickname='Без ника'
        else:
            clientnickname="@"+clientnickname
        datamessagehere = "\n".join(
            [
                '<b>Обращение № '+str(counttickets)+'</b>',
                asd['title'],
                '',
                '🗣 '+clientnickname+' - '+clientcallmeas,
                '👨‍💻 '+operatornickname+' - '+operatorcallmeas,
                '',
                '<i>'+asd['date'].strftime("%d.%m.%Y / %H:%M")+'</i>',
                asd['ticketid'],
                '',
                asd["messagedata"],
                '',
                '<b>‼️Ошибка, похоже клиент забанил бота‼️</b> <i>('+datetime.now().strftime("%d.%m.%Y / %H:%M")+')</i>',
                '',
                '=========================',
                '',
                "Диалог закрыт с ошибкой (клиент забанил бота) ",
                "<i>"+datetime.now().strftime("%d.%m.%Y / %H:%M")+"</i>"

            ]
        ) 
        ticket_collection.update({"ticketid": asd['ticketid'], "isopen": "created"},{"$set":{"isopen":"botbanned","messagedata":datamessagehere}})
        await bot.send_message(chat_id=channelid, text=datamessagehere)

        return returning
    elif asd['isopen']=='paused':
        returning='Невозможно переключиться на обращение. Возможно клиент заблокировал бота.'
    
        counttickets=ticket_collection.find().count()+1

        if asd['operator']=='none':
            
            operatorcallmeas='none'
            operatornickname='none'
        else:
            operatornickname=staff_collection.find_one({'user_id':asd['operator']})
            operatorcallmeas=operatornickname['callmeas']
            operatornickname=operatornickname['username']

        clientnickname=user_collection.find_one({'user_id':asd['userid']})
        clientcallmeas=clientnickname['callmeas']
        clientnickname=clientnickname['username']

        if operatornickname=='none':
            operatornickname='Без ника'
        else:
            operatornickname="@"+operatornickname

        if clientnickname=='none':
            clientnickname='Без ника'
        else:
            clientnickname="@"+clientnickname
        datamessagehere = "\n".join(
            [
                '<b>Обращение № '+str(counttickets)+'</b>',
                asd['title'],
                '',
                '🗣 '+clientnickname+' - '+clientcallmeas,
                '👨‍💻 '+operatornickname+' - '+operatorcallmeas,
                '',
                '<i>'+asd['date'].strftime("%d.%m.%Y / %H:%M")+'</i>',
                asd['ticketid'],
                '',
                asd["messagedata"],
                '',
                '<b>‼️Ошибка, похоже клиент забанил бота‼️</b> <i>('+datetime.now().strftime("%d.%m.%Y / %H:%M")+')</i>',
                '',
                '=========================',
                '',
                "Диалог закрыт с ошибкой (клиент забанил бота) ",
                "<i>"+datetime.now().strftime("%d.%m.%Y / %H:%M")+"</i>"

            ]
        ) 
        ticket_collection.update({"ticketid": asd['ticketid'], "isopen": "paused"},{"$set":{"isopen":"botbanned","messagedata":datamessagehere}})
        bot.send_message(chat_id=channelid, text=datamessagehere)

        return returning
    elif asd['isopen']=='onair':
        returning='Невозможно переключиться на обращение. Другой оператор уже начал диалог.'
        print('tut4')
        return returning
    else:
        print('tut5')
        returning='Невозможно переключиться на обращение. Неизвестная ошибка.'
        return returning

# -----------------media----parsers-----------------------


def parse_video_by_tag_name(x):
    asd = videos_collection.find_one({"name":x})
    if asd==None:
        return ''
    return asd['video_id']

def parse_photos_by_tag_name(x):
    asd = photos_collection.find_one({"name":x})
    if asd==None:
        return ''
    return asd['photo_id']


def parse_videocircles_by_tag_name(x):
    asd = videocircles_collection.find_one({"name":x})
    if asd==None:
        return ''
    return asd['videocircle_id']

def photoparser(x):
    asd = photos_collection.find_one({"name":x})
    if asd==None:
        return ''
    return asd['photo_id']



# -----------------media----parsers----end--------------

def xstr(s):
    if s is None:
        return 'none'
    return str(s)


def send_to_channel(x):
    asd = ticket_collection.find_one({"ticketid":x})
    bot.send_message(chat_id=channelid, text=asd['messagedata'])
    return False



def linkparser(x):
    asd = links_collection.find_one({"uniquename":x})
    if asd!=None:
        return asd['city'], asd['citycode'], asd['social']
    else:
        asd = links_collection.find_one({"uniquename":'default'})
        return asd['city'], asd['citycode'], asd['social']
def linkparser_default():
    asd = links_collection.find_one({"uniquename":'default'})
    return asd['city'], asd['citycode'], asd['social']    

def system_text_parser(x):
    asd=settings_collection.find_one({"settings":"mainsettings"})
    mytext=asd['text_system'][x]
    return mytext

def get_partner_obj(x):
    asd=partner_collection.find_one({'system_tag':x})
    return asd
