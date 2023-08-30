import os

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot import bot
from keyboards.buttons import choose_doctors, image_answers, get_personal_account

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
                caption=f'{data["doctor"]}, Вам сообщение от {message.from_user.username}\nПациент: {data["patient"]}',
                reply_markup=image_answers(message.from_user.id).as_markup()
            )
        else:
            await bot.send_photo(
                chat_id=os.getenv('GROUP_ID'),
                photo=message.photo[-1].file_id,
                caption=f'Доктора, вам сообщение от {message.from_user.username}\nПациент: {data["patient"]}',
                reply_markup=image_answers(message.from_user.id).as_markup()
            )
        await message.reply('Ваше сообщение переслано')
        await state.clear()
    else:
        await message.answer('Возникла ошибка. Попробуем снова?')
        await state.set_state(Steps.start)


@router.callback_query(Text(startswith='answer_1'))
async def answer_1(callback: CallbackQuery):
    user_id = callback.data.split(':')[1]
    await bot.send_message(user_id, text='На контрольных рентгенограммах наблюдается достаточная '
                                         'консолидация(сращение перелома), поэтому возможно удаление металлоконструкции'
                                         'в плановом порядке\nЗапись на плановую госпитализацию проводится по телефону '
                                         '83952218974 по понедельникам с 13.00 до 14.00.\nТакже можно оставить заявку на'
                                         'плановую госпитализацию в личном кабинете портала ОГАУЗ ГИМДКБ',
                           reply_markup=get_personal_account().as_markup())
    await callback.message.answer('Отправлен ответ, что консолидация достаточная и возможна плановая госпитализация'
                                  '(вариант 1)')


@router.callback_query(Text(startswith='answer_2'))
async def answer_2(callback: CallbackQuery):
    user_id = callback.data.split(':')[1]
    await bot.send_message(user_id, text='На контрольных рентгенограммах наблюдается НЕдостаточная '
                                         'консолидация(сращение перелома). Необходимо повторить контрольные '
                                         'рентгенограммы через 1 месяц')
    await callback.message.answer('Отправлен ответ, что необходимо повторить снимки через 1 месяц (вариант 2)')


@router.callback_query(Text(startswith='answer_3'))
async def answer_3(callback: CallbackQuery):
    user_id = callback.data.split(':')[1]
    await bot.send_message(user_id, text='Необходимо уточнить некоторые детали. Перезвоните по телефону 83952218974 '
                                         'в рабочие дни с 14.00 до 15.00')
    await callback.message.answer('Отправлен ответ, что необходимо перезвонить (вариант 3)')
