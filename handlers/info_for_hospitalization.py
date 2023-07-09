from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message

router = Router()


@router.message(Text(text='Получить список анализов для плановой госпитализации'))
async def send_hospitalization_info(message: Message):
    await message.answer('При себе иметь ручку для заполнения документов.\n'
                         '1. Направление на госпитализацию из поликлиники, другого ЛПУ, подписанное лечащим врачом, '
                         'заверенного печатью направившего учреждения.\n'
                         '2. Общий анализ крови развернутый + сахар крови. (действителен 10 дней)\n'
                         '3. Общий анализ мочи. (действителен 10 дней)\n'
                         '4. Кал на я/глист и соскоб на энтеробиобиоз. (действителен 10 дней)\n'
                         '5. Кал на диз. группу (детям до 2-х лет). (действителен 14 дней)\n'
                         '6. Кровь на УМСС (всем детям). (действителен 10 дней)\n'
                         '7. Флюорография грудной клетки (детям старше 15 лет).\n'
                         '8. Справка об осмотре ребенка педиатром в поликлинике по месту жительства перед '
                         'госпитализацией. (действителен 3 дня)\n'
                         '9. Справка о перенесенных детских инфекционных заболеваниях.\n'
                         '10. Справка об эпид.окружении. (Справка об отсутствии контактов с инфекционными больными по '
                         'месту жительства (от педиатра поликлиники) и из детского учреждения (школа, д/сад ит.д.) за '
                         'последние 3 недели. Справка действительна 3 дня.)\n'
                         '11. Справка о прививках, выделить КОРЬ.\n\n'
                         'ДОПОЛНИТЕЛЬНО при госпитализации для проведения планового оперативного лечения:\n'
                         '1. Маркеры гепатита С, гепатита В (действителен 1 месяц)\n'
                         '2. ЭКГ. (действителен 1 месяц)\n'
                         '3. Группа крови с типированием, резус-фактор.\n'
                         '4. Биохимический анализ крови (о. белок, сахар, билирубин).(действителен 10 дней)\n\n'
                         'Иногородним детям:\n'
                         '1. Копию страхового полиса, копию свидетельства о рождении.\n'
                         '2. Паспорт, копию паспорта одного из родителей.\n\n'
                         'Сопровождающим необходимо иметь:\n'
                         '1. Кровь на УМСС. (действителен 10 дней)\n'
                         '2. ФЛГ грудной клетки.\n'
                         '3. Справка от гинеколога. (действителен 6 месяцев)\n'
                         '4. Анализ кала на диз. группу (при поступлении с ребенком до 2-х лет).\n'
                         '5. Справка о вакцинации против КОРИ.\n'
                         'http://xn--90aflji.xn--p1ai/travmatologicheskoye'
                         )
    await message.answer('Запись на плановую госпитализацию проводится по телефону 83952218974 по понедельникам с 13.00'
                         ' до 14.00.\nТакже с нами можно связаться по электронной почте travmaimdkb@mail.ru')