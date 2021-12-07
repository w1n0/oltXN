import hashlib
from aiogram import types, Bot, Dispatcher
from create_bot import bot, dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from weather import get_weather
import time, datetime, os
from house import house_database
from youtube.youtube_parser import searcher
from googletrans import Translator

class FSMsity(StatesGroup):
    ask_sity = State()
    answer_sity = State()

# @dp.message_handler(commands=["start","help"])
async def commands_start(message: types.Message):
    await message.answer_sticker(r'CAACAgIAAxkBAAEDLNJhesopOAINZdbMB8qtORxviLdkygACNQUAAkb7rAQ1FgQgV19OpSEE')
    await bot.send_message(message.from_user.id, "Чем могу быть полезна?", reply_markup=kb_client)


# @dp.message_handler(text=['Погода'])
async def text_weather(message: types.Message):
    await message.answer_sticker(r'CAACAgIAAxkBAAEDLNphesuURXxXGtCKkTsR0GutPAlQ9wACMwUAAkb7rARoQzS0QtDEbyEE')
    await bot.send_message(message.from_user.id, "В каком городе нужно узнать погоду?", reply_markup=kb_weather)


# @dp.message_handler(text=['Питер'])
async def text_weather_spb(message: types.Message):
    await bot.send_message(message.from_user.id, "Метеоцентр 'Крылья по ветру' приступил к работе")
    time.sleep(1)
    answer = get_weather.getting_temperature("Санкт-Петербург")
    await bot.send_message(message.from_user.id, "За окном сейчас " + str(answer) + " градусов")
    answer = get_weather.getting_wind("Санкт-Петербург")
    await bot.send_message(message.from_user.id, "Ветерок поддувает на " + str(answer) + " м/с")
    answer = get_weather.getting_humidity("Санкт-Петербург")
    await bot.send_message(message.from_user.id, "Влажность составляет " + str(answer) +"%")
    answer = get_weather.getting_status("Санкт-Петербург")
    await bot.send_message(message.from_user.id, "В небесах " + str(answer))
    await message.answer_sticker(r'CAACAgIAAxkBAAEDLPdhetiCvFUxQCNSiK9UxGumszRxAAM-BQACRvusBOPYSrsbHfRjIQQ')

# @dp.message_handler(text=['Другой город'], state=None)
async def text_weather_another_ask(message: types.Message, state=FSMsity):
    await FSMsity.ask_sity.set()
    await message.answer_sticker(r'CAACAgIAAxkBAAEDLPlhettBikO-tZDv6ijU8i-tx8FxqAACMwUAAkb7rARoQzS0QtDEbyEE')
    await message.reply("Так, и о каком городе мы говорим?")


#@dp.message_handler(state=FSMsity.ask_sity)
async def text_weather_another_answer(message: types.Message,state=FSMsity):
    try:
        city = message.text
        await bot.send_message(message.from_user.id, "Метеоцентр 'Крылья по ветру' приступил к работе")
        time.sleep(1)
        answer = get_weather.getting_temperature(city)
        await bot.send_message(message.from_user.id, "За окном сейчас " + str(answer) + " °С")
        answer = get_weather.getting_wind(city)
        await bot.send_message(message.from_user.id, "Ветерок поддувает на " + str(answer) + " м/с")
        answer = get_weather.getting_humidity(city)
        await bot.send_message(message.from_user.id, "Влажность составляет " + str(answer) +"%")
        answer = get_weather.getting_status(city)
        await bot.send_message(message.from_user.id, "В небесах " + str(answer))
        await message.answer_sticker(r'CAACAgIAAxkBAAEDLPdhetiCvFUxQCNSiK9UxGumszRxAAM-BQACRvusBOPYSrsbHfRjIQQ')
        await state.finish()
    except:
        await message.answer_sticker(r'CAACAgIAAxkBAAEDLQJheuFvKnHJHmkoE6BdVuQvUaFTeAACLwUAAkb7rAQP18VQze5AgCEE')
        await bot.send_message(message.from_user.id, "Город не найден")
        await state.finish()

class FSMhouse(StatesGroup):
    ask_house_date = State()
    ask_house_date_free = State()
    ask_house_counter = State()
    answer_house_counter = State()


# @dp.message_handler(text=['Кошкин дом'])
async def text_house(message: types.Message):
    await bot.send_message(message.from_user.id, "Что будем делать?", reply_markup=kb_home_counter)


# @dp.message_handler(text=['Показания за 3 мес'])
async def text_3month(message: types.Message):
    await bot.send_message(message.from_user.id, 'За последние 3 месяца ситуация следующая:')
    await house_database.sql_read_last3(message)
    await house_database.sql_read_price(message)

# @dp.message_handler(text=['Полная история'])
async def text_months(message: types.Message):
    await bot.send_message(message.from_user.id, 'Общая история показаний счетчика такова:')
    await house_database.sql_read(message)

# @dp.message_handler(text=['Внести данные'])
async def text_input_data(message: types.Message, state=FSMhouse):
    await bot.send_message(message.from_user.id, 'Первым делом нужно ввести дату показаний')
    await bot.send_message(message.from_user.id, 'Запишем сегодняшним числом или на другой день?', reply_markup=kb_date)
    await FSMhouse.ask_house_date.set()

# @dp.message_handler(text=['Запишем на сегодня'])
async def text_input_date_self(message: types.Message, state=FSMhouse):
    async with state.proxy() as data:
        data['date'] = datetime.date.today()
    await bot.send_message(message.from_user.id, 'Дата записана, а теперь введите цифрой показания счетчика')
    await FSMhouse.ask_house_counter.set()


# @dp.message_handler(text=['Ввести другую дату'])
async def text_input_date_another(message: types.Message, state=FSMhouse):
    await bot.send_message(message.from_user.id, 'Введиде дату без пробелов в формате год месяц день:')
    await bot.send_message(message.from_user.id, 'например, 20211101 (год-месяц-день)')
    await FSMhouse.ask_house_date_free.set()

# @dp.message_handler(state=ask_house_date_free.set())
async def text_input_date_another_step2(message: types.Message, state=FSMhouse):
    try:
        async with state.proxy() as data:
            data['date'] = datetime.datetime.strptime(message.text, '%Y%m%d').date()
        await bot.send_message(message.from_user.id, 'Дата записана, а теперь введите цифрой показания счетчика')
        await FSMhouse.ask_house_counter.set()
    except:
        current_state = await state.get_state()
        await bot.send_message(message.from_user.id, "Дата введена неверно", reply_markup=kb_home_counter)
        if current_state is None:
            return
        await state.finish()

# @dp.message_handler(state=FSMhouse.ask_house_counter)
async def text_input_counter(message: types.Message, state=FSMhouse):
    async with state.proxy() as data:
        data['counter'] = int(message.text)
    await house_database.sql_add(state)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Показания успешно записаны', reply_markup=kb_home_counter)


# @dp.message_handler(text=['Удалить запись'])
async def text_delete(message: types.Message):
    read = await house_database.sql_read2()
    for ret in read:
        await bot.send_message(message.from_user.id, f"На {ret[0]} - {ret[1]} кВт")
        await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup(). \
                               add(InlineKeyboardButton(f'Удалить запись от {ret[0]}', callback_data=f'del {ret[0]}')))

@dp.callback_query_handler (lambda x: x.data and x.data.startswith("del "))
async def callback_run(callback_query : types.CallbackQuery):
    await house_database.sql_delete_command(callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)


# @dp.message_handler(text=['Назад'])
async def text_back(message: types.Message):
    await bot.send_message(message.from_user.id, "Главное меню:", reply_markup=kb_client)

# @dp.message_handler(text=['Отмена'])
async def text_cancel(message: types.Message, state=FSMhouse):
    current_state = await state.get_state()
    await bot.send_message(message.from_user.id, "Возвращаемся в главное меню", reply_markup=kb_client)
    if current_state is None:
        return
    await state.finish()


class FSMyt(StatesGroup):
    yt_ask = State()
    yt_answer = State()


# @dp.message_handler(text=['Поиск на YouTube'])
async def text_ytserach_ask(message: types.Message):
    await bot.send_message(message.from_user.id, "Что именно будем искать?")
    await FSMyt.yt_ask.set()

# @dp.message_handler(text=['Поиск на YouTube'])
async def text_ytserach_amswer(message:types.Message, state=FSMyt):
    await bot.send_message(message.from_user.id, "По вашему запросу в топе выдачи находится следующее:")
    links = searcher(message.text)
    for link in links:
        answer = f'https://www.youtube.com/watch?v={link["id"]}'
        await bot.send_message(message.from_user.id, answer)
    await state.finish()


class FSMtranslate(StatesGroup):
    language_select = State()
    translate_start = State()
    translate_answer = State()

# @dp.message_handler(text=['🎆Перевод с Google Translate'])
async def text_gtranslate_select_language(message: types.Message):
    await bot.send_message(message.from_user.id, "На какой язык нужно перевести?", reply_markup=kb_language)
    await FSMtranslate.language_select.set()

# @dp.message_handlerstate=FSMtranslate.language_select()
async def text_gtranslate_start(message: types.Message):
    global language_from_user
    language_from_user = message.text
    await bot.send_message(message.from_user.id, "Введите слово или выражение, которое хотите перевести", reply_markup=kb_cancel)
    await FSMtranslate.next()


# @dp.message_handler(state=FSMtranslate. translate_start)
async def text_gtranslate_answer(message: types.Message, state=FSMtranslate):
    gTrans = Translator()
    #try:
    if language_from_user == "Английский":
        language = 'en'
        answer = gTrans.translate(message.text, language).text
        await bot.send_message(message.from_user.id, answer, reply_markup=kb_client)
    elif language_from_user == "Русский":
        language = 'ru'
        answer = gTrans.translate(message.text, language).text
        await bot.send_message(message.from_user.id, answer, reply_markup=kb_client)
    else:
        await bot.send_message(message.from_user.id, "Неправильно введен язык - айда сначала!", reply_markup=kb_client)
    '''except:
        await message.answer_sticker(r'CAACAgIAAxkBAAEDLQJheuFvKnHJHmkoE6BdVuQvUaFTeAACLwUAAkb7rAQP18VQze5AgCEE')
        await bot.send_message(message.from_user.id, "Ох, возникла ошибка!", reply_markup=kb_client)'''
    await state.finish()


def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=["start", "help"])
    dp.register_message_handler(text_cancel, text=['Отмена'], state="*")
    dp.register_message_handler(text_weather, text=['🌦Погода️'])
    dp.register_message_handler(text_house, text=['🐱Кошкин дом'])
    dp.register_message_handler(text_weather_spb, text=['Питер'])
    dp.register_message_handler(text_weather_another_ask, text=['Другой город'], state=None)
    dp.register_message_handler(text_weather_another_answer, state=FSMsity.ask_sity)
    dp.register_message_handler(text_house, text=['🐱Кошкин дом'])
    dp.register_message_handler(text_3month, text=['Показания за 3 мес'])
    dp.register_message_handler(text_months, text=['Полная история'])
    dp.register_message_handler(text_input_data, text=['Внести данные'])
    dp.register_message_handler(text_input_date_self, text=['Запишем на сегодня'], state=FSMhouse.ask_house_date)
    dp.register_message_handler(text_input_date_another, text=['Ввести другую дату'], state=FSMhouse.ask_house_date)
    dp.register_message_handler(text_input_date_another_step2, state=FSMhouse.ask_house_date_free)
    dp.register_message_handler(text_input_counter, state=FSMhouse.ask_house_counter)
    dp.register_message_handler(text_delete, text=['Удалить запись'])
    dp.register_message_handler(text_ytserach_ask, text=['🔎Поиск на YouTube'], state=None)
    dp.register_message_handler(text_ytserach_amswer, state=FSMyt.yt_ask)
    dp.register_message_handler(text_gtranslate_select_language, text=['🏷Перевод с Google Translate'], state=None)
    dp.register_message_handler(text_gtranslate_start, state=FSMtranslate.language_select)
    dp.register_message_handler(text_gtranslate_answer, state=FSMtranslate.translate_start)
    dp.register_message_handler(text_back, text=['Назад'])


btn1 = KeyboardButton('🌦Погода️')
btn2 = KeyboardButton('🐱Кошкин дом')
btn3 = KeyboardButton('🔎Поиск на YouTube')
btn4 = KeyboardButton('🏷Перевод с Google Translate')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.row(btn1, btn2).row(btn3, btn4)

w_btn1 = KeyboardButton('Питер')
w_btn2 = KeyboardButton('Другой город')
w_btn3 = KeyboardButton('Назад')
kb_weather = ReplyKeyboardMarkup(resize_keyboard=True).row(w_btn1, w_btn2).add(w_btn3)

h_btn1 = KeyboardButton('Показания за 3 мес')
h_btn2 = KeyboardButton('Полная история')
h_btn3 = KeyboardButton('Внести данные')
h_btn4 = KeyboardButton('Удалить запись')
h_btn5 = KeyboardButton('Назад')
kb_home_counter = ReplyKeyboardMarkup(resize_keyboard=True).row(h_btn1, h_btn2).row(h_btn3, h_btn4).add(h_btn5)

d_btn1 = KeyboardButton('Запишем на сегодня')
d_btn2 = KeyboardButton('Ввести другую дату')
d_btn3 = KeyboardButton('Отмена')
kb_date = ReplyKeyboardMarkup(resize_keyboard=True).row(d_btn1,d_btn2).add(d_btn3)

c_btn1 = KeyboardButton('Отмена')
kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True).row(c_btn1)

t_btn1 = KeyboardButton('Английский')
t_btn2 = KeyboardButton('Русский')
kb_language = ReplyKeyboardMarkup(resize_keyboard=True).row(t_btn1,t_btn2)