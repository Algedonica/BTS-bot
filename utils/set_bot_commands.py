from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("reset", "Сброс и возврат в главное меню (используйте только в случае если вы застряли)")
    ])
