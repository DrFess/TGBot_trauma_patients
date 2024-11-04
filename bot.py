import os


import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

from handlers import info_for_hospitalization, send_image
from keyboards.buttons import menu
from utils import read_json

bot = Bot(token=os.getenv('TOKEN'), parse_mode="HTML")
router = Router()


@router.message(Command(commands=["start", "menu"]))
async def command_start_handler(message: Message):
    doctors_id = read_json('doctors_id.json')
    if message.from_user.id in doctors_id.values():
        await message.answer(
            f"Спасибо, что пользуетесь нашим ботом. Предложения по улучшению или замечания адресовать @DrFess"
        )
    else:
        await message.answer(
            f"Привет {message.from_user.username}, это помощник врачей отделения травматологии ОГАУЗ ГИМДКБ. "
            f"Чтобы отправить снимки, нажмите на кнопку Отправить рентгенологические снимки, затем выберите врача "
            f"или укажите Любому врачу",
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
