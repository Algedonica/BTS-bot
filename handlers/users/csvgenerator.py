import math
import csv

from datetime import datetime, timezone
from aiogram import types
from aiogram.types import InputFile, ReplyKeyboardRemove
from loader import dp, bot
from data.config import user_collection, ticket_collection, staff_collection, partner_collection
from states import ProjectManage,SupportManage
from aiogram.types import CallbackQuery,ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto
from utils.misc import isadmin,support_role_check, photoparser

from keyboards.inline import csv_tables_call

import sys,os
pathname = os.path.dirname(sys.argv[0]) 


@dp.callback_query_handler(text='to_csv_tables', state=[SupportManage.menu,SupportManage.initcsv,SupportManage.accept_time,SupportManage.inittimecsv])
async def show_menu_tables_csv(call:types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=0)
    await state.reset_state()
    await SupportManage.menu.set()
    html_text="\n".join(
        [
            'Какую таблицу вы хотите скачать?',
            'В фильтре обращений вы можете произвести фильтрацию всех данных по нужным параметрам'
        ]
    )
    supportmenubase = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(
            text='📄 Фильтр обращений',
            callback_data=csv_tables_call.new('init_csv_filtered',param1=1, param2="none")
        )],
        [InlineKeyboardButton(
            text='👥 Список клиентов',
            callback_data='init_csv_users'
        )],
        [InlineKeyboardButton(
            text='↩️ Назад',
            callback_data='supportbacktomenu'
        )]
    ])

    await call.message.edit_media(media=InputMediaPhoto(media=photoparser('gettablecsv'), caption=html_text), reply_markup=supportmenubase)

@dp.callback_query_handler(csv_tables_call.filter(command='init_csv_filtered'), state=[SupportManage.menu,SupportManage.initcsv,SupportManage.inittimecsv])
async def show_filtered_tables_csv_func(call: types.CallbackQuery, callback_data:dict, state: FSMContext):
    await call.answer(cache_time=0)
    page = callback_data.get("param1")
    page = int(page)
    prevpage = page - 1
    nextpage = page + 1
    inlinekeys = InlineKeyboardMarkup(row_width=2)
    thisoperator=staff_collection.find_one({"user_id":call.from_user.id})
    thisoperator_cities=thisoperator['city_code'][1:]
    opers=staff_collection.find({"staffrole":{"$in":["support","admin","owner"]}, "city_code": {"$in": thisoperator_cities}}).skip((page-1)*5).limit(5)
    data = await state.get_data()
    opersarray = data.get("opers")
    
    if opersarray == None:
        opersarray=[] 


    if callback_data.get("param2") != "none":
        opertoadd=int(callback_data.get("param2"))
        if opertoadd in opersarray:
            opersarray.remove(opertoadd)
        else:
            opersarray.append(opertoadd)
        await state.update_data(opers=opersarray)
    for x in opers:
        galka=""
        if x["user_id"] in opersarray:
            galka="✅"
        inlinekeys.add(InlineKeyboardButton(text=galka+x["callmeas"]+' '+x["first_name"]+' ('+support_role_check(x['user_id'])+')', callback_data=csv_tables_call.new('init_csv_filtered',param1=page, param2=x["user_id"])))

    
   
    data = await state.get_data()
    opersarray = data.get("opers")
    if prevpage < 1:
        prevtoadd=InlineKeyboardButton(
            text='◀️',
            callback_data=csv_tables_call.new('init_csv_filtered',param1=1, param2="none")
        )
    else:
        prevtoadd=InlineKeyboardButton(
            text='◀️',
            callback_data=csv_tables_call.new('init_csv_filtered',param1=prevpage, param2="none")
        )

    if  math.ceil(opers.count()/5)==page:
        nexttoadd=InlineKeyboardButton(
            text='▶️',
            callback_data=csv_tables_call.new('init_csv_filtered',param1=page, param2="none")
        )      
    else:
        nexttoadd=InlineKeyboardButton(
            text='▶️',
            callback_data=csv_tables_call.new('init_csv_filtered',param1=nextpage, param2="none")
        ) 
    html_text="\n".join(
        [
            ' '
        ]
    )
    inlinekeys.add(prevtoadd,nexttoadd)
    inlinekeys.add(InlineKeyboardButton(
        text='🌆 Выбрать город',
        callback_data=csv_tables_call.new('to_csv_cities',param1=1, param2="none")
    ))
    inlinekeys.add(InlineKeyboardButton(
        text='↩️ Назад',
        callback_data='to_csv_tables'
    ))
    await SupportManage.initcsv.set()
    # await call.message.edit_text(text=html_text, reply_markup=inlinekeys) 
    await call.message.edit_media(media=InputMediaPhoto(media=photoparser('chooseoperatorcsv'), caption=html_text), reply_markup=inlinekeys)



@dp.callback_query_handler(csv_tables_call.filter(command='to_csv_cities'), state=[SupportManage.initcsv, SupportManage.inittimecsv])
async def show_table_cities_csv_func(call: types.CallbackQuery, callback_data:dict, state: FSMContext):
    await call.answer(cache_time=0)
    page = callback_data.get("param1")
    page = int(page)
    prevpage = page - 1
    nextpage = page + 1
    inlinekeys = InlineKeyboardMarkup(row_width=2)
    thisoperator=staff_collection.find_one({"user_id":call.from_user.id})
    thisoperator_cities=thisoperator['city_code'][1:]
    cities_obj=partner_collection.find({'system_tag':{'$in': thisoperator_cities}}).skip((page-1)*5).limit(5)
    
    cities_obj_len = cities_obj.count()
    data = await state.get_data()
    citiesarray = data.get("cities")
    
    if citiesarray == None:
        citiesarray=[] 


    if callback_data.get("param2") != "none":
        citytoadd=callback_data.get("param2")
        if citytoadd in citiesarray:
            citiesarray.remove(citytoadd)
        else:
            citiesarray.append(citytoadd)
        await state.update_data(cities=citiesarray)
    for x in cities_obj:
        galka=""
        if x["system_tag"] in citiesarray:
            galka="✅"
        inlinekeys.add(InlineKeyboardButton(text=galka+x["system_tag"]+' - '+x["city_name"], callback_data=csv_tables_call.new('to_csv_cities',param1=page, param2=x["system_tag"])))

    
   
    data = await state.get_data()
    citiesarray = data.get("cities")
    if prevpage < 1:
        prevtoadd=InlineKeyboardButton(
            text='◀️',
            callback_data=csv_tables_call.new('to_csv_cities',param1=1, param2="none")
        )
    else:
        prevtoadd=InlineKeyboardButton(
            text='◀️',
            callback_data=csv_tables_call.new('to_csv_cities',param1=prevpage, param2="none")
        )

    if  math.ceil(cities_obj_len/5)==page:
        nexttoadd=InlineKeyboardButton(
            text='▶️',
            callback_data=csv_tables_call.new('to_csv_cities',param1=page, param2="none")
        )      
    else:
        nexttoadd=InlineKeyboardButton(
            text='▶️',
            callback_data=csv_tables_call.new('to_csv_cities',param1=nextpage, param2="none")
        ) 
    html_text="\n".join(
        [
            ' '
        ]
    )
    inlinekeys.add(prevtoadd,nexttoadd)
    inlinekeys.add(InlineKeyboardButton(
        text='🕟 Указать период',
        callback_data=csv_tables_call.new('to_csv_time',param1=1, param2="none")
    ))
    inlinekeys.add(InlineKeyboardButton(
        text='↩️ Назад',
        callback_data='to_csv_tables'
    ))
    await SupportManage.inittimecsv.set()
    # await call.message.edit_text(text=html_text, reply_markup=inlinekeys)
    await call.message.edit_media(media=InputMediaPhoto(media=photoparser('choosecitycsv'), caption=html_text), reply_markup=inlinekeys)

@dp.callback_query_handler(csv_tables_call.filter(command='to_csv_time'), state=[SupportManage.accept_time, SupportManage.inittimecsv])
async def show_table_time_csv_func(call: types.CallbackQuery, callback_data:dict, state: FSMContext):
    
    html_text="\n".join(
        [
            'Для сбора информации за определенный период необходимо указать даты с - по, в формате: <b>число/месяц/год</b>, как показано в примере выше.'
        ]
    )
    inlinekeys = InlineKeyboardMarkup(row_width=2)
    inlinekeys.add(InlineKeyboardButton(
        text='↩️ Назад',
        callback_data='to_csv_tables'
    ))
    await SupportManage.accept_time.set()
    await call.message.edit_media(media=InputMediaPhoto(media=photoparser('choosetimecsv'), caption=html_text), reply_markup=inlinekeys)

@dp.message_handler(state=SupportManage.accept_time)
async def accept_time_csv_func(message: types.Message, state: FSMContext):
    thismsg=message.text
    thismsg = thismsg.split(' ')

    # try:
    timefrom = thismsg[0]
    timefrom = timefrom.split('-')
    timefrom = datetime(year=int(timefrom[2]), month=int(timefrom[1]), day=int(timefrom[0]))

    timeto = thismsg[1]
    timeto = timeto.split('-') 
    timeto = datetime(year=int(timeto[2]), month=int(timeto[1]), day=int(timeto[0]))


    try:
        data = await state.get_data()
        cities = data.get('cities')
        opers = data.get('opers')

        tickets_found=ticket_collection.find({"operator": {"$in": opers}, "citytag": {"$in": cities}, "date": { "$gte": timefrom, "$lte":timeto }})

        await message.answer(text="Идет генерация файла",reply_markup=None)
        currentdate = datetime.utcnow().strftime("%d.%m.%Y-%I.%M%p")+'_tickets_by_opers_cities_time.csv'

        with open(currentdate, 'w', encoding='utf8',newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Ticket ID',
                'Created', 
                'Question', 
                'Ticket status', 
                'Client_username',
                'Client_name',
                'Client_id', 
                'Client_callmeas', 
                'Came_when', 
                'Came_from', 
                'Operator ID', 
                'Operator_username', 
                'Operator_name', 
                'Operator_callmeas',
                'Message_data',])  
            for x in tickets_found:
                thisuser = user_collection.find_one({"user_id":x["userid"]})
                thisoperator = staff_collection.find_one({"user_id":x["operator"]})

                ticketcreatedat = x['date'].strftime("%d/%m/%Y %I:%M%p")
                thisusercamewhen = thisuser['when_came'].strftime("%d/%m/%Y %I:%M%p")

                ticketstatus=x['isopen']
                if ticketstatus == "onair":
                    ticketstatus = "В процессе"
                elif ticketstatus == "onpause":
                    ticketstatus = "Приостановлен"
                elif ticketstatus == "created":
                    ticketstatus = "Создан"
                elif ticketstatus == "closedbyclient":
                    ticketstatus = "Завершен клиентом"
                elif ticketstatus == "closedbyoperator":
                    ticketstatus = "Завершен оператором"



                writer.writerow([
                    x['ticketid'], 
                    ticketcreatedat, 
                    x['title'], 
                    ticketstatus, 
                    thisuser['username'], 
                    str(thisuser['first_name'])+' '+str(thisuser['last_name']),
                    thisuser['user_id'],
                    thisuser['callmeas'],
                    thisusercamewhen,
                    thisuser['came_from'],
                    thisoperator['user_id'],
                    thisoperator['username'],
                    thisoperator['first_name']+' '+thisoperator['last_name'],
                    thisoperator['callmeas'],
                    x['messagedata'],
                    ])
        pathfinal = os.path.join(pathname, currentdate)
        await bot.send_document(chat_id=message.from_user.id, document=InputFile(pathfinal))
        os.remove(pathfinal)
        await state.reset_state()
        await SupportManage.menu.set()
        html_text="\n".join(
            [
                '<b>Таблица сформирована.</b>',
                '<i>Если при открытии будет отображаться нечитаемый текст (кодировка), то рекомендуем импортировать таблицу в Google Docs.</i>'
            ]
        )
        inlinekeys= InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [InlineKeyboardButton(
                text='↩️ Назад',
                callback_data='supportbacktomenu'
            )]
        ])
        await message.answer_photo(photo=photoparser('donecsv'), caption=html_text, reply_markup=inlinekeys)
    except:
        await message.answer(text="Вы ввели промежуток неверно")

@dp.callback_query_handler(text='init_csv_users', state=SupportManage.menu)
async def user_tables_csv(call:types.CallbackQuery, state: FSMContext):
    thisoperator=staff_collection.find_one({"user_id":call.from_user.id})
    thisoperator_cities=thisoperator['city_code'][1:]
    avaiableusers=user_collection.find({'citytag':{"$in": thisoperator_cities}})

    await call.message.answer(text="Идет генерация файла",reply_markup=None)
    currentdate = datetime.utcnow().strftime("%d.%m.%Y-%I.%M%p")+'_users.csv'

    with open(currentdate, 'w', encoding='utf8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Came from',
            'Came at', 
            'City', 
            'Client name', 
            'Client username',
            'Client call me as',
            'Last ticket', 
            'Ticket amount', 
            'Tickets ID',
            'Client ID'])  
        for x in avaiableusers:
            thisusercamewhen = x['when_came'].strftime("%d/%m/%Y %I:%M%p")

            alltickets = ticket_collection.find({'userid':x['user_id']})
            dataticketids=''
            for y in alltickets:
                dataticketids="\n".join(
                    [
                        dataticketids,
                        y['ticketid']
                    ]
                )
            

            tod = datetime.now()
          
            lastticket = ticket_collection.find({'userid':x['user_id']}).sort([("ticketid", 1), ("date", -1)]).limit(1)

            for p in lastticket:
                lastdate= p['date']

            actual_ago=tod-lastdate        
            writer.writerow([
                x['came_from'], 
                thisusercamewhen, 
                x['city'], 
                str(x['first_name'])+' '+str(x['last_name']),
                x['username'],
                x['callmeas'],
                str(actual_ago.days)+' days ago',
                alltickets.count(),
                dataticketids,
                x['user_id'],
                ])
    pathfinal = os.path.join(pathname, currentdate)
    await bot.send_document(chat_id=call.from_user.id, document=InputFile(pathfinal))
    os.remove(pathfinal)
