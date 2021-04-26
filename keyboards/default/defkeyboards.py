from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

defaultmenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            # KeyboardButton(text='📲 Техподдержка')
            KeyboardButton(text='💎 О нас / услуги'),
            KeyboardButton(text='💎 Партнерам «КК»'),
        ],
        [
            KeyboardButton(text='🗣 Получить консультацию')
        ],
        [
            KeyboardButton(text='💰 100% годовых — фонд SCHUTZ')
        ],
        [
            KeyboardButton(text='⁉️ База знаний'),
            KeyboardButton(text='💵 Курс BTC/ETH/SST'),
        ]
    ],
    resize_keyboard=True
)

userendsupport = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='✅ Завершить диалог')
        ],
    ],
    resize_keyboard=True
)

operatorshowuser = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🗣 Показать всех ожидающих')
        ],
    ],
    resize_keyboard=True
)

operatorcontrol = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='❌ Завершить'),
            KeyboardButton(text='🗣 Переключиться'),
        ],
    ],
    resize_keyboard=True
)