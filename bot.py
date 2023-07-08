import os


import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

from handlers import info_for_hospitalization, send_image
from keyboards.buttons import menu

bot = Bot(token=os.getenv('TOKEN'), parse_mode="HTML")
router = Router()


@router.message(Command(commands=["start", "menu"]))
async def command_start_handler(message: Message):
    await message.answer(
        f"Привет {message.from_user.username}, это помощник врачей отделения травматологии ОГАУЗ ГИМДКБ",
        reply_markup=menu
    )


async def main():
    dp = Dispatcher()
    dp.include_routers(
        router,
        info_for_hospitalization.router,
        send_image.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
