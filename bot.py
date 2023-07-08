import os


import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command(commands=["start", "menu"]))
async def command_start_handler(message: Message):
    await message.answer("Hi! I'm working")


async def main():
    bot = Bot(token=os.getenv('TOKEN'), parse_mode="HTML")
    dp = Dispatcher()
    dp.include_routers(
        router
    )

    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())