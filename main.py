import telebot
from telebot import types
import RatePrice
import time


API_TOKEN = 'YOUR API TOKEN'

bot = telebot.TeleBot(API_TOKEN)

first_markup = types.InlineKeyboardMarkup(row_width=2)
button_get = types.InlineKeyboardButton('Узнать курс $', callback_data='get_dol')
button_set = types.InlineKeyboardButton('\U0001F449 Задать границы', callback_data='get_limits')
first_markup.add(button_get, button_set)

first_limit = 0
second_limit = 0


# welcome message
@bot.message_handler(commands=['help', 'start'])
def start_msg(message):
    start_message = f'<b>Привет {message.from_user.first_name}!</b>\n\n' \
                    f'Я бот, присылающий курс доллара если он выйдет за заданные границы\n\n' \
                    f'Выберите действие:'
    bot.send_message(message.chat.id, start_message, parse_mode='html', reply_markup=first_markup)


# the answer when choosing
@bot.callback_query_handler(func=lambda call: True)
def first_menu_answer(call):
    if call.data == 'get_dol':
        bot.send_message(call.message.chat.id, f'Курс доллара на данную минуту составляет:'
                                               f' <b>{RatePrice.print_price()} </b> рублей\nВыберите действие:',
                         parse_mode='html', reply_markup=first_markup)
    if call.data == 'get_limits':
        bot.send_message(call.message.chat.id,
                         f'Курс доллара на данную минуту составляет: <b>{RatePrice.print_price()} </b> рублей',
                         parse_mode='html')
        limit = bot.send_message(call.message.chat.id, 'Введите нижнюю границу', parse_mode='html')
        bot.register_next_step_handler(limit, get_first)


# get first limit
def get_first(message):
    global first_limit
    first_limit = message.text
    limit = bot.send_message(message.chat.id, 'Введите верхнюю границу', parse_mode='html')
    bot.register_next_step_handler(limit, get_second)


# get second limit
def get_second(message):
    global first_limit, second_limit
    second_limit = message.text
    check_input(message)


# checking the numbers
def check_input(message):
    global first_limit, second_limit
    try:
        if (str(first_limit).replace('.', '', 1).isdigit() or first_limit == str(int(first_limit))) and \
                (str(second_limit).replace('.', '', 1).isdigit() or second_limit == str(int(second_limit))):
            bot.send_message(message.chat.id, 'Все окей\nНачинаю работу...\n(Цена обновляется каждую минуту)',
                             parse_mode='html')
            price_in_limits_check(message)
    except ValueError:
        bot.send_message(message.chat.id, 'Вы ввели неправильные границы!', parse_mode='html',
                         reply_markup=first_markup)


# checking the price in the limit
def price_in_limits_check(message):
    global first_limit, second_limit
    while True:
        price = float(RatePrice.print_price())
        if price < float(first_limit):
            bot.send_message(message.chat.id, f'Цена вышла за нижнюю границу и составляет: {price} рублей',
                             parse_mode='html', reply_markup=first_markup)
            break
        elif price > float(second_limit):
            bot.send_message(message.chat.id, f'Цена вышла за верхнюю границу и составляет: {price} рублей',
                             parse_mode='html', reply_markup=first_markup)
            break
        time.sleep(60)


if __name__ == '__main__':
    bot.polling(none_stop=True)
