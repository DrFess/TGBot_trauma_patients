from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def image_answers(user_id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='На плановую госпитализацию', callback_data=f'answer_1:{user_id}'))
    builder.row(InlineKeyboardButton(text='Повторить снимок через 1 месяц', callback_data=f'answer_2:{user_id}'))
    builder.row(InlineKeyboardButton(text='Свяжитесь с нами', callback_data=f'answer_3:{user_id}'))
    return builder


def get_personal_account():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Личный кабинет пациента ИМДКБ', url='https://imdkb.mzio.ru/'))
    return builder


menu_buttons = [
    [KeyboardButton(text='Отправить рентгенологические снимки')],
    [KeyboardButton(text='Получить список анализов для плановой госпитализации')],
]
menu = ReplyKeyboardMarkup(keyboard=menu_buttons, resize_keyboard=True)

choose_doctors_buttons = [
    [KeyboardButton(text='Яковлев А.Б.')],
    [KeyboardButton(text='Большаков Г.А.')],
    [KeyboardButton(text='Дегтярев А.А.')],
    [KeyboardButton(text='Зеленин И.В.')],
    [KeyboardButton(text='Остапенко В.Г.')],
    [KeyboardButton(text='Любому врачу')]
]
choose_doctors = ReplyKeyboardMarkup(keyboard=choose_doctors_buttons, one_time_keyboard=True, resize_keyboard=True)
