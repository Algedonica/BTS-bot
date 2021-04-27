from data.config import staff_collection, ticket_collection, settings_collection, pmessages_collection, videos_collection, photos_collection, videocircles_collection, channelid
from loader import dp, bot

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
def parse_city(x):
    asd=settings_collection.find_one({"settings":"mainsettings"})
    cities_obj=asd["current_cities"]
    gotcha=""
    for y in cities_obj:
        if x == y['code']:
            gotcha = y['city']
            break
    
    return gotcha

def parse_message_by_tag_name(x):
    asd = pmessages_collection.find_one({"tag_name":x})
    if asd==None:
        return ''
    return asd['text']


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



# def photoparser(x):
    


#     asd = settings_collection.find_one({"settings":"mainsettings"})
#     photo_arr = asd['photos_system']
#     if x == "changed":
#         return photo_arr[0]
#     elif x == "clientfinished":
#         return photo_arr[1]
#     elif x == "new_question":
#         return photo_arr[2]
#     elif x == "paused":
#         return photo_arr[3]
#     elif x == "silent":
#         return photo_arr[4]
#     elif x == "waiting":
#         return photo_arr[5]
#     elif x == "adminpanel":
#         return photo_arr[6]
#     elif x == "chooseoperatorcsv":
#         return photo_arr[7]
#     elif x == "choosecitycsv":
#         return photo_arr[8] 
#     elif x == "choosetimecsv":
#         return photo_arr[9]
#     elif x == "donecsv":
#         return photo_arr[10]
#     elif x == "gettablecsv":
#         return photo_arr[11]
#     elif x == "citieslist":
#         return photo_arr[12]
#     elif x == "operatorcitiesaccess":
#         return photo_arr[13]
#     elif x == "operatornameupdated":
#         return photo_arr[14]      
#     elif x == "nameroletags":
#         return photo_arr[15]
#     elif x == "operatorchangename":
#         return photo_arr[16] 
#     elif x == "operatorticketfinished":
#         return photo_arr[17] 
#     elif x == "operatorlist":
#         return photo_arr[18]
#     elif x == "deleteoperatorask":
#         return photo_arr[19]
#     elif x == "deletetagask":
#         return photo_arr[20]
#     elif x == "operatormanage":
#         return photo_arr[21]
#     elif x == "operatormainmenu":
#         return photo_arr[22]
#     elif x == "usermainmenu":
#         return photo_arr[23]
#     elif x == "useraskcity":
#         return photo_arr[24]
#     elif x == "userwritecity":
#         return photo_arr[25]
#     elif x == "userknowledgebase":
#         return photo_arr[26]
#     elif x == "adminknowledgebase":
#         return photo_arr[27]
#     elif x == "adminknowledgebase_change_name":
#         return photo_arr[28]
#     elif x == "adminknowledgebase_change_name_done":
#         return photo_arr[29]
