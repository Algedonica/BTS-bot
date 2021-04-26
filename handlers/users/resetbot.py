# from aiogram import types
# from data.config import user_collection, staff_collection, settings_collection
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
# from loader import dp,bot
# from states import ProjectManage,SupportManage, SetupBTSstates
# from aiogram.dispatcher import FSMContext
# from utils.misc import issupport, parse_city, isadmin, support_role_check, xstr, photoparser
# from aiogram.types import InputMediaPhoto
# from keyboards.default import defaultmenu,operatorshowuser
# from keyboards.inline import usersupportchoiceinline, ticket_callback, add_operator_callback, show_support_pages, edit_something_admin, show_cities_pages

# @dp.message_handler(text="/reset", state=[
#     ProjectManage.menu, 
#     ProjectManage.awaitingsup, 
#     ProjectManage.getcityuser, 
#     ProjectManage.initializingsup, 
#     ProjectManage.preparingquest, 
#     ProjectManage.onair, 
#     ProjectManage.changeoperatorname,
#     ])