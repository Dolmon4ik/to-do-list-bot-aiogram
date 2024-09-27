from aiogram import Bot, Dispatcher, types, Router
from config import TOKEN
import asyncio
from todolist import database as db
from todolist.database import db_start
from handler import router

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def on_startup():
    await db.db_start()
    print('База данных подключена!')

async def main():
    dp.include_router(router)
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    print('Бот успешно запущен!')
    asyncio.run(main())
