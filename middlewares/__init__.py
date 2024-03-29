from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .maintenance import OndevMiddleware

def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(OndevMiddleware())
