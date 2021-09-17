from datetime import datetime
from aiogram import types
from loader import dp, bot
from data.config import user_collection, ticket_collection, staff_collection, settings_collection, states_collection, pmessages_collection, channelid
from states import ProjectManage,SupportManage
from aiogram.types import CallbackQuery,ReplyKeyboardRemove, InputFile
from aiogram.utils.callback_data import CallbackData
from utils.misc.logging import logging
from utils.misc import rate_limit
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import InputMediaPhoto
from utils.misc import get_partner_channel, build_support_menu,isadmin,support_role_check, xstr, photoparser, parse_message_by_tag_name, getCryptoData, parse_video_by_tag_name, send_to_channel, issupport

from keyboards.inline import usersupportchoiceinline, ticket_callback, add_operator_callback, show_support_pages, edit_something_admin, show_cities_pages, knowledge_list_call
from keyboards.default import userendsupport,defaultmenu, operatorcontrol,operatorshowuser
@dp.message_handler(text="/reset", state=[
    ProjectManage
    ])
async def resetbot_byuser(message: types.Message):
    thisicket=ticket_collection.find_one({"userid": message.from_user.id, "$or":[{'isopen':'onair'},{'isopen':'onpause'}, {'isopen':'created'}]})
    if thisicket!=None:
        counttickets=ticket_collection.find().count()+1
      
        if thisicket['operator']=='none':
            
            operatorcallmeas='none'
            operatornickname='none'
        else:
            operatornickname=staff_collection.find_one({'user_id':thisicket['operator']})
            operatorcallmeas=operatornickname['callmeas']
            operatornickname=operatornickname['username']

        clientnickname=user_collection.find_one({'user_id':thisicket['userid']})
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
                '<b>№'+str(counttickets)+' '+thisicket['citytag']+'</b>',
                '<b>'+thisicket['title']+'</b>',
                '🗣 '+clientnickname+' - '+clientcallmeas+' - tg ID:'+str(thisicket['userid']),
                '<i>'+thisicket['date'].strftime("%d.%m.%Y / %H:%M")+'</i>',
                '',
                '👨‍💻 '+operatornickname+' - '+operatorcallmeas,
                thisicket['ticketid'],
                '',
                '===',
                "🗣 Закрыт клиентом",
                "<i>"+datetime.now().strftime("%d.%m.%Y / %H:%M")+"</i>"

            ]
        ) 
        tomad= "\n".join([
            "Диалог закрыт клиентом ",
            "<i>"+datetime.now().strftime("%d.%m.%Y / %H:%M")+"</i>"
        ])
        extradd={
            "side":"fromuser" ,
            "date": datetime.now(),
            "text":tomad,
            "from_id":message.from_user.id,
            "message_from_id":message.message_id,
            "type":"text",
            "mediaid":"none",
            "isread":True}

        photos=await bot.get_user_profile_photos(user_id=thisicket['userid'], limit=1)

        if photos.total_count>0:
            photofinal=photos.photos[0][0].file_id

            mesid=await bot.send_photo(chat_id=channelid, caption=datamessagehere, photo=photofinal)   
            channelid_partner=get_partner_channel(thisicket['citytag'])
            if channelid_partner!='none':
                mesid_partner=await bot.send_photo(chat_id=channelid_partner, caption=datamessagehere, photo=photofinal)  
                ticket_collection.update({"userid": message.from_user.id, "$or":[{'isopen':'onair'},{'isopen':'onpause'}, {'isopen':'created'}]},{"$set":{"isopen":"closedbyclient", "messagedata":datamessagehere, 'original_id':mesid['message_id'], 'original_channel':mesid['sender_chat']['id'], 'original_id_partner':mesid_partner['message_id'], 'original_channel_partner':mesid_partner['sender_chat']['id']}, '$addToSet': { 'extrafield': extradd } })
            ticket_collection.update({"userid": message.from_user.id, "$or":[{'isopen':'onair'},{'isopen':'onpause'}, {'isopen':'created'}]},{"$set":{"isopen":"closedbyclient", "messagedata":datamessagehere, 'original_id':mesid['message_id'], 'original_channel':mesid['sender_chat']['id'], 'original_id_partner':'none', 'original_channel_partner':'none',}, '$addToSet': { 'extrafield': extradd } })

        else:
            mesid=await bot.send_message(chat_id=channelid, text=datamessagehere)   
            channelid_partner=get_partner_channel(thisicket['citytag'])
            if channelid_partner!='none':
                mesid_partner=await bot.send_message(chat_id=channelid_partner, text=datamessagehere)
                ticket_collection.update({"userid": message.from_user.id, "$or":[{'isopen':'onair'},{'isopen':'onpause'}, {'isopen':'created'}]},{"$set":{"isopen":"closedbyclient", "messagedata":datamessagehere, 'original_id':mesid['message_id'], 'original_channel':mesid['sender_chat']['id'], 'original_id_partner':mesid_partner['message_id'], 'original_channel_partner':mesid_partner['sender_chat']['id']}, '$addToSet': { 'extrafield': extradd } })
            ticket_collection.update({"userid": message.from_user.id, "$or":[{'isopen':'onair'},{'isopen':'onpause'}, {'isopen':'created'}]},{"$set":{"isopen":"closedbyclient", "messagedata":datamessagehere, 'original_id':mesid['message_id'], 'original_channel':mesid['sender_chat']['id'], 'original_id_partner':'none', 'original_channel_partner':'none',}, '$addToSet': { 'extrafield': extradd } })

        if thisicket['operator']!='none':
            html_text2="\n".join(
                [
                    '<b>🤖 Бот КриптоКонсалтинг:</b>',
                    '',
                    'Клиент завершил диалог, нажмите на ❌ Завершить'
                ]
            )
            endinline= InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                [InlineKeyboardButton(
                    text='❌ Завершить',
                    callback_data='operator_end_inline_ticket'
                )]
            ]) 
            await bot.send_photo(chat_id=thisicket['operator'],parse_mode='HTML', photo=photoparser('clientfinished'), reply_markup=ReplyKeyboardRemove())
            await bot.send_message(chat_id=thisicket['operator'], text=html_text2,parse_mode='HTML',reply_markup=endinline)
    thisuser=user_collection.find_one({'user_id':message.from_user.id})
    html_text="\n".join(
        [
            '<b>💎 ООО «Крипто Консалтинг»</b>',
            '',
            '<b>Профессионально окажем консультацию в сфере криптовалют, а также расскажем о заработке, хранении, уплате налогов и переводах.</b>',
            '',
            '🗣 Консультация и обучение',
            '💲 Доверительное управление',
            '🎓 Юридическое сопровождение',
            '🛡 Холодное хранение',
            '💱 Легальный обмен',
            '',
            'Подписывайтесь на наш Telegram канал:',
            '👉 @cryptocons 👈',
            # parse_message_by_tag_name(thisuser['citytag'])
        ]
    )
    
    await message.answer_photo(photo=photoparser('usermainmenu'), caption=html_text,parse_mode='HTML',reply_markup=defaultmenu)
    await ProjectManage.menu.set()



@dp.message_handler(text="/reset", state=[
    SupportManage
    ])
async def resetbot_byoperator(message: types.Message, state: FSMContext):
    thisicket=ticket_collection.find_one({"operator": message.from_user.id,"isopen": "onair"}) 
    if thisicket!=None:
        counttickets=ticket_collection.find().count()+1

        operatornickname=staff_collection.find_one({'user_id':thisicket['operator']})
        operatorcallmeas=operatornickname['callmeas']
        operatornickname=operatornickname['username']

        clientnickname=user_collection.find_one({'user_id':thisicket['userid']})
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
                '<b>№'+str(counttickets)+' '+thisicket['citytag']+'</b>',
                '<b>'+thisicket['title']+'</b>',
                '🗣 '+clientnickname+' - '+clientcallmeas+' - tg ID:'+str(thisicket['userid']),
                '<i>'+thisicket['date'].strftime("%d.%m.%Y / %H:%M")+'</i>',
                '',
                '👨‍💻 '+operatornickname+' - '+operatorcallmeas,
                thisicket['ticketid'],
                '',
                '===',
                "👨‍💻 Закрыт оператором",
                "<i>"+datetime.now().strftime("%d.%m.%Y / %H:%M")+"</i>"

            ]
        )
        # ticket_collection.update({"operator": message.from_user.id, "isopen": "onair"},{"$set":{"isopen":"closedbyoperator","messagedata":datamessagehere}})
        
        html_text2="\n".join(
            [
                ' ',
            ]
        )
        clientgotomenu= InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [InlineKeyboardButton(
                text='✅ Завершить и выйти в меню',
                callback_data='to_client_menu'
            )]
        ]) 
        await bot.send_photo(chat_id=thisicket['userid'],photo=photoparser('operatorticketfinished') ,caption=html_text2,parse_mode='HTML',reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=thisicket['userid'],text='Оператор завершил диалог',parse_mode='HTML',reply_markup=clientgotomenu)
        tomad= "\n".join([
            "Диалог закрыт оператором ",
            "<i>"+datetime.now().strftime("%d.%m.%Y / %H:%M")+"</i>"
        ])
        extradd={
            "side":"fromoperator" ,
            "date": datetime.now(),
            "text":tomad,
            "from_id":message.from_user.id,
            "message_from_id":message.message_id,
            "type":"text",
            "mediaid":"none",
            "isread":True}


        photos=await bot.get_user_profile_photos(user_id=thisicket['userid'], limit=1)

        if photos.total_count>0:
            photofinal=photos.photos[0][0].file_id

            mesid=await bot.send_photo(chat_id=channelid, caption=datamessagehere, photo=photofinal)
            channelid_partner=get_partner_channel(thisicket['citytag'])
            if channelid_partner!='none':
                mesid_partner=await bot.send_photo(chat_id=channelid_partner, caption=datamessagehere, photo=photofinal)
                ticket_collection.update({"ticketid":thisicket['ticketid']},{"$set":{"isopen":"closedbyoperator","messagedata":datamessagehere,'original_id':mesid['message_id'], 'original_channel':mesid['sender_chat']['id'],'original_id_partner':mesid_partner['message_id'], 'original_channel_partner':mesid_partner['sender_chat']['id']},'$addToSet': { 'extrafield': extradd }})
            ticket_collection.update({"ticketid":thisicket['ticketid']},{"$set":{"isopen":"closedbyoperator","messagedata":datamessagehere,'original_id':mesid['message_id'], 'original_channel':mesid['sender_chat']['id']},'$addToSet': { 'extrafield': extradd }})
            

        else:
            mesid=await bot.send_message(chat_id=channelid, text=datamessagehere)
            channelid_partner=get_partner_channel(thisicket['citytag'])
            if channelid_partner!='none':
                mesid_partner=await bot.send_message(chat_id=channelid_partner, text=datamessagehere)
                ticket_collection.update({"ticketid":thisicket['ticketid']},{"$set":{"isopen":"closedbyoperator","messagedata":datamessagehere,'original_id':mesid['message_id'], 'original_channel':mesid['sender_chat']['id'],'original_id_partner':mesid_partner['message_id'], 'original_channel_partner':mesid_partner['sender_chat']['id']},'$addToSet': { 'extrafield': extradd }})
            ticket_collection.update({"ticketid":thisicket['ticketid']},{"$set":{"isopen":"closedbyoperator","messagedata":datamessagehere,'original_id':mesid['message_id'], 'original_channel':mesid['sender_chat']['id']},'$addToSet': { 'extrafield': extradd }})
            
    html_text,supportmenubase=build_support_menu(message.from_user.id)
         
    await bot.send_message(chat_id=message.from_user.id,text='Успешно',parse_mode='HTML',reply_markup=ReplyKeyboardRemove())
    await bot.send_photo(chat_id=message.from_user.id,photo=photoparser("operatormainmenu"), caption=html_text,parse_mode='HTML',reply_markup=supportmenubase ) 
    await state.reset_state()
    await SupportManage.menu.set()
    



@dp.message_handler(text="/vm", state=[SupportManage.menu])
async def reverserole_for_staff(message: types.Message, state: FSMContext):
    if issupport(message.from_user.id)==True:
        await state.reset_state()
        await ProjectManage.menu.set()
        staff_collection.find_and_modify( 
            query={"user_id":message.from_user.id}, 
            update={ "$set": { 'isreverse': True} }
            )
        await message.answer('Напишите что-нибудь', reply_markup=ReplyKeyboardRemove()) 

@dp.message_handler(text="/vm", state=[ProjectManage.menu])
async def reverserole_for_staff(message: types.Message, state: FSMContext):
    if issupport(message.from_user.id)==True:
        await state.reset_state()
        await SupportManage.menu.set() 
        staff_collection.find_and_modify( 
            query={"user_id":message.from_user.id}, 
            update={ "$set": { 'isreverse': False} }
            )
        await message.answer('Напишите что-нибудь', reply_markup=ReplyKeyboardRemove())    

@dp.message_handler(text="/push", state=[SupportManage.menu])
async def reversenotifications_for_staff(message: types.Message, state: FSMContext):
    if issupport(message.from_user.id)==True:
        thisstaff=staff_collection.find_one({"user_id":message.from_user.id})

        if thisstaff['notified']=='disabled':
            staff_collection.find_and_modify( 
                query={"user_id":message.from_user.id}, 
                update={ "$set": { 'notified': 'none'} }
                )
            await message.answer('<b>Уведомления включены. Для продолжения отправьте любое сообщение.</b>')
        elif thisstaff['notified']=='none':
            staff_collection.find_and_modify( 
                query={"user_id":message.from_user.id}, 
                update={ "$set": { 'notified': 'disabled'} }
                )
            await message.answer('<b>Уведомления отключены. Для продолжения отправьте любое сообщение.</b>')
        elif thisstaff['notified']=='notified':
            staff_collection.find_and_modify( 
                query={"user_id":message.from_user.id}, 
                update={ "$set": { 'notified': 'disabled'} }
                )
            await message.answer('<b>Уведомления отключены. Для продолжения отправьте любое сообщение.</b>')


# inlinekeyb.add(InlineKeyboardButton(text="↩️ в меню",callback_data='supportbacktomenu'))






@dp.callback_query_handler(text='to_extra_msg', state=SupportManage.menu)
async def to_extra_msg(call: types.CallbackQuery):
    html_text="\n".join(
        [
            'Введите ID пользователя Telegram',
        ]
    )
    inlinekeyb=InlineKeyboardMarkup(row_width=1)
    inlinekeyb.add(InlineKeyboardButton(text="↩️ Отменить и вернуться в меню",callback_data='supportbacktomenutwo'))
    await call.message.delete()
    await call.message.answer(text=html_text,reply_markup=inlinekeyb)
    await SupportManage.extra_message_init.set()


@dp.message_handler(state=[SupportManage.extra_message_init])
async def extra_msg_idgot(message: types.Message, state:FSMContext):
    html_text="\n".join(
        [
            'Напишите сообщение, которое нужно доставить пользователю.',
        ]
    )
    inlinekeyb=InlineKeyboardMarkup(row_width=1)
    inlinekeyb.add(InlineKeyboardButton(text="↩️ Отменить и вернуться в меню",callback_data='supportbacktomenutwo'))
    await message.answer(text=html_text,reply_markup=inlinekeyb)
    await SupportManage.extra_message_text.set()
    await state.update_data(userid=message.text)

@dp.message_handler(state=[SupportManage.extra_message_text])
async def extra_msg_idgot(message: types.Message, state:FSMContext):
    data = await state.get_data()
    userid = int(data.get("userid"))
    message_user=message.text

    try:
        await bot.send_message(chat_id=userid, text=message_user)
        html_text="\n".join(
            [
                'Готово',
            ]
        )
        inlinekeyb=InlineKeyboardMarkup(row_width=1)
        inlinekeyb.add(InlineKeyboardButton(text="↩️ В меню",callback_data='supportbacktomenutwo'))
        await message.answer(text=html_text,reply_markup=inlinekeyb)
    except:
        html_text="\n".join(
            [
                'Данный пользователь не найден в базе данных или бот был заблокирован.',
                'Пожалуйста, вернитесь в главное меню и попробуйте снова'
            ]
        )
        inlinekeyb=InlineKeyboardMarkup(row_width=1)
        inlinekeyb.add(InlineKeyboardButton(text="↩️ В меню",callback_data='supportbacktomenutwo'))
        await message.answer(text=html_text,reply_markup=inlinekeyb)

