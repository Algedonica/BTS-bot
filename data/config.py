import os

from dotenv import load_dotenv

import pymongo
import array
client = pymongo.MongoClient("mongodb+srv://application:application@bosa-cluster.jseku.mongodb.net/cryptocons_dev?retryWrites=true&w=majority")
db = client.cryptocons_dev
user_collection = db.users
ticket_collection= db.tickets
staff_collection=db.staff
settings_collection = db.settings
dbstates = client.aiogram_fsm
states_collection=dbstates.aiogram_state
knowledge_collection = db.knowledge_base
pmessages_collection = db.personal_message
videos_collection = db.videos
load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [
    
]
admincode = str(os.getenv("admincode"))
ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
