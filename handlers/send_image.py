import os

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot import bot
from keyboards.buttons import choose_doctors


router = Router()


class Steps(StatesGroup):
    start = State()
    doctors = State()
    end = State()


@router.message(Text(text='Отправить рентгенологические снимки'))
async def send_surname_name(message: Message, state: FSMContext):
    await state.set_state(Steps.start)
    await message.answer('Отправьте фамилию и имя пациента', reply_markup=ReplyKeyboardRemove())


@router.message(Steps.start)
async def choose_doctor(message: Message, state: FSMContext):
    await state.update_data(patient=message.text)
    await state.set_state(Steps.doctors)
    await message.answer('Укажите кому из врачей отправить снимки', reply_markup=choose_doctors)


@router.message(Steps.doctors)
async def choose_format(message: Message, state: FSMContext):
    await state.update_data(doctor=message.text)
    await state.set_state(Steps.end)
    await message.answer('Отправьте изображение')


@router.message(Steps.end)
async def send_image(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.photo:
        if data['doctor'] != 'Любому врачу':
            await bot.send_photo(
                chat_id=os.getenv('GROUP_ID'),
                photo=message.photo[-1].file_id,
                caption=f'{data["doctor"]}, Вам сообщение от {message.from_user.username}\nПациент: {data["patient"]}'
            )
        else:
            await bot.send_photo(
                chat_id=os.getenv('GROUP_ID'),
                photo=message.photo[-1].file_id,
                caption=f'Доктора, вам сообщение от {message.from_user.username}\nПациент: {data["patient"]}'
            )
        await message.reply('Ваше сообщение переслано')
        await state.clear()
    else:
        await message.answer('Возникла ошибка. Попробуем снова?')
        await state.set_state(Steps.start)
