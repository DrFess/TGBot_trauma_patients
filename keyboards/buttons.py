from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

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
