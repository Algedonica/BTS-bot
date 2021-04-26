from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from data import config
from data.config import client, user_collection
import pymongo
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

# application:thishardpassword@ccbot.1ejqg.mongodb.net/<dbname>?retryWrites=true&w=majority"

# storage = MongoStorage('mongodb+srv://statesconnector:statesconnector@ccbot.1ejqg.mongodb.net/cryptocons?retryWrites=true&w=majority')
storage = MongoStorage(uri='mongodb+srv://statesconnector:statesconnector@bosa-cluster.jseku.mongodb.net/cryptocons_dev?retryWrites=true&w=majority')



# storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)
