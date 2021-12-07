from aiogram.utils import executor
from handlers import client_handlers
from create_bot import dp
from house import house_database

client_handlers.register_client_handlers(dp)

async def on_startup(_):
    print("Bot is online")
    house_database.star_home_db()


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
