# from utils.set_bot_commands import set_default_commands
from handlers.users.echo import scheduler

async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    scheduler.start()  
    # await set_default_commands(dp)

async def shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()
    
if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=shutdown)
