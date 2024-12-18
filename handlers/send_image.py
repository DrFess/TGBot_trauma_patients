import os

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot import bot
from keyboards.buttons import choose_doctors, image_answers, get_personal_account, image_answers_only_doctor
from utils import read_json

router = Router()


class Steps(StatesGroup):
    start = State()
    doctors = State()
    end = State()


class AnswerMessage(StatesGroup):
    start = State()


@router.message(Text(text='Отправить рентгенологические снимки'))
async def send_surname_name(message: Message, state: FSMContext):
    await state.set_state(Steps.start)
    await message.answer('Укажите сколько прошло времени с момента операции (в месяцах) или дату операции.'
                         '\nЕсли операции не было, укажите "без операции"',
                         reply_markup=ReplyKeyboardRemove())


@router.message(Steps.start)
async def choose_doctor(message: Message, state: FSMContext):
    await state.update_data(operation_time=message.text)
    await state.set_state(Steps.doctors)
    await message.answer('Укажите кому из врачей отправить снимки', reply_markup=choose_doctors)


@router.message(Steps.doctors)
async def choose_format(message: Message, state: FSMContext):
    await state.update_data(doctor=message.text)
    await state.set_state(Steps.end)
    await message.answer('Отправьте изображение')


@router.message(Steps.end)
async def send_image(message: Message, state: FSMContext):
    doctors_id = read_json('doctors_id.json')
    data = await state.get_data()
    if message.photo:
        if data['doctor'] == 'Любому врачу':
            await bot.send_photo(
                chat_id=os.getenv('GROUP_ID'),
                photo=message.photo[-1].file_id,
                caption=f'Доктора, вам сообщение от {message.from_user.username}\n'
                        f'Срок операции: {data["operation_time"]}',
                reply_markup=image_answers(message.from_user.id).as_markup()
            )
        else:
            doctor = data.get('doctor')
            await bot.send_photo(
                chat_id=doctors_id.get(doctor),
                photo=message.photo[-1].file_id,
                caption=f'Вам сообщение от {message.from_user.username}\n'
                        f'Срок операции: {data["operation_time"]}',
                reply_markup=image_answers_only_doctor(message.from_user.id).as_markup()
            )
        await message.reply('Ваше сообщение доставлено. Ожидайте, сообщение доктора пришлю Вам, как только он ответит')
        await state.clear()
    else:
        await message.answer('Возникла ошибка. Попробуем снова?')
        await state.set_state(Steps.start)


@router.callback_query(Text(startswith='answer_1'))
async def answer_1(callback: CallbackQuery):
    user_id = callback.data.split(':')[1]
    await bot.send_message(user_id, text='На контрольных рентгенограммах наблюдается достаточная '
                                         'консолидация(сращение перелома), поэтому возможно удаление металлоконструкции'
                                         ' в плановом порядке\nЗапись на плановую госпитализацию в личном кабинете '
                                         'портала ОГАУЗ ГИМДКБ (https://imdkb.mzio.ru/)\n'
                                         'Подробная инструкция - http://xn--90aflji.xn--p1ai/f/instrukciya_dlya_zapisi_na_planovuyu_gospitalizaciyu_v_travmatologo.pdf',
                           reply_markup=get_personal_account().as_markup())
    await callback.message.answer('Отправлен ответ, что консолидация достаточная и возможна плановая госпитализация'
                                  '(вариант 1)')


@router.callback_query(Text(startswith='answer_2'))
async def answer_2(callback: CallbackQuery):
    user_id = callback.data.split(':')[1]
    await bot.send_message(user_id, text='На контрольных рентгенограммах наблюдается НЕдостаточная '
                                         'для удаления консолидация(сращение перелома). '
                                         'Необходимо повторить контрольные рентгенограммы через 1 месяц')
    await callback.message.answer('Отправлен ответ, что необходимо повторить снимки через 1 месяц (вариант 2)')


@router.callback_query(Text(startswith='answer_3'))
async def answer_3(callback: CallbackQuery):
    user_id = callback.data.split(':')[1]
    await bot.send_message(user_id, text='Необходимо уточнить некоторые детали. Перезвоните по телефону 83952218974 '
                                         'в рабочие дни с 14.00 до 15.00')
    await callback.message.answer('Отправлен ответ, что необходимо перезвонить (вариант 3)')


@router.callback_query(Text(startswith='answer_4'))
async def answer_4(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AnswerMessage.start)
    user_id = callback.data.split(':')[1]
    await state.update_data(user_id=user_id)
    await callback.message.answer('Пришли мне текст сообщения, которое нужно переслать в ответ')


@router.message(AnswerMessage.start)
async def send_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    who_send_answer = data.get('user_id')
    text_answer = message.text
    await bot.send_message(who_send_answer, text=text_answer)
    await message.answer('Ваше сообщение переслано.')
    await state.clear()
