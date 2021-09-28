from datetime import datetime, timezone
from typing import Callable
from aiogram import types
from aiogram.types import InputFile, ReplyKeyboardRemove, message
from aiogram.types.fields import ListField
from loader import dp, bot
from data.config import user_collection, ticket_collection, staff_collection, settings_collection, wallets_collection, advertise_collection
from states import ProjectManage,SupportManage
from aiogram.types import CallbackQuery,ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto
from utils.misc import isadmin,support_role_check, photoparser
import secrets
from keyboards.inline import csv_tables_call,wallet_call
from keyboards.default import userendsupport,defaultmenu
from aiogram.dispatcher.handler import CancelHandler
from handlers.users.echo import scheduler

@dp.message_handler(state=ProjectManage.menu, text='🔐 Кошельки')
async def my_wallets_user(message: types.Message):
    thisuserwallets=wallets_collection.find({'user_id':message.from_user.id,'is_active':'active'})
    inlinekeys = InlineKeyboardMarkup(row_width=2)
    html_text=''
    if thisuserwallets.count()==0:
        html_text="\n".join(
            [
                '🔐 Кошельки',
                'У вас еще нет добавленных контактов.',
                'Добавьте прямо сейчас, это легко!'
            ]
        )
    else:
        walletscount=thisuserwallets.count()
        html_text="\n".join(
            [
                '🔐 Кошельки',
                'Всего '+str(walletscount)+' кошельков'
            ]
        )
        for x in thisuserwallets:
            thisbutton = InlineKeyboardButton(text=x['name'],callback_data=wallet_call.new(command='sac', param1=x['item_id'], param2='none'))
            inlinekeys.add(thisbutton)
    inlinekeys.add(
        InlineKeyboardButton(
            text='↩️ В меню',
            callback_data='userbacktomenu'
            ),
        InlineKeyboardButton(
            text='➕ Добавить',
            callback_data='new_wallet'
            )
        )
        
    await message.answer(html_text, reply_markup=inlinekeys)

@dp.callback_query_handler(text='userbacktowallets', state=ProjectManage.menu)
async def my_wallets_usertwo(call:CallbackQuery):
    thisuserwallets=wallets_collection.find({'user_id':call.from_user.id,'is_active':'active'})
    inlinekeys = InlineKeyboardMarkup(row_width=2)
    html_text=''
    if thisuserwallets.count()==0:
        html_text="\n".join(
            [
                '🔐 Кошельки',
                'У вас еще нет добавленных контактов.',
                'Добавьте прямо сейчас, это легко!'
            ]
        )
    else:
        walletscount=thisuserwallets.count()
        html_text="\n".join(
            [
                '🔐 Кошельки',
                'Всего '+str(walletscount)+' кошельков'
            ]
        )
        for x in thisuserwallets:
            thisbutton = InlineKeyboardButton(text=x['name'],callback_data=wallet_call.new(command='sac', param1=x['item_id'], param2='none'))
            inlinekeys.add(thisbutton)
    inlinekeys.add(
        InlineKeyboardButton(
            text='↩️ В меню',
            callback_data='userbacktomenu'
            ),
        InlineKeyboardButton(
            text='➕ Добавить',
            callback_data='new_wallet'
            )
        )
        
    await call.message.edit_text(html_text, reply_markup=inlinekeys)

#иниц.добавл
@dp.callback_query_handler(text='new_wallet', state=ProjectManage.menu)
async def my_wallets_new_init(call:CallbackQuery):    
    html_text="\n".join(
        [
            '➕ Добавление контакта',
            'Отправьте @username контакта',
            'или название для кошелька'
        ]
    )
    
    await call.message.answer(text='_',parse_mode='HTML', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id+1)
    await call.message.edit_text(text=html_text, reply_markup=None)
    await ProjectManage.addingwallet_name.set()
#добавление имени
@dp.message_handler(state=ProjectManage.addingwallet_name)
async def my_wallets_new_addname(message:types.Message, state:FSMContext):    
    html_text="\n".join(
        [
            '➕ Добавление контакта',
            'Отлично, а теперь адрес кошелька.',
        ]
    )
    await ProjectManage.addingwallet_wallet.set()
    await state.update_data(name=message.text)
    await message.answer(text=html_text, reply_markup=ReplyKeyboardRemove())
#добавление адреса
@dp.message_handler(state=ProjectManage.addingwallet_wallet)
async def my_wallets_new_addr(message:types.Message, state:FSMContext):   
    data = await state.get_data()
    name = data.get("name")

    wallets_collection.insert_one({
        'item_id':secrets.token_hex(4)+'WALLET'+"{:03d}".format(secrets.randbelow(999)),
        'name':name,
        'wallet':message.text,
        'user_id':message.from_user.id,
        'is_active':'active',
        "date": datetime.now(),
    })

    html_text="\n".join(
        [
            '✅ Контакт добавлен',
            '',
            name,
            message.text
        ]
    )
    await state.reset_state()
    await ProjectManage.menu.set()
    await message.answer(text=html_text, reply_markup=defaultmenu)
    
    thisuserwallets=wallets_collection.find({'user_id':message.from_user.id,'is_active':'active'})
    inlinekeys = InlineKeyboardMarkup(row_width=2)
    html_text=''
    if thisuserwallets.count()==0:
        html_text="\n".join(
            [
                '🔐 Кошельки',
                'У вас еще нет добавленных контактов.',
                'Добавьте прямо сейчас, это легко!'
            ]
        )
    else:
        walletscount=thisuserwallets.count()
        html_text="\n".join(
            [
                '🔐 Кошельки',
                'Всего '+str(walletscount)+' кошельков'
            ]
        )
        for x in thisuserwallets:
            thisbutton = InlineKeyboardButton(text=x['name'],callback_data=wallet_call.new(command='sac', param1=x['item_id'], param2='none'))
            inlinekeys.add(thisbutton)
    inlinekeys.add(
        InlineKeyboardButton(
            text='↩️ В меню',
            callback_data='userbacktomenu'
            ),
        InlineKeyboardButton(
            text='➕ Добавить',
            callback_data='new_wallet'
            )
        )
        
    await message.answer(html_text, reply_markup=inlinekeys)


#открыть кошель
@dp.callback_query_handler(wallet_call.filter(command='sac'), state=ProjectManage.menu)
async def my_wallets_open(call:CallbackQuery, callback_data:dict):
    wallet_id = callback_data.get("param1")
    thiswallet = wallets_collection.find_one({'item_id':wallet_id})
    inlinekeys = InlineKeyboardMarkup(row_width=2)
    html_text="\n".join(
        [
            thiswallet['name'],
            ' ',
            thiswallet['wallet']
        ]
    )

    inlinekeys.add(
        InlineKeyboardButton(
            text='↩️ Назад',
            callback_data='userbacktowallets'
            ),
        InlineKeyboardButton(
            text='❌ Удалить',
            callback_data=wallet_call.new(command='sadd', param1=thiswallet['item_id'], param2='none')
            )
        )
    await call.message.edit_text(html_text, reply_markup=inlinekeys)

#удалить кошель
@dp.callback_query_handler(wallet_call.filter(command='sadd'), state=ProjectManage.menu)
async def my_wallets_open(call:CallbackQuery, callback_data:dict):
    wallet_id = callback_data.get("param1")

    wallets_collection.find_and_modify(
        query={"item_id": wallet_id},
        update={"$set":{"is_active":"deleted"}}
    )

    thisuserwallets=wallets_collection.find({'user_id':call.from_user.id, 'is_active':'active'})
    inlinekeys = InlineKeyboardMarkup(row_width=2)
    html_text=''
    if thisuserwallets.count()==0:
        html_text="\n".join(
            [
                '🔐 Кошельки',
                'У вас еще нет добавленных контактов.',
                'Добавьте прямо сейчас, это легко!'
            ]
        )
    else:
        walletscount=thisuserwallets.count()
        html_text="\n".join(
            [
                '🔐 Кошельки',
                'Всего '+str(walletscount)+' кошельков'
            ]
        )
        for x in thisuserwallets:
            thisbutton = InlineKeyboardButton(text=x['name'],callback_data=wallet_call.new(command='sac', param1=x['item_id'], param2='none'))
            inlinekeys.add(thisbutton)
    inlinekeys.add(
        InlineKeyboardButton(
            text='↩️ В меню',
            callback_data='userbacktomenu'
            ),
        InlineKeyboardButton(
            text='➕ Добавить',
            callback_data='new_wallet'
            )
        )
    await call.message.edit_text(html_text, reply_markup=inlinekeys)

