from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import math
import random
from datetime import datetime
from data.config import user_collection, staff_collection, settings_collection, pmessages_collection
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from loader import dp,bot
from states import ProjectManage,SupportManage, SetupBTSstates
from aiogram.dispatcher import FSMContext
from utils.misc import issupport, parse_city, isadmin, support_role_check, xstr, photoparser, parse_message_by_tag_name
from aiogram.types import InputMediaPhoto
from keyboards.default import defaultmenu,operatorshowuser
from keyboards.inline import usersupportchoiceinline, ticket_callback, add_operator_callback, show_support_pages, edit_something_admin, show_cities_pages

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if staff_collection.find({"staffrole":"owner"}).count()<1:
        html_text="\n".join(
            [
                '<b>Спасибо за приобретение BTS!</b>',
                '',
                'Чтобы начать работу и настроить систему, пожалуйста, подготовьте ваш уникальный код и приготовьтесь его ввести'
            ]
        )
        setupsys= InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [InlineKeyboardButton(
                text='Давайте начинать!',
                callback_data='initialize_bts_setup'
            )]
        ]) 
        await message.answer(text=html_text,parse_mode='HTML',reply_markup=setupsys)
        await SetupBTSstates.getadmincode.set()

    else:
        if issupport(message.from_user.id) == True:
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
            await message.answer_photo(photo=photoparser("operatormainmenu"), caption=html_text,parse_mode='HTML',reply_markup=supportmenubase )     
            # await message.answer(text=html_text,parse_mode='HTML',reply_markup=supportmenubase ) 
            await SupportManage.menu.set()  
        else:
            if user_collection.count_documents({"user_id": message.from_user.id}) == 0 and message.from_user.is_bot==False:
                    
                photoo = settings_collection.find_one({"settings":"mainsettings"})
                photoo_add= photoo["photos_profile"]
                pdasasd = photoo_add[random.randint(0, 14)]

                deeplink = "none"
                deeplink = message.get_args()
                user_collection.insert_one(
                {"user_id": message.from_user.id,
                "first_name": xstr(message.from_user.first_name),
                "last_name": xstr(message.from_user.last_name),
                "username": xstr(message.from_user.username),
                "callmeas":"none",
                "citytag":"none",
                "city":"none",
                "came_from": deeplink,
                "when_came": datetime.now(),
                "user_photo":pdasasd
                })
                html_text="\n".join(
                    [
                        '<b>Здравствуйте 👋</b>',
                        ' ',
                        '<i>На связи 💎«Крипто Консалтинг».</i>',
                        '<i>Для начала работы, пожалуйста, укажите ваше имя и выберите свой город.</i>'
                    ]
                )
                inlinebutt = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                    [InlineKeyboardButton(
                        text='Продолжить',
                        callback_data='start_meeting_user'
                    )],
                ]) 
                await bot.send_message(chat_id= message.from_user.id, text=html_text,parse_mode='HTML', reply_markup=inlinebutt)
                await ProjectManage.startmeeting.set()
#################################################User Meet#############################################33                    
@dp.callback_query_handler(text='start_meeting_user', state=ProjectManage.startmeeting)
async def start_meeting_user_func(call:types.CallbackQuery):
    html_text="\n".join(
        [
            '<b>Как к вам обращаться?</b>',
            ' ',
            'Имя будет отображаться в диалоге с технической поддержкой.'
        ]
    )
    await ProjectManage.getnameuser.set()
    await call.message.edit_text(text=html_text, parse_mode='HTML', reply_markup=None)


@dp.callback_query_handler(text="add_city_user_another", state=ProjectManage.getcityuser)
async def addglblcity_init_func(call: types.CallbackQuery):
    html_text="\n".join(
        [
            '<i>🌇 Напишите название города:</i>'
        ]
    )
    await ProjectManage.addglblcity.set()
    await call.message.edit_caption(caption=html_text, parse_mode='HTML', reply_markup=None ) 

@dp.message_handler(state=ProjectManage.addglblcity)
async def addglbl_func(message: types.Message):
    citycode="GLBL"
    city = message.text

    user_collection.find_and_modify(
        query={"user_id":message.from_user.id},
        update={"$set":{"city":city, "citytag":citycode}}
    )

   
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
        ]
    )
    await ProjectManage.menu.set()
    await message.answer_photo(photo=photoparser('usermainmenu'),caption=html_text, parse_mode='HTML', reply_markup= defaultmenu ) 


@dp.callback_query_handler(show_cities_pages.filter(command='pickcityuser'), state=ProjectManage.getcityuser)
async def pickcityuser_func(call: types.CallbackQuery, callback_data:dict):
    citycode=callback_data.get("page")
    city = parse_city(citycode)


    user_collection.find_and_modify(
        query={"user_id":call.from_user.id},
        update={"$set":{"city":city, "citytag":citycode}}
    )



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
            parse_message_by_tag_name(citycode)
        ]
    )
    # await state.reset_state()
    await ProjectManage.menu.set()
    await call.message.delete()
    await call.message.answer_photo(photo=photoparser('usermainmenu'), caption=html_text ,reply_markup=defaultmenu)






########################################################Все что ниже должно быть внизу########################################################








@dp.message_handler(state=[ProjectManage.getnameuser, ProjectManage.getcityuser])
async def askcityuser_func(message: types.Message):
    user_collection.find_and_modify(
        query={"user_id":message.from_user.id},
        update={"$set":{"callmeas":message.text}}
    )
    
    page = 1
    prevpage = page - 1
    nextpage = page + 1
    inlinekeys = InlineKeyboardMarkup(row_width=2)
    x=settings_collection.find_one({"settings":"mainsettings"})
    cities_obj=x["current_cities"]
    cities_on_page = cities_obj[((page-1)*5):(5*page)]

    for y in cities_on_page:
        if y['code']!="GLBL":
            inlinekeys.add(InlineKeyboardButton(text=y['city'], callback_data=show_cities_pages.new("pickcityuser",page=y['code'])))


    
    
    if prevpage < 1:
        prevtoadd=InlineKeyboardButton(
            text='◀️',
            callback_data=show_cities_pages.new("usershowcity",page=1)
        )
    else:
        prevtoadd=InlineKeyboardButton(
            text='◀️',
            callback_data=show_cities_pages.new("usershowcity",page=prevpage)
        )

    if  math.ceil(len(cities_obj)/5)==page:
        nexttoadd=InlineKeyboardButton(
            text='▶️',
            callback_data=show_cities_pages.new("usershowcity",page=page)
        )      
    else:
        nexttoadd=InlineKeyboardButton(
            text='▶️',
            callback_data=show_cities_pages.new("usershowcity",page=nextpage)
        )
    html_text="\n".join(
        [
            '<i><b>'+message.text+'</b>, приятно познакомиться 🙌</i>',
            '<i>🤖 Я бот-помощник ООО «Крипто Консатинг».</i>',
            '<i>📡 Я живу в телеграм, а вы?</i>',
            '<i>💎 Наши офисы открыты в нескольких городах России. Если мы еще не открылись в вашем, выберите «Другой» и напишите название.</i>',
        ]
    )      
    inlinekeys.add(prevtoadd,nexttoadd)
    inlinekeys.add(InlineKeyboardButton(text='Другой',callback_data='add_city_user_another'))
    await ProjectManage.getcityuser.set()
    await message.answer_photo(photo=photoparser('useraskcity') ,caption=html_text, parse_mode='HTML', reply_markup=inlinekeys)
























@dp.message_handler(state=ProjectManage.menu)
async def menu_hand(message: types.Message, state: FSMContext):  
    if issupport(message.from_user.id) == True:
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
        await state.reset_state()
        await SupportManage.menu.set()  
        #await message.answer(text=html_text,parse_mode='HTML',reply_markup=supportmenubase )
        await message.answer_photo(photo=photoparser("operatormainmenu"), caption=html_text,parse_mode='HTML',reply_markup=supportmenubase )    
    else:    
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
        await state.reset_state()
        await ProjectManage.menu.set() 
        # await message.answer(text=html_text,parse_mode='HTML',reply_markup=defaultmenu)
        await message.answer_photo(photo=photoparser('usermainmenu'), caption=html_text ,reply_markup=defaultmenu)








@dp.message_handler(content_types=['photo'], state=SupportManage.menu)
async def parsephoto_hand(message: types.Message, state: FSMContext): 
    # photoo = settings_collection.find_one({"settings":"mainsettings"})
    # photoo_add= photoo["photos_profile"]
    # pdasasd = photoo_add[random.randint(0, 14)]
    await message.answer(text=message.photo[0].file_id)
    await bot.send_photo(chat_id=message.from_user.id, photo=message.photo[0].file_id)

@dp.message_handler(content_types=['video_note'], state=SupportManage.menu)
async def parse_video_note_hand(message: types.Message, state: FSMContext): 
    await message.answer(text=message.video_note.file_id)
    await bot.send_video_note(chat_id=message.from_user.id, video_note=message.video_note.file_id)


@dp.message_handler(content_types=['video'], state=SupportManage.menu)
async def parse_video_hand(message: types.Message, state: FSMContext): 
    await message.answer(text=message.video.file_id)
    await bot.send_video(chat_id=message.from_user.id, video=message.video.file_id)













@dp.message_handler(state=SupportManage.menu)
async def support_menu_hand(message: types.Message, state: FSMContext):  
    if issupport(message.from_user.id) == True:
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
        await state.reset_state()
        await SupportManage.menu.set()     
        # await message.answer(text=html_text,parse_mode='HTML',reply_markup=supportmenubase )
        await message.answer_photo(photo=photoparser("operatormainmenu"), caption=html_text,parse_mode='HTML',reply_markup=supportmenubase )   
    else:    
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
        await state.reset_state()
        await ProjectManage.menu.set() 
        # await message.answer(text=html_text,parse_mode='HTML',reply_markup=defaultmenu) 
        await message.answer_photo(photo=photoparser('usermainmenu'), caption=html_text ,reply_markup=defaultmenu)   
@dp.message_handler(state=SetupBTSstates.getadmincode)
async def blockbts(message: types.Message):
    html_text="\n".join(
            [
                '<b>Спасибо за приобретение BTS!</b>',
                '',
                'Чтобы начать работу и настроить систему, пожалуйста, подготовьте ваш уникальный код и приготовьтесь его ввести'
            ]
    )
    setupsys= InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(
            text='Давайте начинать!',
            callback_data='initialize_bts_setup'
        )]
    ]) 
    await message.answer(text=html_text,parse_mode='HTML',reply_markup=setupsys)
