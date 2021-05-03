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
from utils.misc import isadmin,support_role_check, xstr, photoparser, parse_message_by_tag_name, getCryptoData, parse_video_by_tag_name, send_to_channel

from keyboards.inline import usersupportchoiceinline, ticket_callback, add_operator_callback, show_support_pages, edit_something_admin, show_cities_pages, knowledge_list_call
from keyboards.default import userendsupport,defaultmenu, operatorcontrol,operatorshowuser
@dp.message_handler(text="/reset", state=[
    ProjectManage.menu, 
    ProjectManage.awaitingsup,
    ProjectManage.initializingsup, 
    ProjectManage.preparingquest, 
    ProjectManage.onair
    ])
async def resetbot_byuser(message: types.Message):
    thisicket=ticket_collection.find_one({"userid": message.from_user.id, "$or":[{'isopen':'onair'},{'isopen':'onpause'}, {'isopen':'created'}]})
    if thisicket!=None:
        ticket_collection.update({"userid": message.from_user.id, "$or":[{'isopen':'onair'},{'isopen':'onpause'}, {'isopen':'created'}]},{"$set":{"isopen":"closedbyclient"}})
        await bot.send_message(chat_id=channelid, text=thisicket['messagedata'])


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
            '<i>Нажмите кнопку «О нас / услуги», чтобы узнать подробнее о компании и всех услугах.</i>',
            '',
            parse_message_by_tag_name(thisuser['citytag'])
        ]
    )
    await message.answer_photo(photo=photoparser('usermainmenu'), caption=html_text,parse_mode='HTML',reply_markup=defaultmenu)
    await ProjectManage.menu.set()



@dp.message_handler(text="/reset", state=[
    SupportManage.menu,
    SupportManage.awaitingsup, 
    SupportManage.initializingsup, 
    SupportManage.onair, 
    SupportManage.changeoperatorname, 
    SupportManage.addcityinput,  
    SupportManage.initcsv,  
    SupportManage.inittimecsv,  
    SupportManage.accept_time,  
    SupportManage.knowledge_set_title,  
    SupportManage.knowledge_set_descr,
    ])
async def resetbot_byoperator(message: types.Message, state: FSMContext):
    thisicket=ticket_collection.find_one({"operator": message.from_user.id,"isopen": "onair"}) 
    if thisicket!=None:
        ticket_collection.update({"operator": message.from_user.id, "isopen": "onair"},{"$set":{"isopen":"closedbyoperator"}})
        await bot.send_message(chat_id=channelid, text=thisicket['messagedata'])
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
    html_text="\n".join(
        [
            '👇 Следите за новыми запросами! 👇'
        ]
    )
    supportmenubase = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(
            text='📄 Входящие запросы',
            callback_data='to_tickets'
        )],
        [InlineKeyboardButton(
            text='⚙️ Настройки (в разработке)',
            callback_data='to_settings'
        )]
    ])

    if isadmin(message.from_user.id)== True:
        supportmenubase.add(InlineKeyboardButton(
            text='💎 Админпанель',
            callback_data='to_admin_menu'
        ))
    if support_role_check(message.from_user.id)== "PLUS":
        supportmenubase.add(InlineKeyboardButton(
            text='🗄 Отчеты',
            callback_data='to_csv_tables'
        ))      
    # await bot.send_message(chat_id=call.from_user.id,text='Диалог завершен',parse_mode='HTML',reply_markup=ReplyKeyboardRemove())
    await bot.send_photo(chat_id=message.from_user.id,photo=photoparser("operatormainmenu"), caption=html_text,parse_mode='HTML',reply_markup=supportmenubase ) 
    await state.reset_state()
    await SupportManage.menu.set()
    