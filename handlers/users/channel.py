import secrets
import math
from datetime import datetime
from aiogram import types
from loader import dp, bot
from data.config import user_collection, ticket_collection, staff_collection, settings_collection, states_collection, pmessages_collection
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
from utils.misc import isadmin,support_role_check, xstr, photoparser, parse_message_by_tag_name, getCryptoData, parse_video_by_tag_name

from keyboards.inline import usersupportchoiceinline, ticket_callback, add_operator_callback, show_support_pages, edit_something_admin, show_cities_pages, knowledge_list_call
from keyboards.default import userendsupport,defaultmenu, operatorcontrol,operatorshowuser


@dp.message_handler(state=SupportManage.menu, text='канал')
async def channelgetid(message: types.Message):
    await bot.send_message(chat_id=-1001330118375, text='_',parse_mode='HTML', reply_markup=None)